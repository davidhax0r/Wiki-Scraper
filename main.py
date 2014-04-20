"""
Copyright 2014 Nauman Ahmad

This file is part of the Wiki Scraper library.

Wiki Scraper is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

Wiki Scraper is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Wiki Scraper.
If not, see http://www.gnu.org/licenses/.
"""

#------------------------------------------Imports-------------------------------------------------------#
import requests,time,tweepy
from bs4 import BeautifulSoup
from HTMLStripper import MLStripper
#------------------------------------------Keys---------------------------------------------------------#
#Register your app on dev.twitter.com to get the API Keys and Token, uses OAuth 2
API_KEY = "ADD YOUR KEY HERE"
API_SECRET  ="ADD API SECRET KEY HERE"

TOKEN = "ADD YOUR TOKEN HERE"
TOKEN_SECRET = "ADD YOUR TOKEN SECRET HERE"

#------------------------------------------Instances Of Tweepy Class---------------------------#

#Tweepy API wrapper setup
auth = tweepy.OAuthHandler(API_KEY ,API_SECRET)
auth.set_access_token(TOKEN,TOKEN_SECRET)

#Create an instance of the class API
twitter = tweepy.API(auth)

#------------------------------------------HTML Stripper Function--------------------------------#


def strip_tags(html):
    """
    Remove tags from HTML
    """
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#-------------------------------------------Main function---------------------------------------------#
def tweekibot():
    """
    Module to get facts from http://en.wikipedia.org/wiki/Wikipedia:On_this_day/Today
    Seperate those less than 140 characters and then tweet them
    It waits for some time and then checks the page for more information
    """

    wiki = requests.get('http://en.wikipedia.org/wiki/Wikipedia:On_this_day/Today')
    #fetches the HTML of the link
    wiki_page = wiki.text
    soup = BeautifulSoup(wiki_page)

    #Finds the elements with the <li></li> tags on the page
    list_item = soup.find_all('li')

    #creates a list of length 5 for storing the fetched info from Wikipedia
    tweet_list = ["" ,"" ,"" ,"" ,""]

    counter = 0
    for line in list_item:
        #Makes sure to only get the first 5 <li> tag items
        if counter == 5:
            break
        else:
            #Calls the strip_tags() function to clean the content from the tags
            tweet = strip_tags(str(line))
            tweet_list[counter] = tweet
        counter = counter + 1

#Checks if the length of the info is less than 140 characters
    clean_list = []
    for item in tweet_list:
        len_of_item = len(str(item))
        if len_of_item < 140:
            clean_list.append(item)

    #Returns the length of < 5 that stores the tweetable content
    return clean_list

#Call the function to get the tweetable tweets
get_content = tweekibot()

#Infinite loop for running 24/7 on the server
while True:
    #Makes sure there are items to tweet, if the list is empty the program waits for 30 hours
    if len(get_content) != 0:
        for line in get_content:
            try:
                #Calls the update_status() method to Tweet to Twitter
                twitter.update_status(str(line))
                #Waits 20 second before tweeting the next tweet
                time.sleep(20)
            except:
                print "Error, Twitter API is not responding or the Tweet has already been tweeted"
    #Waits for 30 hours before running the script, so that new content is available.
    time.sleep(42800)