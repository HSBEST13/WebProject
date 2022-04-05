import requests
from bs4 import BeautifulSoup


def news_parser():
    page = requests.get("https://rg.ru/tema/obshestvo/ekologija/")
    soup = BeautifulSoup(page.text, "html.parser")
    all_news = soup.findAll("a", class_="b-link b-link_title", href=True)
    for data in all_news:
        name_of_new, link = data.text, data["href"]
        one_time_page = requests.get(link)
        one_time_soup = BeautifulSoup(one_time_page.text, "html.parser")
        one_time_parser = one_time_soup.findAll("div", class_="b-material-wrapper__text")
        print(one_time_parser)


news_parser()
