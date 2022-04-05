import json
import random
from vk_api import VkApi
from data.keyboard import *
from data.db_handler import LocationsDb
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll, VkEventType


def select_best_location(lat1: float, lon1: float, array: list):
    new_array = []
    for name, lat, lon, address in array:
        new_array.append([(abs(lat1 - lat) + abs(lon1 - lon)) / 2, name, address])
    return sorted(new_array)[0]


class VkHandler:
    def __init__(self):
        with open("data/config.json", "r") as config_file:
            self.config = json.loads(config_file.read())
        with open("data/quotes.txt", encoding="utf-8") as txt:
            self.quotes = txt.read().split(";\n")
        self.vk_session = VkApi(token=self.config["token"])
        self.vk = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)
        self.locate_db = LocationsDb()
        self.keyboards = {
            "Начать": main_inline_keyboard.get_keyboard(),
            "✳ Сдать батарейки": bad_keyboard.get_keyboard(),
            "✳ Сдать Раздельный мусор": bad_keyboard.get_keyboard(),
            "✳ Сдать стекло": bad_keyboard.get_keyboard(),
            "✳ Сдать макулатуру": bad_keyboard.get_keyboard(),
            "✳ Сдать металл": bad_keyboard.get_keyboard(),
            "📜 Главное меню": main_inline_keyboard.get_keyboard(),
            "✳ Сдать мусор": main_pass_keyboard.get_keyboard(),
            "✳ Эко - новости": None,
            "✳ Жалоба": None
        }
        self.messages = {
            "Начать": "Привет!\n🏚 Главное меню",
            "✳ Сдать батарейки": "📩 Отлично, осталось только поделится своим местоположением",
            "✳ Сдать Раздельный мусор": "📩 Отлично, осталось только поделится своим местоположением",
            "✳ Сдать стекло": "📩 Отлично, осталось только поделится своим местоположением",
            "✳ Сдать макулатуру": "📩 Отлично, осталось только поделится своим местоположением",
            "✳ Сдать металл": "📩 Отлично, осталось только поделится своим местоположением",
            "📜 Главное меню": "🏚 Главное меню",
            "✳ Сдать мусор": "⁉ Вот какой мусор мы вам можем помочь сдать",
            "✳ Эко - новости": "🔥 Раздел временно не работает из-за проблем с библиотеками",
            "✳ Жалоба": "Жалоба оформляется на нашем сайте: 'ссылка'"
        }
        self.functions = {
            "Начать": self.writer,
            "✳ Сдать батарейки": self.writer,
            "✳ Сдать Раздельный мусор": self.writer,
            "✳ Сдать стекло": self.writer,
            "✳ Сдать макулатуру": self.writer,
            "✳ Сдать металл": self.writer,
            "📜 Главное меню": self.writer,
            "✳ Сдать мусор": self.writer,
            "✳ Эко - новости": self.writer,
            "✳ Жалоба": self.writer
        }
        self.categories = {
            "✳ Сдать батарейки": "batteries",
            "✳ Сдать Раздельный мусор": "waist",
            "✳ Сдать стекло": "glass",
            "✳ Сдать макулатуру": "paper",
            "✳ Сдать металл": "metal",
        }

    def writer(self, user_id: str or int, message: str, keyboard: VkKeyboard or None) -> None:
        self.vk.messages.send(user_id=user_id,
                              message=message,
                              random_id=0,
                              keyboard=keyboard)

    def run(self) -> None:
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    if event.text:
                        text = event.text
                    try:
                        result = self.vk_session.method("messages.getById", {"message_ids": [event.message_id],
                                                                             "group_id": 189072320})
                        geolocation = result["items"][0]["geo"]["coordinates"]
                        lat, lon = geolocation["latitude"], geolocation["longitude"]
                        best_lat_lon, name, address = select_best_location(lat, lon,
                                                                           self.locate_db.select_category(
                                                                               self.categories.get(text)))
                        self.writer(event.user_id,
                                    f"🏠 Адрес: {address}\n🔎 Название "
                                    f"организации: {name}\nИ помни:\n{random.choice(self.quotes)}",
                                    main_keyboard.get_keyboard())
                        text = ""
                    except KeyError:
                        pass
                    try:
                        self.functions.get(text)(event.user_id, self.messages.get(text), self.keyboards.get(text))
                    except TypeError:
                        pass
