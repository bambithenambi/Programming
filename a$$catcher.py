from TikTokApi import TikTokApi
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import json
import os.path
import webbrowser
import threading
import requests
#Initialize API instance
api = TikTokApi.get_instance()

#Open file of tiktoks and vscos
#Add users from each to lists, line by line
t = open("tiktoks.txt", "r")
tiktoks = list()
for line in t:
    tiktoks.append(line.rstrip())
t.close()
v = open("vscos.txt", "r")
vscos = list()
for line in v:
    vscos.append(line.rstrip())
v.close()

#create new DF
tiktokDF = pd.DataFrame()
vscoDF = pd.DataFrame()

#create id and user list for collection from tiktok
ids = list()
times = list()

#create image list for collection from vsco
imgs = list()

#iterate through all users and all videos, adding data to lists for tiktok
def tiktokExtract(users):
    for username in users:
        print("Sending Request for TikTok@"+username)
        user_videos = api.get_user(username, count=10)
        print("Request Reccieved")
        for video in user_videos["items"]:
            ids.append("https://www.tiktok.com/@"+username+"/video/"+video["id"])
            times.append(datetime.fromtimestamp(video["createTime"]))

#iterate through all vscos and all images. adding data to lists for vsco
def vscoExtract(users):
    for username in users:
        url = "https://vsco.co/"+username+"/gallery"
        print("Sending Request for VSCO@"+username)
        source = requests.get(url)
        print("Request Reccieved")
        soup = BeautifulSoup(source.text, 'html.parser')
        temp0 = str(soup.find_all('script')[2].encode('utf-8'))
        temp1 = temp0.split(" = ", 1)[1]
        temp2 = temp1.replace("</script>", '')
        temp3 = temp2.replace("\\", '')
        finalstr = temp3.replace("'", '')
        data = json.loads(finalstr)
        for item in data["entities"]["images"]:
            imgs.append("https://vsco.co/"+username+"/media/"+item)

#Use two threads to halve time for requests
threads = []
length_tiktok = len(tiktoks)
middle_index_tiktok = length_tiktok//2
length_vsco = len(vscos)
middle_index_vsco = length_vsco//2
#tiktok processess
process1 = threading.Thread(target=tiktokExtract, args=[tiktoks[:middle_index_tiktok]])
process1.start()
threads.append(process1)
process2 = threading.Thread(target=tiktokExtract, args=[tiktoks[middle_index_tiktok:]])
process2.start()
threads.append(process2)
#vsco processess
process3 = threading.Thread(target=vscoExtract, args=[vscos[:middle_index_vsco]])
process3.start()
threads.append(process3)
process4 = threading.Thread(target=vscoExtract, args=[vscos[middle_index_vsco:]])
process4.start()
threads.append(process4)
#prevent rest of code from executing until task complete
for process in threads:
    process.join()

#add lists to DFs
tiktokDF['Video'] = ids
tiktokDF['Time'] = times
vscoDF['Image'] = imgs

#Format DF and display
pd.set_option('display.max_colwidth', 1)
pd.set_option('display.max_rows', None)
tiktokDF = tiktokDF.sort_values(by='Time',ascending=False)


#Initialize csv for tiktok and/or vsco
if (not os.path.exists('persistent.csv')) and (not os.path.exists('images.csv')):
    tiktokDF.to_csv('persistent.csv')
    print("Initialized tiktok and vsco")
    vscoDF.to_csv('images.csv')
    print("Initialized vsco")
elif not os.path.exists('images.csv'):
    vscoDF.to_csv('images.csv')
    print("Initialized vsco")
elif not os.path.exists('persistent.csv'):
    tiktokDF.to_csv('persistent.csv')
    print("Initialized tiktok")
else:
    print('Found previous videos and images')
    #Initialize chrome
    webbrowser.register('chrome',
	None,
	webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

    #open previous csv
    previousTiktok = pd.read_csv('persistent.csv')
    previousVsco = pd.read_csv('images.csv')

    #extract column of DF as list
    newVids = tiktokDF['Video'].tolist()
    prevVids = previousTiktok['Video'].tolist()
    newPics = vscoDF['Image'].tolist()
    prevPics = previousVsco['Image'].tolist()

    #Check if video existed before, if not open it
    for video in newVids:
        if video not in prevVids:
            webbrowser.get('chrome').open(video)

    #Check if image existed before, if not open it
    for image in newPics:
        if image not in prevPics:
            webbrowser.get('chrome').open(image)

    tiktokDF.to_csv('persistent.csv')
    vscoDF.to_csv('images.csv')
