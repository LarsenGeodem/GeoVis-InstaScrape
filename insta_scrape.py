import time
import re
import urllib
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome


def recent_post_links(username, post_count=10):
    """
    With the input of an account page, scrape the 10 most recent posts urls

    Args:
    username: Instagram username
    post_count: default of 10, set as many or as few as you want

    Returns:
    A list with the unique url links for the most recent posts for the provided user
    """
    url = "https://www.instagram.com/" + username + "/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = Chrome(options=chrome_options)
    browser.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < post_count:
        links = [a.get_attribute('href')
                 for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(5)
    else:
        browser.stop_client()
        return post_links[:post_count]


def recent_post_hashtags(hashtag, post_count=10):
    """
    With the input of an account page, scrape the 10 most recent posts urls

    Args:
    url: Instagram link for posts (location, hashtag)
    post_count: default of 10, set as many or as few as you want

    Returns:
    A list with the unique url links for the most recent posts for the provided user
    """
    url = "https://www.instagram.com/explore/tags/" + hashtag + "/"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = Chrome(options=chrome_options)
    browser.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < post_count:
        links = [a.get_attribute('href')
                 for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(5)
    else:
        browser.stop_client()
        return post_links[:post_count]


def find_hashtags(comment):
    """
    Find hastags used in comment and return them

    Args:
    comment: Instagram comment text

    Returns:
    a list or individual hashtags if found in comment
    """
    hashtags = re.findall('#[A-Za-z]+', comment)
    if (len(hashtags) > 1) & (len(hashtags) != 1):
        return hashtags
    elif len(hashtags) == 1:
        return hashtags[0]
    else:
        return ""


def find_mentions(comment):
    """
    Find mentions used in comment and return them

    Args:
    comment: Instagram comment text

    Returns:
    a list or individual mentions if found in comment
    """
    mentions = re.findall('@[A-Za-z]+', comment)
    if (len(mentions) > 1) & (len(mentions) != 1):
        return mentions
    elif len(mentions) == 1:
        return mentions[0]
    else:
        return ""


def findCoordinates(posturl):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = Chrome(options=chrome_options)
    browser.get(posturl)
    try:
        xpathlocation = '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[2]/div[2]/a'
        location = browser.find_element_by_xpath(xpathlocation).text
        newurl = "https://google.ca/maps/place/" + location.replace(" ", "+")
        browser.get(newurl)
        time.sleep(5)
        newurl = browser.current_url
        latlon = newurl[newurl.find("@")+1:]
        latlon = latlon[:latlon.find(",",12)]
    except:
        location = "-1"
        latlon = "-1"
    browser.stop_client()
    return location, latlon


def insta_link_details(url):
    """
    Take a post url and return post details

    Args:
    urls: a list of urls for Instagram posts 

    Returns:
    A list of dictionaries with details for each Instagram post, including link,
    post type, like/view count, age (when posted), and initial comment
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = Chrome(chrome_options=chrome_options)
    browser.get(url)

    #coordinates //  coordinates = findCoordinates(url)
    xpathlocation = '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[2]/div[2]/a'
    xpathimage = '//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div/div[2]'
    xpathimage1 = '/html/body/span/section/main/div/div/article/div[1]/div/div/div[2]'
    xpathimage2 = '/html/body/span/section/main/div/div/article/div[1]/div/div/div[1]' + '/img'
    xpathimage3 = '/html/body/span/section/main/div/div/article/div[1]/div/div'
    xpathimageOrig = '/html/body/span/section/main/div/div/article/div[1]/div/div/div[1]/div[1]/img'
    try:
        location = browser.find_element_by_xpath(xpathlocation).text
        newurl = "https://google.ca/maps/place/" + location.replace(" ", "+")
        filename = 'G:/BlogTo/' + url[28:-1] + '.jpg'
        image = browser.find_element_by_xpath(xpathimageOrig).get_attribute('src').split(' ')[0]
        urllib.request.urlretrieve(image, filename)
        print(url, 'image')
        browser.get(newurl)
        time.sleep(5)
        newurl = browser.current_url
        latlon = newurl[newurl.find("@")+1:]
        latlon = latlon[:latlon.find(",", 12)]

    except:
        location = "-1"
        latlon = "-1"
        print(url, 'empty')

    post_details = {'link': url, 'location': location, 'coordinates': latlon}
    time.sleep(5)
    return post_details

def insta_link_details_p2(url):
    """
    Take a post url and return post details

    Args:
    urls: a list of urls for Instagram posts

    Returns:
    A list of dictionaries with details for each Instagram post, including link,
    post type, like/view count, age (when posted), and initial comment
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = Chrome(chrome_options=chrome_options)
    browser.get(url)

    #coordinates //  coordinates = findCoordinates(url)
    xpathlocation = '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[2]/div[2]/a'
    try:
        location = browser.find_element_by_xpath(xpathlocation).text
        newurl = "https://google.ca/maps/place/" + location.replace(" ", "+")
        browser.get(newurl)
        time.sleep(4)
        newurl = browser.current_url
        latlon = newurl[newurl.find("@")+1:]
        latlon = latlon[:latlon.find(",", 12)]
        print(url, 'image')

    except:
        location = "-1"
        latlon = "-1"
        print(url, 'empty')

    post_details = {'link': url, 'location': location, 'coordinates': latlon}
    #time.sleep(5)
    return post_details

def insta_url_to_img(url, filename="insta.jpg"):
    """
    Getting the actual photo file from an Instagram url

    Args:
    url: Instagram direct post url
    filename: file name for image at url

    Returns:
    image file, saved locally
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = Chrome(chrome_options=chrome_options)
    browser.get(url)
    try: 
        image = browser.find_element_by_xpath(
            """/html/body/span/section/main/div/div/article/
                div[1]/div/div/div[1]/div[1]/img""").get_attribute('src').split(' ')[0]
        urllib.request.urlretrieve(image, filename)
    # If image is not a photo, print notice
    except:
        print("No image")

