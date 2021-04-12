from TikTokApi import TikTokApi
from datetime import datetime
import pandas as pd
import json

api = TikTokApi.get_instance()
results = 10
username = 'washingtonpost'
user_videos = api.get_user(username)
data = json.dumps(user_videos)
#data = json.loads(data2)

df = pd.DataFrame()

ids = list()
times = list()
for video in user_videos["items"]:
    ids.append("https://www.tiktok.com/@"+username+"/video/"+video["id"])
    times.append(datetime.fromtimestamp(video["createTime"]))

df['Video'] = ids
df['Time'] = times

def make_clickable(val):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val, val)
pd.set_option('display.max_colwidth', 1)
df.style.format({'Video': make_clickable})
print(df)
