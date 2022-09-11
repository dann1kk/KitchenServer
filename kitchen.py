from flask import Flask
import threading

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
