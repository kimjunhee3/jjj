from flask import Flask, render_template
from shorts import fetch_kbo_shorts

app = Flask(__name__)

@app.route("/")
def show_shorts():
    shorts = fetch_kbo_shorts()
    return render_template("shorts.html", shorts=shorts)

if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
