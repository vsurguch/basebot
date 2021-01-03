
from flask import Flask

from .src import main

def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.register_blueprint(main.bp)

    return app

if __name__ == '__main__':

    app = create_app()
    app.run()