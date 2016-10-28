'''
Created on Feb 27, 2016

@author: ingrid
'''
#import requests
import facebook
from collections import Counter
import urllib
import json
import csv

def retrieve_posts_json(fanpage, oauth_access_token, max_number, since, until, by_number=False, by_range=True):
    # since=2016-01-18&until=2016-01-19&limit=100
    request_url = '''
                     https://graph.facebook.com/%s/posts?summary=1&filter=stream&fields=likes.summary(true),comments.summary(true),shares,message,from,icon&since=%s&until=%s&limit=100
                     &access_token=%s
                  ''' % (fanpage, since, until, oauth_access_token)

    posts_count = 0
    posts_data = []
    comments_data=[]
    likes_data=[]
    likes_list_ids=[]
    comments_list=[]
    comments_list_ids=[] 
    c_ids=[]
    l_ids=[]
    
    if by_range:
        if max_number==0:
            while True:
                data = json.load(urllib.urlopen(request_url))
                
                try:
                    posts_data = data['data']
                    
                except KeyError:
                    raise KeyError("Your access_token is probably invalid or has expired.")
                
    
                for comments_data in posts_data:
                
                    comments_list=comments_data["comments"]
                
                    for comments_list_ids in comments_list["data"]:
                        c_ids.append(comments_list_ids["from"]["id"])
                
                for likes_id in posts_data:
        
                    likes_data=likes_id["likes"]
                
                    for likes_list_ids in likes_data["data"]:
                        l_ids.append(likes_list_ids["id"])
                
                posts_count += len(data['data'])
                
                if (posts_count % 100)==0:
                    print "%d posts retrieved." % posts_count
            
                try: 
                    request_url = data['paging']['next']

                except KeyError:
                    print "End of pages for posts."
                    break
            
            create_csv(c_ids,l_ids)   
    else:
        print "end"

def create_csv(clist,llist):
    
    ckeyList=[]
    keyList=[]
    id1_value=[]
    l_value=[]
    c_value=[]
    cl_list=[]
    
    c1=Counter(clist)
    ckeyList=c1.keys()
        
       
    c2=Counter(llist)
    keyList=c2.keys()

    for i in range(0,len(ckeyList)):
        id1=str(ckeyList[i])
        
        if id1 in keyList:
            id1_value.append(id1)
            l_value.append(c2.get(id1))
            c_value.append(c1.get(id1))
        
        else:
            id1_value.append(id1)
            l_value.append(0)
            c_value.append(c1.get(id1))
    
    cl_list=zip(id1_value,l_value,c_value)
    
    with open("users_2015.csv", "wb") as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerows(cl_list)   

def main():
    
    fanpage = 'UFPAOficial'
    oauth_access_token = 'XXXX'
    
    retrieve_posts_json(fanpage, oauth_access_token, 0, '2015-01-01', '2015-01-31', by_number=False, by_range=True)

    #data = retrieve_posts(fanpage, oauth_access_token, 10)

    #save_data(data)

if __name__ == '__main__':
    main()
    

    
