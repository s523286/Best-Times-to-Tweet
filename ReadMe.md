# Best Times to Tweet

### Developer: Liz Conard

## Description:
This project will take timeline data using a streamlistener. The goal is to get tweets from multiple days and multiple times during the week. It will examine things like favorite_count, retweet_count, and created_at using tweepy. Once all the data is collected, it will clean the data and use an algorithm to create a Heatmap of the best times of the week to tweet. I am using the Anaconda distribution for Python.

I would like to compare it to the results given at this website:
- https://sproutsocial.com/insights/best-times-to-post-on-social-media/#twitter

## To Begin:
- Make sure to create a twitter developer account. Save the consumer and access keys in a python file within your folder.
- Create a .gitignore file and put the filename containing your access keys within this file.
- Create a scraper.py and a startup.py file and put them in your folder.
- Create a results.csv file to save your output to and place it in the same folder as everything else.
- Create a findings.ipynb file to manipulate your data in and also put it in your folder.

## Retrieving the Data:
### Contents of scraper.py
```python
from twitter_keys import consumer_key, consumer_secret, access_token, access_secret
import tweepy
import csv
import pytz
import requests
from bs4 import BeautifulSoup

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

my_tweets = api.home_timeline()

# Will set all time stamps to central time
central = pytz.timezone('US/Central')


#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        
        #if the tweet is actually a retweet
        if hasattr(status, 'retweeted_status'):
            #print that it's a retweet
            print('retweet')
            retweet = 1
            #status.retweeted_status is now the retweeted tweet
            
            #get a unique link for each tweet
            link = "https://twitter.com/" + str(status.retweeted_status.user.screen_name) + "/status/" + str(status.retweeted_status.id)
            r = requests.get(link)
            soup = BeautifulSoup(r.text, 'html5lib')
            
            #Replies
            replies = soup.find('span', {"class": "ProfileTweet-actionCount"})
            if replies is not None:
                num_replies = int(replies['data-tweet-stat-count'])
            else:
                num_replies = 0

            #Retweets
            li = soup.find('li', {"class": "js-stat-retweets"})
            if li is not None:
                retweets = li.find('a')
                num_retweets = retweets['data-tweet-stat-count']
            else:
                num_retweets = 0
        
            #Favorites
            li2 = soup.find('li', {"class": "js-stat-favorites"})
            if li2 is not None:
                favorites = li2.find('a')
                num_favorites = favorites['data-tweet-stat-count']
            else:
                num_favorites = 0
            
            #Better Date Format
            central_date = central.localize(status.retweeted_status.created_at)
            fmt = '%Y-%m-%d %H:%M:%S %Z%z'
            
            #open the results file and stores it to csvFile
            #newline deletes the extra row inbetween lines
            csvFile = open('results.csv', 'a', newline = '')
            csvWriter = csv.writer(csvFile)
            #write the information we want to a csv
            csvWriter.writerow([central_date.strftime(fmt), status.retweeted_status.user.screen_name, 
                                status.retweeted_status.user.followers_count, num_retweets, num_favorites, 
                                num_replies, status.id, retweet, link])
            csvFile.close()
        else:
            #print that it's a regular tweet
            print('tweet')
            retweet = 0
            
            #get a unique link for each tweet
            link = "https://twitter.com/" + str(status.user.screen_name) + "/status/" + str(status.id)
            r = requests.get(link)
            soup = BeautifulSoup(r.text, 'html5lib')
            
            #Replies
            replies = soup.find('span', {"class": "ProfileTweet-actionCount"})
            if replies is not None:
                num_replies = int(replies['data-tweet-stat-count'])
            else:
                num_replies = 0

            #Retweets
            li = soup.find('li', {"class": "js-stat-retweets"})
            if li is not None:
                retweets = li.find('a')
                num_retweets = retweets['data-tweet-stat-count']
            else:
                num_retweets = 0
        
            #Favorites
            li2 = soup.find('li', {"class": "js-stat-favorites"})
            if li2 is not None:
                favorites = li2.find('a')
                num_favorites = favorites['data-tweet-stat-count']
            else:
                num_favorites = 0
            
            #Better Date Format
            central_date = central.localize(status.created_at)
            fmt = '%Y-%m-%d %H:%M:%S %Z%z'
            
            #open the results file and stores it to csvFile
            #newline deletes the extra row inbetween lines
            csvFile = open('results.csv', 'a', newline = '')
            csvWriter = csv.writer(csvFile)
            #write the information we want to a csv
            csvWriter.writerow([central_date.strftime(fmt), status.user.screen_name, 
                                status.user.followers_count, num_retweets, num_favorites, num_replies, 
                                status.id, retweet, link])
            csvFile.close()
    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
    
#Comment this out when running startup.py, uncomment this when running this file
'''
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['python'])
'''
```
#### About scraper.py
- If you want column headings, this code will be ran after you run startup.py, make sure the last 4 lines of code of this file are commented out when you run startup.py. The last 4 lines are calling the streamlistener() class (which we will need when we run this file), but we do not need that when we run startup.py because we already call the streamlistener within startup.py.
- To run this scraper.py, uncomment the last 4 lines.
- We will read in the twitter api consumer keys and tokens to access my twitter developer account. If you do not have a developer account, you will need to request one before you can recreate this.
- pytz helps us convert everything to central time because twitter does not standardize time at all.
- We will then hit the streamlistener which will keep reading tweets off of twitter until you manually stop it or until it encounters an error (error code at the bottom), such as wifi disconnecting.
- The first thing we hit is an if statement to determine weather the tweet was just created, or if it was a retweet. This is because tweepy reads retweets and tweets differently. For retweets, we will add in a .retweeted_status to various functions that we call in tweepy. I have also programmed this to print whether it is a retweet or a tweet, so you can see what you are collecting as the program is running.
- The overall setup of tweets and retweets are the same. We will get a link to the tweet, use beautiful soup to get the number of replies, favorites, and retweets on the tweet, and then call the rest of the information we want from tweepy. We will write all this information, using pandas, to a csv file. 
- You can run this file as many times as you would like, and it will add the new tweets to the bottom of your csv.

