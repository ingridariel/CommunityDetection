'''
Created on 16 de Abril de 2016

@author: Ingrid Nascimento

You need to create an application in Twitter developer plataform for access keys generation.
For more infos: https://dev.twitter.com/

For more information about tweepy library to collect data from Twitter, 
see: http://tweepy.readthedocs.io/en/v3.5.0/

'''

import tweepy 
from tweepy import OAuthHandler
from collections import Counter
import json
import sys
import csv
import time

consumer_key = 'XXXX'
consumer_secret = 'XXXX'
access_token = 'XXXX'
access_secret = 'XXXX'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

tweets_list=[]
ret_list=[]
count=0

for tweet in tweepy.Cursor(api.user_timeline,count=100, screen_name='UFPA_Oficial').items():
    
    tweets=(tweet._json)
    post_id=(tweets['id_str'])
    retweet_count=(tweets['retweet_count'])
    
    #Data from comments made in tweets
    
    if tweets['in_reply_to_user_id_str']!='None':

        text=(unicode(tweets['text']).encode("utf-8"))
        
        tweets_list.append([tweets['in_reply_to_user_id_str'],
                            text,
                            tweets['retweet_count'],
                            tweets['favorite_count'],
                            tweets['created_at']])
    
        with open("Replies_users_ids.csv", "a") as fp:
            csv_writer = csv.writer(fp)
            csv_writer.writerows(tweets_list)   
            tweets_list=[]
    
    if retweet_count>0:
        
        try:
            result=api.retweeters(post_id) #Data from retweeters
            
            for a in range(0, len(result)):
                r2=(result[a]) #Retweeter id from post
                r2=str(r2)
                ret_list.append([post_id, r2])
    
            with open("retweeters_ids.csv", "a") as fp:
                csv_writer = csv.writer(fp)
                csv_writer.writerows(ret_list)  
                ret_list=[]
        
        except tweepy.TweepError:
            print "Rate limit reached. Sleeping for 15 min"
            time.sleep(15 * 60 + 15)
            continue
        
    
    