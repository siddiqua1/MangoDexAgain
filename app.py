from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    print("test")
    return "hello wrld"

@app.route('/hello')
def potato():
    return "hello wrld"


app.run(debug=True)