### Contents of startup.py
```python
from twitter_keys import consumer_key, consumer_secret, access_token, access_secret
import tweepy
import csv
from scraper import MyStreamListener

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

my_tweets = api.home_timeline()

    
with open('results.csv',newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open('results.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['Created At', 'User Name', 'NumFollowers', 'NumRetweets', 'NumFavorites', 'NumReplies', 'statusID', 
                'retweet', 'link'])
f.close()

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['python'])

```
#### About startup.py
-When running this file, make sure the last 4 lines of scraper.py are commented out.
- Every time you run this file, it will erase everything in your csv and start over. This file is really just for starting.
- We will read in the twitter api consumer keys and tokens to access my twitter developer account. 
-This will open a csv and write the column headers. It will then call the streamlistener and read in tweets to write to the csv. 
- After you have stopped running startup.py, you will run scraper.py to collect more tweets.

## Cleaning and Using the data:
### findings.ipynb
#### Read in the .csv
```python
import pandas as pd
df = pd.read_csv("results.csv")
df
```
#### Convert the "Created At" field into a datetime data type, extract the day of the week, and map it onto a new column called "weekdays"
```python
import datetime

df1 = df.copy()

df1['Created At'] = pd.to_datetime(df1['Created At'])
value = df1['Created At']
        
def weekday(date):
    if date.weekday() == 0:
        return 'Monday'
    elif date.weekday() == 1:
        return 'Tuesday'
    elif date.weekday() == 2:
        return 'Wednesday'
    elif date.weekday() == 3:
        return 'Thursday'
    elif date.weekday() == 4:
        return 'Friday'
    elif date.weekday() == 5:
        return 'Saturday'
    else:
        return 'Sunday'

df1["weekdays"] = value.map(weekday)
df1['weekdays'].head()
```
#### Now extract the time and map it onto a new column called "time"
```python
df2 = df1.copy()

def time(date):
    time2 = date.time()
    return time2

df2["time"] = value.map(time)
df2['time'].head()
```
#### Group the times into hourly buckets and map it onto a new column called "time groups"
```python
df3 = df2.copy()

def time_groups(time):
    if time >= datetime.time(0,0) and time <= datetime.time(1,0):
        return '12AM-1AM'
    elif time >= datetime.time(1,0) and time <= datetime.time(2,0):
        return '1AM-2AM'
    elif time >= datetime.time(2,0) and time <= datetime.time(3,0):
        return '2AM-3AM'
    elif time >= datetime.time(3,0) and time <= datetime.time(4,0):
        return '3AM-4AM'
    elif time >= datetime.time(4,0) and time <= datetime.time(5,0):
        return '4AM-5AM'
    elif time >= datetime.time(5,0) and time <= datetime.time(6,0):
        return '5AM-6AM'
    elif time >= datetime.time(6,0) and time <= datetime.time(7,0):
        return '6AM-7AM'
    elif time >= datetime.time(7,0) and time <= datetime.time(8,0):
        return '7AM-8AM'
    elif time >= datetime.time(8,0) and time <= datetime.time(9,0):
        return '8AM-9AM'
    elif time >= datetime.time(9,0) and time <= datetime.time(10,0):
        return '9AM-10AM'
    elif time >= datetime.time(10,0) and time <= datetime.time(11,0):
        return '10AM-11AM'
    elif time >= datetime.time(11,0) and time <= datetime.time(12,0):
        return '11AM-12PM'
    elif time >= datetime.time(12,0) and time <= datetime.time(13,0):
        return '12PM-1PM'
    elif time >= datetime.time(13,0) and time <= datetime.time(14,0):
        return '1PM-2PM'
    elif time >= datetime.time(14,0) and time <= datetime.time(15,0):
        return '2PM-3PM'
    elif time >= datetime.time(15,0) and time <= datetime.time(16,0):
        return '3PM-4PM'
    elif time >= datetime.time(16,0) and time <= datetime.time(17,0):
        return '4PM-5PM'
    elif time >= datetime.time(17,0) and time <= datetime.time(18,0):
        return '5PM-6PM'
    elif time >= datetime.time(18,0) and time <= datetime.time(19,0):
        return '6PM-7PM'
    elif time >= datetime.time(19,0) and time <= datetime.time(20,0):
        return '7PM-8PM'
    elif time >= datetime.time(20,0) and time <= datetime.time(21,0):
        return '8PM-9PM'
    elif time >= datetime.time(21,0) and time <= datetime.time(22,0):
        return '9PM-10PM'
    elif time >= datetime.time(22,0) and time <= datetime.time(23,0):
        return '10PM-11PM'
    elif time >= datetime.time(23,0) and time <= datetime.time(23,59):
        return '11PM-12AM'
    else:
        return 'other'

df3["time groups"] = df3['time'].map(time_groups)
df3
```
#### Get the value counts of "weekdays"
```python
df3['weekdays'].value_counts()
```
#### Get the value counts of "time groups"
```python
df3['time groups'].value_counts()
```
#### Renamed "time groups" to "time_groups" for manipulation purposes later
```python
df4 = df3.copy()
df5 = df4.rename(index=str, columns={"time groups": "time_groups"})
df5
```
#### Notes Before Plotting
- In order to plot the heat map(below), I had to create a "tweet efficiency score" to determine which time of day is the best to tweet. To create this score, I first took all the tweets in a given time frame on a given day of the week. I then summed all of the retweets, favorites, and replies these tweets got, and divided it by the number of total tweets in that group.
- Because some of these numbers greatly outweighed others, I decided to group the values into buckets. If there were 0 tweets, the score was automatically 0. If the value was greater than or equal to 500, the score was 4. If the value was less than 500, but greater than or equal to 200, the score was 3. If the value was less than 200, but greater than or equal to 100, the score was 2. Anything lower than 100 made the score 1.

