
import requests

from ..config import OWM_KEY
from .plain_controller import PlainController
from .utils import sendMsg


owm_url = 'https://api.openweathermap.org/data/2.5/weather'


class WeatherContoller(PlainController):

    @classmethod
    def process(cls, chat_id, msg_text):
        data = msg_text.split(" ")

        city = data[0] if len(data) > 0 else "Riga"
        country = data[1] if len(data) > 1 else ""

        url = f"{owm_url}?q={city},{country}&appid={OWM_KEY}&units=metric"
        resp_json = requests.get(url).json()
        code = resp_json['cod']
        if code == 200:
            temp = resp_json['main']['temp']
            temp_min = resp_json['main']['temp_min']
            temp_max = resp_json['main']['temp_max']
            feels_like = resp_json['main']['feels_like']
            sky = resp_json['weather'][0]['description']
            msg_text = f"Weather for {city}\nTemp {temp}\nMin temp {temp_min}\nMax temp {temp_max}\nFeels like {feels_like}\n{sky}"
        else:
            msg_text = "City not found"
        resp = sendMsg({'chat_id': chat_id, 'text': msg_text})
        return resp.text


