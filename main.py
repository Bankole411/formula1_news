import requests
from bs4 import BeautifulSoup 
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


response = requests.get('https://www.formula1.com/en/latest/all.html#default')
content = response.text
content = content.replace('â\x80\x98', "'").replace('â\x80\x99', "'").replace("â\x80\x93", "-")
soup = BeautifulSoup(content,'html.parser')
# print(soup.prettify)


article_tags = []
news_tags_index = []
news_headings = []
message_body = "\n"

all_article_captions = soup.find_all(name="div", class_="f1-cc--caption")
# print(len(all_article_tags))


for article in all_article_captions:
    article_tags.append(article.find(name="p", class_="misc--tag").getText().strip())
# print(article_tags)



for index, article in enumerate(article_tags):
    if article == 'News':
        news_tags_index.append(index)
# print(news_tags_index)



for article in all_article_captions:
    if all_article_captions.index(article) in news_tags_index:
        news_headings.append(article.find(name="p", class_="no-margin").getText())
# print(news_headings[])



for news in news_headings[:5]:
    message_body += f"➡️  {news_headings.index(news) + 1}. {news} \n"
print(message_body)




proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

account_sid = os.environ["SSID"]
auth_token = os.environ["TOKEN"]
receiver = os.environ["RECEIVER"]
sender = os.environ["SENDER"]

client = Client(account_sid, auth_token, http_client=proxy_client)

# twilio api calls will now work from behind the proxy:
message = client.messages.create(to=receiver, from_=sender, body=message_body)
