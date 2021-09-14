from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta_adv

from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():

    diaries = list(db.diary.find({}, {'_id':False}))

    return jsonify({'diaries':diaries})

@app.route('/diary', methods=['POST'])
def save_diary():
    title = request.form['title']
    content = request.form['content']

    # 파일저장
    file = request.files["file"]
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title':title,
        'content':content,
        'file':f'{filename}.{extension}'
    }

    db.diary.insert_one(doc)
    return jsonify({'msg':'저장완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)