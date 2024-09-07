from flask import Flask,jsonify
app=Flask(__name__)
@app.route("/")

def ping_server():
    return jsonify("yes we can now ping server...server is ruuning")


@app.route("/next")
def nextpage():
    return jsonify("yes this is the next page")


if __name__=="__main__":
    app.run(debug=True,port=5000)