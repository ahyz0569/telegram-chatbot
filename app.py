from flask import Flask, escape, request, render_template
from decouple import config
from bs4 import BeautifulSoup
import requests
import random, re

app = Flask(__name__)

api_url = 'https://api.telegram.org/bot'
token = config('TELEGRAM_BOT_TOKEN')
google_key = config('GOOGLE_KEY')
open_weather_api_key = config('OPEN_WEATHER_MAP_API')
airkorea_api_key = config('AIRKOREA_OPEN_API')

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


# @app.route(f'/{token}', methods=['POST'])
@app.route('/telegram', methods=['POST'])
def telegram():
    req = request.get_json()
    # print(req)

    # user의 id와 입력한 메세지 추출
    user_id = req['message']['from']['id']
    user_input = req['message']['text']

    # user_input 값에서 찾을 문자열 패턴
    greeting = re.compile("안녕")
    pinedust_check = re.compile("미세먼지")

    # 로또 번호 추천 기능 구현
    if user_input == "로또":
        num_list = range(1, 46)
        lotto_num = random.sample(num_list, 6)

        return_data = f"오늘의 로또번호는 {lotto_num} 입니다."
    
    # 번역 기능 구현: 메세지 입력창에 "번역 안녕하세요"라고 입력하면 번역 뒤에 글자서부터 번역할 수 있게 구현
    elif user_input[0:3] == "번역 ":
        google_api_url = "https://translation.googleapis.com/language/translate/v2"
        before_text = user_input[3:]

        data = {
            'q': before_text,
            'source': 'ko',
            'target': 'en'
        }
        request_url = f'{google_api_url}?key={google_key}'

        requests.post(request_url, data)

        # 구글 번역 api에 데이터를 전달해 번역을 요청하고 그 번역값을 받아서 res에 저장
        res = requests.post(request_url, data).json()
        print (res)

        return_data = res['data']['translations'][0]['translatedText']

    # 날씨 상태와 기온 알림 기능 구현
    elif user_input == "오늘의 날씨":
        # API Call: http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID={APIKEY}
        open_weather_api_url = 'http://api.openweathermap.org/data/2.5/weather?q=Seoul'
        request_url = f'{open_weather_api_url}&APPID={open_weather_api_key}'

        res = requests.get(request_url).json()

        weather_state = res['weather'][0]['main']
        temp = float(res['main']['temp'])-273.15
        temp = round(temp, 3)

        return_data = f"오늘의 날씨는 {weather_state}이며 기온은 {temp} 도 입니다."
    
    # 미세 먼지 정보 알림 기능 구현
    # 서울시 지역구 별로 정보 조회가 가능하게끔 구현함
    elif pinedust_check(user_input) :

        # 서울시 미세먼지 측정소 정보 리스트
        seoul_gu_list = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구',
                        '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', 
                        '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']
        stationName = ''
        # '/' 를 기준으로 입력한 지역구명와 seoul_gu_list내에 있는 지역구명을 비교함
        input_station = user_input.split('/')[1]
        for gu in seoul_gu_list:
            if gu == input_station:
                stationName = gu
                break
        
        # 유저가 입력한 지역구명에 오타가 있을 경우 재입력 메세지 노출
        if stationName == '':
            return_data = '지역구명을 잘못 입력하셨습니다. 명령어를 다시 입력해주세요.'

        else:    
            # 시도별 실시간 측정정보 조회 : http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?sidoName=%EC%84%9C%EC%9A%B8&dataTerm=daily&numOfRows=40&ServiceKey={서비스키}&ver=1.3
            # 측정소별 실시간 측정정보 조회 url
            airkorea_api_url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?&dataTerm=daily&ver=1.3'
            request_url = f'{airkorea_api_url}&ServiceKey={airkorea_api_key}&stationName={stationName}'

            res = requests.get(request_url).text
            soup = BeautifulSoup(res, 'xml')
            dust_info = soup.find('item')
            
            # 요청 기준 제일 최근에 조회되는 미세먼지 정보 추출
            time = dust_info.dataTime.text
            dust = int(dust_info.pm10Value.text)
            dust_grade = dust_info.pm10Grade1h.text

            # 미세먼지등급
            if dust_grade == '1':
                grade = '좋음'
            elif dust_grade == '2':
                grade = '보통'
            elif dust_grade == '3':
                grade = '나쁨'
            else:
                grade = '매우 나쁨'
        
            return_data = f"{time} 기준 {stationName}의 미세먼지 농도는 {dust}이며 대기 상태는 {grade} 입니다."

    # 인사 기능 구현
    elif greeting.search(user_input) :
        return_data = "안녕하세요 :) 사용가능한 명령어는 '로또', '번역', '오늘의 날씨', '미세먼지' 입니다. \n" \
                    + "★ 로또: 로또번호를 추천해드립니다. \n" \
                    + "★ 번역: 번역할 문장 앞에 `번역 ` 을 입력하면 영어로 번역해드립니다. \n" \
                    + "★ 오늘의 날씨: 오늘의 날씨 상태와 기온을 알려드립니다. \n" \
                    + "★ 미세먼지: `미세먼지/(지역구명)` 로 입력하시면 해당 지역구의 실시간 미세먼지 정보를 알려드립니다."

    else:
        return_data = "사용가능한 명령어는 '로또', '번역', '오늘의 날씨' 입니다. 명령어를 다시 입력해주세요. \n" \
                    + "★ 로또: 로또번호를 추천해드립니다. \n" \
                    + "★ 번역: 번역할 문장 앞에 `번역 ` 을 입력하면 영어로 번역해드립니다. \n" \
                    + "★ 오늘의 날씨: 오늘의 날씨 상태와 기온을 알려드립니다. \n" \
                    + "★ 미세먼지: `미세먼지/(지역구명)` 로 입력하시면 해당 지역구의 실시간 미세먼지 정보를 알려드립니다."

    #sendMessage Method 사용요청
    send_url = f'https://api.telegram.org/bot{token}/sendMessage?text={return_data}&chat_id={user_id}'
    requests.get(send_url)

    # status code 200: 요청 성공을 의미
    return 'ok', 200

# python app.py 로 실행
if __name__ == '__main__':
    app.run(debug=True)