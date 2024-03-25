import ctypes
import os

from flask import Flask, request
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route("/test", methods=["GET"])
def test():
    logging.info("Test")
    response = {
        "version": "1.0.0",
        "session": "bebra",
        "response": {
            "end_session": False
        }
    }

    return json.dumps(response)


def lock_windows():
    ctypes.windll.user32.LockWorkStation()


def disable_pc():
    os.system("shutdown /s /t 1")


@app.route("/", methods=["POST"])
def main():
    logging.info(request.json)

    response = {
        "version": request.json["version"],
        "session": request.json["session"],
        "response": {
            "end_session": False
        }
    }

    req = request.json

    input_words = req["request"]["nlu"]["tokens"]

    if req["session"]["new"]:
        response["response"]["text"] = "Теперь вы можете управлять компьютером!"
    else:
        if any(ext in input_words for ext in ["заблокируй", "экран"]):
            lock_windows()
            response["response"]["text"] = "Экран заблокирован"
            response["response"]["end_session"] = True
        elif any(ext in input_words for ext in ["выключи", "выруби"]):
            disable_pc()
            response["response"]["text"] = "Выключаю компьютер"
            response["response"]["end_session"] = True
        else:
            response["response"]["text"] = "Неизвестная команда"

    return json.dumps(response)
