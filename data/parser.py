import requests
from bs4 import BeautifulSoup


def news_parser1() -> dict:
    page = requests.get("https://www.ecoindustry.ru/news.html")
    soup = BeautifulSoup(page.text, "html.parser")
    all_news = soup.findAll("a", class_="list-item__title color-font-hover-only", href=True)
    sl = {}
    for data in all_news:
        name_of_new, link = data.text, data["href"]
        one_time_page = requests.get(link)
        one_time_soup = BeautifulSoup(one_time_page.text, "html.parser")
        one_time_parser = one_time_soup.findAll("div", class_="article__text")
        text = ""
        for one_time_data in one_time_parser:
            text += one_time_data.text + " "
        sl[data.text] = text
    return sl


def news_parser() -> dict:
    page = requests.get("https://www.ecoindustry.ru/news.html")
    soup = BeautifulSoup(page.text, "html.parser")
    all_news = soup.findAll("a", class_="", href=True)
    for data in all_news:
        try:
            name_of_new, link = data.text, data["href"]
            one_time_page = requests.get(link)
            one_time_soup = BeautifulSoup(one_time_page.text, "html.parser")
            one_time_parser = one_time_soup.findAll("p", class_="")
        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.InvalidSchema:
            pass

