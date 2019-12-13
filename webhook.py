from decouple import config

# Webhook 설정을 위한 경로
token = config('TELEGRAM_BOT_TOKEN')
url = f'https://api.telegram.org/bot{token}/setWebhook'

#내가 연결하려는 주소
ngrok_url = 'https://8a3519ee.ngrok.io/telegram'

# 실행 주소
setWebhook_url = f'{url}?url={ngrok_url}'

print(setWebhook_url)