#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify


class ApiServer:
    def __init__(self):
        self.api = Flask(__name__)
        self.data_received = []
        os.environ["FLASK_APP"] = "api_server.py"
        os.environ["FLASK_ENV"] = "development"

        @self.api.post("/gstat")
        def add_stat_post():
            data = request.get_data()
            if data is not None:
                self.data_received.append(data)
                print("Data Received via POST!\n{}".format(data))
                return jsonify({"status": "ok"})

        @self.api.put("/gstat")
        def add_stat_put():
            data = request.get_data()
            if data is not None:
                self.data_received.append(data)
                print("Data Received via PUT!\n{}".format(data))
                return jsonify({"status": "ok"})

        @self.api.get("/gstat")
        def get_data():
            return self.data_received


def main():
    server = ApiServer()
    server.api.run(host="localhost", port=80)


if __name__ == '__main__':
    main()
