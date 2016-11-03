'''
Created on May 24, 2016

@author: Ingrid Nascimento

For information about Instagram Python Library access: https://www.instagram.com/developer/libraries/
For infos about data extraction regulation, see: https://www.instagram.com/developer/libraries/

'''
from instagram.client import InstagramAPI
import csv
import sys

'''Opening connection to request recent medias'''
access_token = "XXXX"
client_secret = "XXXX"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)

recent_media, next_url = api.user_recent_media(user_id="XXX", count=20) 


media_list=[] 

"""Data from media"""

for media in recent_media:

    text=(unicode(media.caption.text).encode("utf-8")) 
    id1=media.id    
    like=media.like_count   
    comment=media.comment_count     
    time=media.created_time     
    tp=media.type  
    lc=media.link   
    
    media_list.append([id1, like, comment, time, tp,lc,text])
    
    
    with open("instagram_media.csv", "a") as fp:
        csv_writer = csv.writer(fp) 
        csv_writer.writerows(media_list)   
        media_list=[]   
