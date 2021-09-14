from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/detail/<path_val>')
def detail(path_val):
    r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
    response = r.json()
    rows = response['RealtimeCityAir']['row']

    req_word = request.args.get('word')

    return render_template("detail.html", rows=rows, req_word=req_word, path_word=path_val)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)