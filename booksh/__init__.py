from flask import Flask, jsonify


# TODO: typing package (& mypy) の導入
# TODO: pytestの導入
# TODO: 書籍検索APIを叩いてみる

def make_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return jsonify({'message': 'Hello, World!'})

    return app