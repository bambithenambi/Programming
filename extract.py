import re, json, requests, time
from selenium import webdriver
from bs4 import BeautifulSoup

PATH = "/Users/Soccerboy_Krish/Documents/chromedriver"
driver = webdriver.Chrome(PATH)

# Way to download VSCO images as mht (MIME HTML) using selenium and requests

def vsco_extract(username):
    url = "https://vsco.co/" + username + "/gallery"
    response = requests.get(url).text
    data = json.loads(re.search(r'window\.__PRELOADED_STATE__ = (\{.*\})', response).group(1))
    links = []
    for img in data['entities']['images'].values():
        links.append(img['permalink'])

    for link in links:
        driver.get(link)
        time.sleep(2)
        open("out.mht", "wb").write((driver.get(link)))

print(vsco_extract("krishrastogi"))

# Following code got image links using BeautifulSoup, not necessary anymore

def get_html(username):
    url = "https://vsco.co/" + username + "/gallery"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script = str(soup.find_all('script'))
    start_index = script.find("entities")
    end_index = script.find("articles", start_index)
    images = script[start_index:end_index]
    return images

get_html("krishrastogi")