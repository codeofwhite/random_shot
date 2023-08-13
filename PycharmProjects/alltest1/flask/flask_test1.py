from flask import Flask

app = Flask(__name__)


@app.route("/", methods=['POST'])
def home():
    return '<h1>hello world bae</h1>'


app.run(host='0.0.0.0')
