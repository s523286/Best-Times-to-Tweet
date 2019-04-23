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

