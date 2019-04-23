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
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['python'])