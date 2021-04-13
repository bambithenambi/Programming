from TikTokApi import TikTokApi
from datetime import datetime
import pandas as pd
import json
import os.path
import webbrowser
import threading
#Initialize API instance
api = TikTokApi.get_instance()
#Open file of users
f = open("users.txt", "r")
#Add users to list, line by line
userlist = list()
for line in f:
    userlist.append(line.rstrip())
#print(userlist)
f.close()

#create new DF
df = pd.DataFrame()
#create id and user list for collection
ids = list()
times = list()
#iterate through all users and all videos, adding data to lists
def extract(users):
    for username in users:
        print("Sending Request for @"+username)
        user_videos = api.get_user(username, count=10)
        print("Request Reccieved")
        for video in user_videos["items"]:
            ids.append("https://www.tiktok.com/@"+username+"/video/"+video["id"])
            times.append(datetime.fromtimestamp(video["createTime"]))
#Use two threads to halve time for requests
threads = []
length = len(userlist)
middle_index = length//2
process1 = threading.Thread(target=extract, args=[userlist[:middle_index]])
process1.start()
threads.append(process1)
process2 = threading.Thread(target=extract, args=[userlist[middle_index:]])
process2.start()
threads.append(process2)
for process in threads:
    process.join()

#add lists to DF
df['Video'] = ids
df['Time'] = times

#Format DF and display
pd.set_option('display.max_colwidth', 1)
pd.set_option('display.max_rows', None)
df = df.sort_values(by='Time',ascending=False)


if not os.path.exists('persistent.csv'):
    df.to_csv('persistent.csv')
    print("Initialized")
else:
    print('Found previous videos')
    webbrowser.register('chrome',
	None,
	webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
    previous = pd.read_csv('persistent.csv')
    newVids = df['Video'].tolist()
    prevVids = previous['Video'].tolist()
    for video in newVids:
        if video not in prevVids:
            webbrowser.get('chrome').open(video)
    df.to_csv('persistent.csv')
