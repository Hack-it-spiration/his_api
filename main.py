import os

from src.app import create_app

app = create_app(os.getenv("FLASK_CONFIG") or "default")


@app.route("/")
def probe():

    return "hello"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
