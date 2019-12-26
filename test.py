import requests
from bs4 import BeautifulSoup
from decouple import config
# 외부에서 token을 변수화 해서 저장한 값을 불러와서 사용
token = config('TELEGRAM_BOT_TOKEN')

# url : f'https://api.telegram.org/bot{token}/{사용할METHOD명}
url = f'https://api.telegram.org/bot{token}/getUpdates'

# .json(): json > dict 타입으로 변환
# res = requests.get(url).json()

# result 0번째에서 userid를 조회
# user_id=res['result'][0]['message']['from']['id']

# 프롬프트를 통해 input값을 받기 위함
# user_input = input("보낼 메세지를 입력해주세요: ")

#sendMessage Method 사용
# send_url = f'https://api.telegram.org/bot{token}/sendMessage?text={user_input}&chat_id={user_id}'

# requests.get(send_url)


airkorea_api_key = config('AIRKOREA_OPEN_API')

stationName='관악구'
airkorea_api_url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?&dataTerm=daily&ver=1.3'
request_url = f'{airkorea_api_url}&ServiceKey={airkorea_api_key}&stationName={stationName}'

res = requests.get(request_url).text
soup = BeautifulSoup(res, 'xml')
#print(soup.find('item'))
dust_info=soup.find('item')
print(dust_info.dataTime.text)
print(dust_info.pm10Value.text)
print(type(dust_info.pm10Value.text))

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

print(return_data)
