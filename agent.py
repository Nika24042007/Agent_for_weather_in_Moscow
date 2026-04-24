from openai import OpenAI
import os
from tools import tools
from dotenv import load_dotenv
import requests

load_dotenv()
weather_key = os.getenv("WEATHER_API_KEY")
base_url = os.getenv("BASE_URL")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url= base_url)

def get_weather_in_Moscow() -> str:
    lat, lon = (55.751244, 37.618423)
    yandex_url = os.getenv("YANDEX_URL")
    url = yandex_url
    headers = {"X-Yandex-API-Key": weather_key}
    params = {"lat": lat, "lon": lon, "limit": 1, "lang": "ru_RU"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        fact = data['fact']
        temp = fact['temp']
        feels_like = fact['feels_like']
        condition = fact['condition']
        wind_speed = fact['wind_speed']
        pressure_mm = fact['pressure_mm']

        weather_conditions = {
            'clear': '☀️ ясно', 'partly-cloudy': '⛅️ малооблачно',
            'cloudy': '☁️ облачно', 'overcast': '☁️ пасмурно',
            'light-rain': '🌧 небольшой дождь', 'rain': '🌧 дождь',
            'heavy-rain': '🌧 сильный дождь', 'snow': '❄️ снег',
            'snow-showers': '🌨 снегопад'
        }
        condition_ru = weather_conditions.get(condition, condition)

        result = (
            f"🌡 *Температура:* {temp}°C, ощущается как {feels_like}°C\n"
            f"🌥 *Погода:* {condition_ru}\n"
            f"💨 *Ветер:* {wind_speed} м/с\n"
            f"☁️ *Давление:* {pressure_mm} мм рт. ст."
        )
        return result

    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе погоды: {str(e)}"
    except KeyError:
        return "Не удалось обработать ответ от сервера погоды."
    
    
def chat_with_agent(client_message):
    type_model = os.getenv("TYPE_MODEL")
    messages = [
        {"role": "system", "content": "Ты — полезный ассистент с доступом к инструментам. Отвечай на вопросы, используя get_weather_in_Moscow когда нужно."},
        {"role": "user", "content": client_message}
    ]

    response = client.chat.completions.create(
        model= type_model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    if tool_calls:
        messages.append(response_message)
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = eval(tool_call.function.arguments)
            
            if function_name == "get_weather_in_Moscow":
                result = get_weather_in_Moscow()
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        
        second_response = client.chat.completions.create(
            model=type_model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        final_answer = second_response.choices[0].message.content
        return final_answer
    else:
        return response_message.content
