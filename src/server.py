from flask import Flask
from flask import request
import json

from src.text_completer import TextCompleter

app = Flask(__name__)

tc = TextCompleter()


@app.route("/", methods=["GET"])
def index():
    with open("src/index.html", "r") as htmlFile:
        data = htmlFile.read()
    return data


@app.route("/api/conditional_sample", methods=["POST"])
def api_unconditional_sample():
    data = request.form
    if "input_text" in data and type(data["input_text"]) == str and data["input_text"]:
        result = tc.complete(data["input_text"])
        response = {
            "status": "Successful",
            "result": result
        }
        return json.dumps(response)
    return json.dumps({
        "status": "Failed",
        "result": "Failed."
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