#### Plot the heat map
```python
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm


days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", 
                "Friday", "Saturday"]
time_frames = ["12AM-1AM", "1AM-2AM", "2AM-3AM", "3AM-4AM", "4AM-5AM", 
               "5AM-6AM", "6AM-7AM", "7AM-8AM", "8AM-9AM", "9AM-10AM",
               "10AM-11AM", "11AM-12PM", "12PM-1PM", "1PM-2PM", "2PM-3PM",
               "3PM-4PM", "4PM-5PM", "5PM-6PM", "6PM-7PM", "7PM-8PM",
               "8PM-9PM", "9PM-10PM", "10PM-11PM", "11PM-12AM"]

tweet_score = []
#try divinding by count out of the loop
def efficiency_score(df, day, times):
    array1 = []
    #for each of the time frames
    for time in times:
        #locate the day of the week and the specific time frame, pull the data
        m1 = df.loc[(df["weekdays"]== day) & (df["time_groups"]== time),
                 ["weekdays","time_groups", "NumRetweets",
                 "NumFavorites", "NumReplies"]]
        #If there are no tweets in that time frame
        if m1["time_groups"].count() == 0:
            instance_val = 0
            #lowest category
            sum1 = 0
        else:
            #Sum the retweets, replies, and favorites and divide by num of tweets
            instance_val = ((m1["NumRetweets"].sum()+ m1["NumFavorites"].sum() 
                             + m1["NumReplies"].sum())/m1["time_groups"].count())
            #putting the tweets into categorical buckets
            if instance_val >= 500:
                sum1 = 4
            elif instance_val >= 200 and instance_val < 500:
                sum1 = 3
            elif instance_val >= 100 and instance_val < 200:
                sum1 = 2
            else:
                sum1 = 1
        #array1.append(instance_val)
        array1.append(sum1)
    return array1

s_array = efficiency_score(df5, "Sunday", time_frames)
tweet_score.append(s_array)
m_array = efficiency_score(df5, "Monday", time_frames)
tweet_score.append(m_array)
t_array = efficiency_score(df5, "Tuesday", time_frames)
tweet_score.append(t_array)
w_array = efficiency_score(df5, "Wednesday", time_frames)
tweet_score.append(w_array)
th_array = efficiency_score(df5, "Thursday", time_frames)
tweet_score.append(th_array)
f_array = efficiency_score(df5, "Friday", time_frames)
tweet_score.append(f_array)
st_array = efficiency_score(df5, "Saturday", time_frames)
tweet_score.append(st_array)
print(tweet_score)

fig, ax = plt.subplots(figsize=(20,50))
#(figsize=(width,height))
im = ax.imshow(tweet_score, cmap = cm.Blues)

#get rid of grid lines
ax.grid(False)

# We want to show all ticks...
ax.set_xticks(np.arange(len(time_frames)))
ax.set_yticks(np.arange(len(days_of_week)))
# ... and label them with the respective list entries
ax.set_xticklabels(time_frames)
ax.set_yticklabels(days_of_week)

plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
         rotation_mode="anchor")

cbarlabel = "Efficiency Score"
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

ax.set_title("Best Times to Post to twitter")
fig.tight_layout()
plt.show()
```
#### Heat map result:
#### * This map will continue to be edited throughout the weekend because I do not yet have sufficient data for Friday, Saturday and Sunday. Nothing about the code will be changed, just more data collection. *
![gs1](https://github.com/44520-w19/wm-project-midterm-s523286/blob/master/heatmap.png)

#### Compare to:
![gs2](https://github.com/44520-w19/wm-project-midterm-s523286/blob/master/compare.JPG)

### Comparison:
If you compare the two images, my heat map is more sporadic. The one from the website shows more activity during the middle of the day. I think this is due to my algorithm, and how I obtained the data. First of all, I know my algorithm is not perfect, that is something I would like to work on potentially for the final project. Making it any more complicated would have taken time that I did not have. Secondly, because I used a stream listener, I had to scrape tweets whenever I was free during the day. I could not have it running all day long due to classes and other activities. If I had more time, I would try to collect data more evenly among the hours and days of the week. I still think that these are pretty good results and I would be interested to know how that website determined high activity/interaction and low activity/interaction.

### Extra ways to look at the data:
#### Count the number of tweets in each time frame during each day of the week
```python
tweet_count = []

def tweets(df, day, times):
    array1 = []
    for time in times:
        m1 = df.loc[(df["weekdays"]== day) & (df["time_groups"]== time),
                 ["weekdays","time_groups", "NumRetweets", "NumFollowers",
                 "NumFavorites", "NumReplies"]]
        instance_val = m1["time_groups"].count()
        array1.append(instance_val)
    return array1

m_count = tweets(df5, "Monday", time_frames)
print("Monday: ", m_count)
tweet_count.append(m_count)
t_count = tweets(df5, "Tuesday", time_frames)
tweet_count.append(t_count)
print("Tuesday: ", t_count)
w_count = tweets(df5, "Wednesday", time_frames)
tweet_count.append(w_count)
print("Wednesday: ", w_count)
th_count = tweets(df5, "Thursday", time_frames)
tweet_count.append(th_count)
print("Thursday: ", th_count)
f_count = tweets(df5, "Friday", time_frames)
tweet_count.append(f_count)
print("Friday: ", f_count)
st_count = tweets(df5, "Saturday", time_frames)
tweet_count.append(st_count)
print("Saturday: ", st_count)
s_count = tweets(df5, "Sunday", time_frames)
tweet_count.append(s_count)
print("Sunday: ", s_count)
```
#### Test a random score for a given date and time
```python
thurs = df5.loc[(df5["weekdays"]== "Thursday") & (df5["time_groups"]== "12PM-1PM"),
                ["weekdays","time_groups", "NumRetweets", "NumFollowers",
                 "NumFavorites", "NumReplies"]]
(thurs["NumRetweets"].sum() + thurs["NumFavorites"].sum() + thurs["NumReplies"].sum())/thurs["NumFavorites"].count()
```
