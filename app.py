from flask import Flask, redirect, render_template, request, url_for
from utils import distracted_boyfriend_meme_generator

app = Flask(__name__)

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        url = distracted_boyfriend_meme_generator(user_input)
        return redirect(url_for("index", result=url))

    result = request.args.get("result", None)
    return render_template("index.html", result=result)
