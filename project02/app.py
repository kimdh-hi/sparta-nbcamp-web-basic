from flask import Flask, render_template, request
import requests
import xml.etree.ElementTree as et
tree = et.parse('keys.xml')
owlApiKey = tree.find('string[@name="owlbot-key"]').text

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/detail/<keyword>')
def detail(keyword):
    r = requests.get(f'https://owlbot.info/api/v4/dictionary/{keyword}', headers={"Authorization": f'Token {owlApiKey}'})
    result = r.json()
    print(result)

    return render_template("detail.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)