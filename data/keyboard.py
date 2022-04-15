import json
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

blue, white, green, red = VkKeyboardColor.PRIMARY, VkKeyboardColor.SECONDARY, VkKeyboardColor.POSITIVE, \
                          VkKeyboardColor.NEGATIVE

with open("data/config.json", encoding="utf-8") as json_file:
    config = json.loads(json_file.read())


def generate_keyboard_link(user_id) -> VkKeyboard:
    keyboard = VkKeyboard(inline=True)
    keyboard.add_openlink_button("🔎 Перейти на сайт", link=f"{config['my-site']}/complaint/{user_id}")
    keyboard.add_button("⁉ Мои жалобы", color=green)
    return keyboard


main_pass_keyboard = VkKeyboard(inline=True)
main_pass_keyboard.add_button("✳ Сдать батарейки", color=green)
main_pass_keyboard.add_line()
main_pass_keyboard.add_button("✳ Сдать Раздельный мусор", color=red)
main_pass_keyboard.add_line()
main_pass_keyboard.add_button("✳ Сдать стекло", color=green)
main_pass_keyboard.add_line()
main_pass_keyboard.add_button("✳ Сдать макулатуру", color=red)
main_pass_keyboard.add_line()
main_pass_keyboard.add_button("✳ Сдать металл", color=green)

main_keyboard = VkKeyboard()
main_keyboard.add_button("📜 Главное меню", color=green)

main_inline_keyboard = VkKeyboard(inline=True)
main_inline_keyboard.add_button("✳ Сдать мусор", color=blue)
main_inline_keyboard.add_button("✳ Эко - новости", color=green)
main_inline_keyboard.add_button("✳ Жалоба", color=red)

send_location = VkKeyboard(one_time=True)
send_location.add_location_button(payload=True)

list_keyboard = VkKeyboard(inline=True)
list_keyboard.add_openlink_button("РИА НОВОСТИ", link="https://ria.ru/eco/")
list_keyboard.add_line()
list_keyboard.add_openlink_button("RG.RU", link="https://rg.ru/tema/obshestvo/ekologija/")
list_keyboard.add_line()
list_keyboard.add_openlink_button("Экология производства", link="https://www.ecoindustry.ru/news.html")
list_keyboard.add_line()
list_keyboard.add_openlink_button("Экосфера", link="https://ecosphere.press/news/")
list_keyboard.add_line()
list_keyboard.add_openlink_button("ECO portal", link="https://ecoportal.su/news.html")


bad_keyboard = VkKeyboard(one_time=True)
bad_keyboard.add_location_button(payload=True)
