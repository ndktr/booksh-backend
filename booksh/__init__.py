from flask import Flask, jsonify

def make_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return jsonify({'message': 'Hello, World!'})

    return app