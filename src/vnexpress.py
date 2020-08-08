import requests
from bs4 import BeautifulSoup
import argparse


def most_viewed():
    r = requests.get("https://vnexpress.net/tin-xem-nhieu").text
    content = BeautifulSoup(r, "lxml")
    articles = content.find(
        "div", {"class": "width_common list-news-subfolder"}
    ).find_all("article")[:15]
    count = 0
    for article in articles:
        try:
            title = article.find("a")["title"]
            link = article.find("a")["href"]
            r = requests.get(link).text
            print("Title: {}\nLink: {}\n".format(title, link))
            count += 1
            if count == 10:
                break
        except TypeError:
            continue


def related_article(related=None, total=0):
    related = "+".join(related.split(" "))
    page = 1
    count = 0
    while True:
        r = requests.get(
            "https://timkiem.vnexpress.net/?q={}&cate_code=&media_type"
            "=all&latest=&fromdate=&todate=&date_format=all&page={}".format(
                related, page
            )
        ).text
        content = BeautifulSoup(r, "lxml")
        articles = content.find_all("article")
        for article in articles:
            try:
                title = article.find("a")["title"]
                link = article.find("a")["href"]
                print("Title: {}\nLink: {}\n".format(title, link))
                count += 1
                if count == total:
                    break
            except TypeError:
                continue
        page += 1
        if count == total:
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        action="store_true",
        default=False,
        dest="boolean_t",
        help="Default show top 10 articles most viewed last 24h",
    )
    parser.add_argument(
        "-m",
        action="store_false",
        default=True,
        dest="boolean_t",
        help="Search news and total of articles to show",
    )
    result = parser.parse_args()
    if result.boolean_t is True:
        most_viewed()
    elif result.boolean_t is False:
        related = str(input("Related to: ")).strip()
        total = int(input("Total articles: "))
        related_article(related, total)


if __name__ == "__main__":
    main()
