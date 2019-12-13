from decouple import config

# Webhook 설정을 위한 경로
token = config('TELEGRAM_BOT_TOKEN')
url = f'https://api.telegram.org/bot{token}/setWebhook'

# 내가 연결하려는 주소
# ngrok_url = 'https://8a3519ee.ngrok.io/telegram'
python_anywhere_url = 'https://ahyz0569.pythonanywhere.com/telegram'
# 실행 주소
setWebhook_url = f'{url}?url={python_anywhere_url}'

print(setWebhook_url)
