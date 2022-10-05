import queue
import threading
import time
import requests
from flask import Flask, request
from threading import Thread
from Cooks import *
from Menu import *

threads = []
Orders = []
Ordered_items = queue.Queue()
time_unit = 1
app = Flask(__name__)


@app.route('/order', methods=['GET', 'POST'])
def order():
    orders = request.get_json()
    new_order(orders)
    print(f'Received order from dinning-hall with ID: {orders["order_id"]}\n  ')
    return {'success': True}


def new_order(order):
    received_order = {
        'table_id': order['table_id'],
        'order_id': order['order_id'],
        'items': order['items'],
        'items_number': len(order['items']),
        'waiter_id': order['waiter_id'],
        'priority': order['priority'],
        'max_wait': order['max_wait'],
        'received_time': time.time(),
        'cooking_details': queue.Queue(),
        'prepared_items': 0,
        'time_start': order['time_start'],
    }
    Orders.append(received_order)
    for id in received_order['items']:
        order_item = next((item for i, item in enumerate(Menu) if item['id'] == id), None)
        if order_item is not None:
            Ordered_items.put_nowait({'food_id': order_item['id'], 'order_id': order['order_id']})


def cooking_process(cook, food_items: queue.Queue):
    while True:
        try:
            food_item = food_items.get_nowait()
            food_details = next((f for f in Menu if f['id'] == food_item['food_id']), None)
            (idx, order_details) = next(((idx, order) for idx, order in enumerate(Orders) if order['order_id'] == food_item['order_id']), (None, None))
            len_order_items = len(Orders[idx]['items'])
            if food_details['complexity'] == cook['rank'] or food_details['complexity'] == cook['rank'] - 1:
                print(f'{threading.current_thread().name} cooking food {food_details["name"]}: with Id {food_details["id"]} for order {order_details["order_id"]}')
                time.sleep(food_details['preparation-time'] * time_unit)
                Orders[idx]['prepared_items'] += 1
                if Orders[idx]['prepared_items'] == len_order_items:
                    print(f'{threading.current_thread().name} cook finished order {order_details["order_id"]}')
                    Orders[idx]['cooking_details'].put({'food_id': food_details['id'], 'cook_id': cook['id']})
                    finish_preparation_time = int(time.time())
                    payload = {
                        **Orders[idx],
                        'cooking_time': finish_preparation_time - int(Orders[idx]['received_time']),
                        'cooking_details': list(Orders[idx]['cooking_details'].queue)
                    }
                    requests.post('http://dinninghall:80/distribution', json=payload, timeout=0.0000000001)

            else:
                food_items.put_nowait(food_item)
        except Exception as e:
            pass


def cooks_multitasking_process(cook, food_items):
    for i in range(cook['proficiency']):
        hand_thread = threading.Thread(target=cooking_process, args=(cook, food_items,), daemon=True, name=f'{cook["name"]}-Task {i}')
        hand_thread.start()


def run_kitchen():
    main_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False),
                                   daemon=True)
    main_thread.start()
    print("Kitchen is running!")

    for _, cook in enumerate(Cooks):
        cook_thread = threading.Thread(target=cooks_multitasking_process, args=(cook, Ordered_items,), daemon=True)
        cook_thread.start()

    while True:
        pass


if __name__ == '__main__':
    run_kitchen()
