import flask
import os

app = flask.Flask(__name__)

@app.route("/")
def hello_world():
    return flask.render_template("index.html")

@app.route('/data/', methods = ['POST','GET'])
def data():
    if flask.request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if flask.request.method == 'POST':
        form_data = flask.request.form
        print(form_data)
        return flask.render_template('index.html',form_data = form_data)

if __name__=="__main__":
    app.run()
