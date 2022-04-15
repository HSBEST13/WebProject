import random
import requests
from vk_api import VkApi
from data.keyboard import *
from data.db_handler import Db
from data.parser import news_parser
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll, VkEventType


def select_best_location(lat1: float, lon1: float, array: list) -> list:
    new_array = []
    for name, lat, lon, address in array:
        new_array.append([(abs(lat1 - lat) + abs(lon1 - lon)) / 2, name, address])
    return sorted(new_array)[0]


class VkHandler:
    def __init__(self) -> None:
        with open("data/config.json", "r") as config_file:
            self.config = json.loads(config_file.read())
        with open("data/quotes.txt", encoding="utf-8") as txt:
            self.quotes = txt.read().split(";\n")
        self.vk_session = VkApi(token=self.config["token"])
        self.vk = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)
        self.news = news_parser()
        self.locate_db = Db()
        self.keyboards = {
            "Начать": main_inline_keyboard.get_keyboard(),
            "✳ Сдать батарейки": bad_keyboard.get_keyboard(),
            "✳ Сдать Раздельный мусор": bad_keyboard.get_keyboard(),
            "✳ Сдать стекло": bad_keyboard.get_keyboard(),
            "✳ Сдать макулатуру": bad_keyboard.get_keyboard(),
            "✳ Сдать металл": bad_keyboard.get_keyboard(),
            "📜 Главное меню": main_inline_keyboard.get_keyboard(),
            "✳ Сдать мусор": main_pass_keyboard.get_keyboard(),
            "✳ Эко - новости": list_keyboard.get_keyboard(),
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
            "✳ Эко - новости": "🔥 Подборка лучших сайтов, чтобы узнать эко - новости",
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
        }
        self.categories = {
            "✳ Сдать батарейки": "batteries",
            "✳ Сдать Раздельный мусор": "waist",
            "✳ Сдать стекло": "glass",
            "✳ Сдать макулатуру": "paper",
            "✳ Сдать металл": "metal",
        }

    def update_news(self) -> dict:
        self.news = news_parser()
        self.locate_db.init_all_users()

    def get_new_by_index(self, index: int) -> list:
        counter = 0
        for key, value in self.news.items():
            if counter == index:
                return [key, value[:3500]]
            counter += 1

    def writer(self, user_id: str or int, message: str, keyboard: VkKeyboard or None) -> None:
        self.vk.messages.send(user_id=user_id,
                              message=message,
                              random_id=random.randint(0, 2147000000),
                              keyboard=keyboard)
        self.locate_db.check_user(user_id)

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
                        if text == "✳ Жалоба":
                            self.writer(
                                event.user_id,
                                "🔥 Жалоба оформляется на нашем сайте",
                                generate_keyboard_link(user_id=event.user_id).get_keyboard()
                            )
                        elif text == "⁉ Мои жалобы":
                            response = requests.get(f"{self.config['my-site']}/"
                                                    f"api/v2/get-complaints/{event.user_id}").json()
                            for i in response["complaints"]:
                                self.writer(
                                    event.user_id,
                                    f"📩 Название жалобы: {i['name']}\n🌐 Адрес: {i['address']}",
                                    keyboard=None
                                )

