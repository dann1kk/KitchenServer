from flask import Flask
import threading

Menu = [{
    "id": 1,
    "name": "pizza",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 2,
    "name": "salad",
    "preparation-time": 10,
    "complexity": 1,
    "cooking-apparatus": None
}, {
    "id": 3,
    "name": "zeama",
    "preparation-time": 7,
    "complexity": 1,
    "cooking-apparatus": "stove"
}, {
    "id": 4,
    "name": "Scallop Sashimi with Meyer Lemon Confit",
    "preparation-time": 32,
    "complexity": 3,
    "cooking-apparatus": None

}, {
    "id": 5,
    "name": "Island Duck with Mulberry Mustard",
    "preparation-time": 35,
    "complexity": 3,
    "cooking-apparatus": "oven"
}, {
    "id": 6,
    "name": "Waffles",
    "preparation-time": 10,
    "complexity": 1,
    "cooking-apparatus": "stove"

}, {
    "id": 7,
    "name": "Aubergine",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 8,
    "name": "Lasagna",
    "preparation-time": 30,
    "complexity": 2,
    "cooking-apparatus": "oven"
}, {
    "id": 9,
    "name": "Burger",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": "stove"
}, {
    "id": 10,
    "name": "Gyros",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": None
}, {
    "id": 11,
    "name": "Kebab",
    "preparation-time": 15,
    "complexity": 1,
    "cooking-apparatus": None
}, {
    "id": 12,
    "name": "Unagi Maki",
    "preparation-time": 20,
    "complexity": 2,
    "cooking-apparatus": None
}, {
    "id": 13,
    "name": "Tobacco Chicken",
    "preparation-time": 30,
    "complexity": 2,
    "cooking-apparatus": "oven"
}]

Cooks = [{
    "id": 1,
    "rank": 3,
    "proficiency": 4,
    "name": "Jamie Oliver",
    "catch-phrase": "Can I put some olive oil in your food?"
}, {
    "id": 2,
    "rank": 2,
    "proficiency": 3,
    "name": "Gordon Ramsay",
    "catch-phrase": "You f****** donkey"
}, {
    "id": 3,
    "rank": 2,
    "proficiency": 2,
    "name": "Nusret Gökçe",
    "catch-phrase": "Salt Bae"
}, {
    "id": 4,
    "rank": 1,
    "proficiency": 2,
    "name": "Guy Fieri",
    "catch-phrase": "Nice sauce man"
    }]

app = Flask(__name__)


def run_kitchen():
    main_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False),
                                   daemon=True)
    main_thread.start()
    print("Kitchen is running!")

    while True:
        pass


if __name__ == '__main__':
    run_kitchen()
