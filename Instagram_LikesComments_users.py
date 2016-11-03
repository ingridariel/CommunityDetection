'''
Created on May 24, 2016

@author: Ingrid Nascimento

For infos about Instagram's data extraction regulation, see: https://www.instagram.com/developer/libraries/

'''
import urllib
import json
import csv
import sys
import time
from instagram.bind import InstagramAPIError

media_list=[]

"""Likes data from posts"""

with open("instagram_media.csv") as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:    
        f=(row['id'])
        media_id=str(f)
        print media_id

        request_url = '''
                        https://api.instagram.com/v1/media/%s/likes?access_token=XXXXX
                    '''%(media_id)
        data = json.load(urllib.urlopen(request_url))
        likes_data=data['data']
        
        try:
            for likes in likes_data:
            
                usern=(unicode(likes['username']).encode("utf-8"))
            
                id1=likes['id']
            
                fn=(unicode(likes['full_name']).encode("utf-8"))
            
                ln=likes['profile_picture']
                      
                media_list.append([id1,usern,fn,ln])
            
                with open("likes_media.csv", "a") as fp:
                    csv_writer = csv.writer(fp)
                    csv_writer.writerows(media_list)   
                    media_list=[]
 
        except InstagramAPIError as e:
            if(e.status_code==429):
                print "The maximum number of requests per hour has been exceeded."
                time.sleep(60 * 60 + 15)
                continue
print  "done"           
#-----------------------------------------------------------------------------------------------------------
"""Comments data from posts"""

with open("instagram_media.csv") as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:    
        
        f=(row['id'])
        media_id=str(f)

        request_url = '''
                        https://api.instagram.com/v1/media/%s/comments?access_token=XXXX
                    '''%(media_id)
        
        data = json.load(urllib.urlopen(request_url))
        comments_data=data['data']
        
        for comments in comments_data:
            
            time=comments['created_time']
            text=(unicode(comments['text']).encode("utf-8"))
            usern=(unicode(comments['from']['username']).encode("utf-8"))
            pp=comments['from']['profile_picture']
            id1=comments['from']['id']
            fn=(unicode(comments['from']['full_name']).encode("utf-8"))
            
            media_list.append([id1,usern,fn,time,pp,text])
            
            with open("comments_media.csv", "a") as fp:
                csv_writer = csv.writer(fp)
                csv_writer.writerows(media_list)   
                media_list=[]
 

print  "done"           
