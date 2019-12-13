import requests
from decouple import config
# 외부에서 token을 변수화 해서 저장한 값을 불러와서 사용
token = config('TELEGRAM_BOT_TOKEN')

token = '1016852222:AAGCGCJAtwiVqbtoU8DeefaHcz4gfONmDYk'

# url : f'https://api.telegram.org/bot{token}/{사용할METHOD명}
url = f'https://api.telegram.org/bot{token}/getUpdates'

# .json(): json > dict 타입으로 변환
res = requests.get(url).json()

# result 0번째에서 userid를 조회
user_id=res['result'][0]['message']['from']['id']

# 프롬프트를 통해 input값을 받기 위함
user_input = input("보낼 메세지를 입력해주세요: ")

#sendMessage Method 사용
send_url = f'https://api.telegram.org/bot{token}/sendMessage?text={user_input}&chat_id={user_id}'

# 
requests.get(send_url)