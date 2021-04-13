### Find New Videos on Tiktok Script

#### REQUIREMENTS
- Windows 10
- [Google Chrome](https://www.google.com/chrome/)
- [Python 3.8+](https://docs.python.org/release/3.9.2/using/windows.html)
- [Anaconda 2020.11+](https://docs.anaconda.com/anaconda/install/windows/)
- [TikTokApi](https://github.com/davidteather/TikTok-Api)

#### DESCRIPTION
Script takes a text file (**users.txt**) with 1 username on each line and finds 5 most recent videos for each.

On the first run, the videos are saved to a CSV (**persistent.csv**).

On proceeding runs, the videos are compared to the previous CSV and any new videos not in the previous CSV are opened in **Google Chrome**. Then the previous CSV is overwritten with the new videos.
