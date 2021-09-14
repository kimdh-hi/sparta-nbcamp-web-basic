from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests

import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
owlApiKey = tree.find('string[@name="owlbot-key"]').text

app = Flask(__name__)

#client = MongoClient('내AWS아이피', 27017, username="test", password="test")
client = MongoClient('localhost',27017)
db = client.dbsparta_plus_week2


@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    msg = request.args.get('msg')
    words = list(db.words.find({}, {'_id' : False}))

    return render_template("index.html", words=words, msg=msg)


@app.route('/detail/<keyword>')
def detail(keyword):

    status = request.args.get('status')
    r = requests.get(f'https://owlbot.info/api/v4/dictionary/{keyword}',
                     headers={'Authorization' : f'Token {owlApiKey}'})
    if r.status_code != 200:
        return redirect(url_for('main', msg='찾을 수 없는 단어입니다.'))
    result = r.json()

    return render_template("detail.html", word=keyword, result=result, status=status)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기

    word = request.form['word']
    definition = request.form['definition']
    doc = {
        'word':word,
        'definition':definition
    }

    db.words.insert_one(doc)

    return jsonify({'result': 'success', 'msg': f'단어 저장 - {word}'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    word = request.form['word']
    db.words.delete_one({'word':word})

    return jsonify({'result': 'success', 'msg': f'단어 삭제 - {word}'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)