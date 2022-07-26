# Enter a list of VSCO usernames and download their 14 latest pictures
# Made using selenium and requests

import re, json, requests
from selenium import webdriver


PATH = "/Users/Soccerboy_Krish/Documents/chromedriver"
driver = webdriver.Chrome(PATH)


def vsco_extract(usernames):
    for username in usernames:
        url = "https://vsco.co/" + username + "/gallery"
        response = requests.get(url).text
        counter = 1
        data = json.loads(re.search(r'window\.__PRELOADED_STATE__ = (\{.*\})', response).group(1))
        links = []
        for image in data['entities']['images'].values():
            links.append(image['permalink'])

        for link in links:
            driver.get(link)
            driver.save_screenshot(username + str(counter) + ".png")
            counter += 1

# enter as many profiles as you want
# vsco_extract(["krishrastogi", "chrysc", ""])