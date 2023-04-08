import praw
import random
import os
import time
import re
import sys
import requests
from praw.models import Comment

# Reddit login/app info
userAgent = ''
cID = ''
cSC= ''
userN = ''
userP =''
reddit = praw.Reddit(user_agent=userAgent, client_id=cID, client_secret=cSC, username=userN, password=userP)

def get_random_image(subreddit_name, maxpost, nsfw):
    subreddit = reddit.subreddit(subreddit_name)
    if subreddit.over18 and nsfw!="nsfw":
        print("This subreddit can only be used in NSFW channels.")
        return
    i = 0
    postn = random.randint(0, maxpost)
    for post in subreddit.hot(limit=maxpost):
        if not post.is_self and ((subreddit.over18 and nsfw=="nsfw") or not subreddit.over18):
            if i > postn:
                if "https://imgur.com" in post.url: # not tested
                    r = requests.get(post.url)
                    soup = BeautifulSoup(r.text, 'lxml')
                    first_image_link = soup.find('a', class_='image-list-link')['href']
                    print ("".join([f"\n\"{post.title.replace('||','')}\" by u/{post.author}||", first_image_link]))
                    return
                if hasattr(post, "is_gallery"): # TODO: doesn't handle videos properly
                    image_dict = post.media_metadata
                    for image_item in image_dict.values():
                        largest_image = image_item['s']
                        image_url = largest_image['u']
                        print ("".join([f"\n\"{post.title.replace('||','')}\" by u/{post.author}||", image_url]))
                        return
                else:
                    print ("".join([f"\n\"{post.title.replace('||','')}\" by u/{post.author}||", post.url]))
                    return
                break
        if i > maxpost:
            break
        i += 1
    print("Failed to fetch image.")
    return

get_random_image(sys.argv[1], int(sys.argv[2]), sys.argv[3])
