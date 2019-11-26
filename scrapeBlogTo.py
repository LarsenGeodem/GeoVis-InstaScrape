import pandas as pd
import urllib.request
from collections import Counter
from insta_scrape import recent_post_links, insta_link_details, insta_url_to_img, recent_post_hashtags
import time

starttime = time.time()

#tag = "toronto" #"selfie"
username = "blogto"


print("scraping", username, "posts")
#example_urls = recent_post_hashtags(tag, post_count=1200)
example_urls = recent_post_links(username, post_count=2000)
print(example_urls.__len__(), username, "post urls found")
print(example_urls)

out_urls = pd.DataFrame(example_urls)
out_urls.head()
out_urls.to_csv('csv/' + username + '_2019_11_18_urls.csv')

example_details = [insta_link_details(url) for url in example_urls]

example_username = pd.DataFrame(example_details)
example_username.head()
example_username.to_csv('csv/' + username + '_2019_11_18.csv')
print("finished scraping", username)

endtime = time.time()
elapsed_time = endtime-starttime
print("Runtime:", round(elapsed_time/60, 2), "minutes.")
