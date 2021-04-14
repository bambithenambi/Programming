# Find New Videos on Tiktok Script

### REQUIREMENTS
- Windows 10
- [Google Chrome](https://www.google.com/chrome/)
- [Python 3.8+](https://docs.python.org/release/3.9.2/using/windows.html)
- [Anaconda 2020.11+](https://docs.anaconda.com/anaconda/install/windows/)
- [TikTokApi](https://github.com/davidteather/TikTok-Api)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

### DESCRIPTION
Script takes two text files (**tiktoks.txt** and **vscos.txt**) with 1 username on each line and finds:
- 5 most recent videos for each TikTok
- 14 most recent images for each VSCO
**WARNING! Both text files must exist with at least one username in each**

On the first run:
- Videos are saved to a CSV (**persistent.csv**).
- Images are saved to CSV (**images.csv**)

On proceeding runs, any videos or images that did not exist before are opened **Google Chrome**.
Then the both CSV files are overwritten with the new videos and photos.
