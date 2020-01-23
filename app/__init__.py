from flask import Flask

def create_app():
    app = Flask(__name__)

    # Remove the previous code using `@app` and replace it with:
    from .main.controllers import main
    app.register_blueprint(main)

    return app
