from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

#client = MongoClient('52.79.158.100', 27017, username="test", password="test")
client = MongoClient('localhost',27017)
db = client.dbsparta_plus_week3


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/matjip', methods=["GET"])
def get_matjip():
    matjip_list = list(db.matjips.find({}, {'_id':False}))

    return jsonify({'result': 'success', 'matjip_list': matjip_list})

@app.route('/test', methods=["GET"])
def test():
    return render_template("prac_map.html")

@app.route('/like', methods=["POST"])
def like():
    print('like')
    title = request.form['title']
    address = request.form['address']
    db.matjips.update_one({'title':title, 'address':address}, {'$set':{'like':'1'}})
    return jsonify({'result':'ok'})

@app.route('/unlike', methods=["POST"])
def unlike():
    print('unlike')
    title = request.form['title']
    address = request.form['address']
    db.matjips.update_one({'title':title, 'address':address}, {'$set':{'like':'0'}})
    return jsonify({'result':'ok'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)