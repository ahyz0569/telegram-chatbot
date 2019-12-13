from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    # name을 받으면 name을, name이 없으면 default값으로 World를 전달
    # root?name="AAA": Hello, AAA! 가 출력됨
    name = request.args.get("name", "World")
    # escape처리
    return f'Hello, {escape(name)}!'

# python app.py 로 실행
if __name__ == '__main__':
    app.run(debug=True)