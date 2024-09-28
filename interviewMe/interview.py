from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index3.html')  # Your HTML file goes here

if __name__ == '__main__':
    app.run(debug=True)
