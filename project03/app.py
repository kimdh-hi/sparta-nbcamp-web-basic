from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('15.164.211.216', 27017, username="test", password="test")
db = client.dbsparta_plus_week3


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/map')
def testmap():
    return render_template('prac_map.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)