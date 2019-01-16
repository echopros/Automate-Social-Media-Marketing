#Author: Soumya Jagdev
#Date: 01/08/19
#Python3

import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import sys
from bs4 import BeautifulSoup
import urllib.request
from InstagramAPI import InstagramAPI
#How frequently should I check
sleep = 10
#CHANGE EMAIL ID
fbID = 'Foo'
#CHANGE PASSWORD
fbPswd = 'Bar'
#CHANGE INSTA ID
instaID = 'Foo'
#CHANGE INSTA PASSWORD
instaPswd = 'Bar'
#fbPages to post on
fbPages = ['']
#hashtags to enter on insta
hashtag = "#automation #script "
#link of the blog
blog = "http://www.reviewkopcha.com/"
#link of the current top post
current_link = ""
#future top post link
topPostLink = ""
#title with HTML
soupTitle = ""
#the title
title = ""
def new_post():
	global blog
    global topPostLink
    global current_link
    html = requests.get(blog)
    soup = BeautifulSoup(html.content, 'html.parser')
    #get top post link
    topPostLink = soup.find(class_="post-title entry-title").find('a').get('href')
    if (topPostLink != current_link):
        current_link = topPostLink
        return True
    else:
        return False

def page_info():
    global title
    global soupTitle
    global topPostLink

    #Getting post title
    html = requests.get(topPostLink)
    soupTitle = BeautifulSoup(html.content, 'html.parser')
    title = soupTitle.find(class_="post-title entry-title").string

def instagram_post():
    global soupTitle
    # Get image link    
    link = soupTitle.findAll('img')[4]["src"]
    # Download image
    urllib.request.urlretrieve(link, "1.jpg")
    #CHANGE PATH
    photo_path = '/home/pi/Desktop/1.jpg'
    time.sleep(2)
    # Caption of insta post
    caption = title + "Link in bio!\nreviewkopcha.com\n\n" + hashtag
    InstagramAPI = InstagramAPI(instaID, instaPswd)
    InstagramAPI.login() 
    InstagramAPI.uploadPhoto(photo_path, caption=caption)
    time.sleep(2)
    os.remove(photo_path)

def fb_post():
    global title
    global topPostLink
    global fbID
    global fbPswd
    #message to be printed
    message = title + "\nCheck it out at " + topPostLink

    # Creating the WebDriver object using the ChromeDriver
    driver = webdriver.Chrome()

    # Directing the driver to the defined url
    driver.get('http://www.facebook.com/')

    #email
    email = driver.find_element_by_name("email")
    email.send_keys(fbID)

    #password
    password = driver.find_element_by_name("pass")
    password.send_keys(fbPswd)

    password.submit()

    for site in fbPages:
        driver.get(site)
        time.sleep(3)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        post_box=driver.find_element_by_xpath("//*[@name='xhpc_message_text']")
        post_box.send_keys(message + " ")
        time.sleep(5)
        driver.find_element_by_xpath("//button[contains(.,'Post')]").click()
        time.sleep(5)

    driver.quit()

#getting the top link    
def first_run():
	global blog
    global topPostLink
    global current_link
    html = requests.get(blog)
    soup = BeautifulSoup(html.content, 'html.parser')
    current_link = soup.find(class_="post-title entry-title").find('a').get('href')
    topPostLink = current_link

first_run()
while True:
    if (new_post() == True):
        print ("Began Posting")
        page_info()
        instagram_post()
        fb_post()
        print("Posting ended")
    else:
        print ("Sleeping for " + str(sleep) + " mins")  
        time.sleep(sleep * 60)