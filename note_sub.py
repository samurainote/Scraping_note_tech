import pandas as pd
from bs4 import BeautifulSoup
import requests

Tech_articles = {}
article_no = 0

url = "https://note.mu/categories/tech"

while True:

    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    all_infos = soup.find_all("div", {"class":"feeds"})

    for all_info in all_infos:

        title = all_info.find("span", attrs={"ng-bind-html":"note.name"}).text
        user = all_info.find("span")[0].text
        date = all_info.find("span", attrs={"ng-bind":"::note.publish_at | date:'yyyy/MM/dd HH:mm'"}).text
        like_tag = all_info.find("div", attrs={"class":"renewal-p-action__count"})
        like = like_tag.text if like_tag else "N/A"
        link = all_info.find("a", attrs={"ng-if":"$ctrl.linkMethod == 'state' && !$ctrl.analytics"}).get("href")

        article_no = article_no + 1
        Tech_articles[article_no] = [title, user, date, like, link]

print("Total number of Tech articles in note", article_no)
Tech_articles_df = pd.DataFrame.from_dict(Tech_articles, orient = "index", columns = ["title", "user", "date", "like", "link"])
Tech_articles_df.to_csv("note_tech_articles.csv")
