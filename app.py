from flask import Flask, escape, request, render_template
from decouple import config
import requests

app = Flask(__name__)

api_url = 'https://api.telegram.org/bot'
token = config('TELEGRAM_BOT_TOKEN')

@app.route('/')
def hello():
    # name을 받으면 name을, name이 없으면 default값으로 World를 전달
    # root?name="AAA": Hello, AAA! 가 출력됨
    name = request.args.get("name", "World")
    # escape처리
    return f'Hello, {escape(name)}!'

# 전송할 메세지 입력
@app.route('/write')
def write():
    return render_template('write.html')

# 메세지 전송
@app.route('/send')
def send():    

    get_user_api = f"{api_url}{token}/getUpdates"
    res = requests.get(get_user_api).json()
    # userid를 조회
    user_id=res['result'][0]['message']['from']['id']
    # write.html에서 입력한 user_input값을 받아옴
    user_input = request.args.get('user_input')

    #sendMessage Method 사용
    send_url = f'https://api.telegram.org/bot{token}/sendMessage?text={user_input}&chat_id={user_id}'
    requests.get(send_url)

    return render_template('send.html')

# python app.py 로 실행
if __name__ == '__main__':
    app.run(debug=True)