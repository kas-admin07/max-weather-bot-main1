import json
import os
import requests
from bot.weather import get_weather_info
from bot.max_api import send_message_to_max

def handler(event, context):
    """
    Обработка webhook от MAX API
    """
    try:
        if event.get('httpMethod') != 'POST':
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'ok'})
            }
        
        # Получаем данные от MAX
        body = json.loads(event.get('body', '{}'))
        
        if 'message' not in body:
            return {'statusCode': 200, 'body': 'ok'}
        
        message = body['message']
        user_id = message.get('from', {}).get('id')
        text = message.get('text', '').strip()
        
        if not user_id or not text:
            return {'statusCode': 200, 'body': 'ok'}
        
        # Получаем информацию о погоде
        weather_info = get_weather_info(text)
        
        # Отправляем ответ через MAX API
        success = send_message_to_max(user_id, weather_info)
        
        return {
            'statusCode': 200 if success else 500,
            'body': json.dumps({'status': 'ok' if success else 'error'})
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'error', 'message': str(e)})
        }