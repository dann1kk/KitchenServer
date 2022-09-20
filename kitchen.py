import queue
import threading
import time
import requests
from flask import Flask, request
from threading import Thread
from Cooks import *
from Menu import *

threads = []
Orders = queue.Queue()
Ordered_items = queue.Queue()
Orders.join()
Ordered_items.join()

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
        'priority': order['priority'],
    }
    Orders.put(received_order)
    for id in received_order['items']:
        order_item = next((item for i, item in enumerate(Menu) if item['id'] == id), None)
        if order_item is not None:
            Ordered_items.put({'order_id': order['order_id'], 'food_id': order_item['id']})


def cooking_process():
    try:
        order = Orders.get()
        number_of_foods = order['items_number']
        for _ in range(0, number_of_foods):
            time.sleep(1)
            food = Ordered_items.get()
            print(f'Food with ID:{food["food_id"]} from the order nr.{order["order_id"]} ready!\n')
            Ordered_items.task_done()
        print(f'Cook has finished the order {order["order_id"]}!\n')
        payload = dict({
            'table_id': order['table_id'],
            'order_id': order['order_id'],
            'items': order['items'],
            'priority': order['priority']
        })

        requests.post('http://dinninghall:80/distribution', json=payload, timeout=0.0000000001)
        Orders.task_done()
    except Exception as e:
        pass


class Cook(Thread):
    def __init__(self, *args, **kwargs):
        super(Cook, self).__init__(*args, **kwargs)

    def run(self):
        while True:
            time.sleep(1)
            cooking_process()


def run_kitchen():
    main_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False),
                                   daemon=True)
    main_thread.start()
    print("Kitchen is running!")

    cooks_thread = Cook()
    threads.append(cooks_thread)

    for th in threads:
        th.start()
    for th in threads:
        th.join()

    while True:
        pass


if __name__ == '__main__':
    run_kitchen()
