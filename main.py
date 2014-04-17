# Developed by: Nauman Ahmad
# Twitter: twitter.com/itsnauman
# Email: nauman-ahmad@outlook.com
# Feel free to send pull requests for fixing the code
# Run it in the terminal on even Raspberry Pi!
# python main.py

#------------------------------------------Imports-------------------------------------------------------#
import requests,time,tweepy
from bs4 import BeautifulSoup
from HTMLStripper import MLStripper
#------------------------------------------Keys---------------------------------------------------------#
#Register your app on dev.twitter.com to get the API Keys and Token, uses OAuth 2
API_KEY = "pKxKEHl6hyFwQBrh0GTZV8BBn"
API_SECRET  ="sQ4xh1gZ8elA4Yq4sz8EtTlOZfT14FG3HH8RFMG8vHH9LI1XBU"

TOKEN = "2447417772-Ul4fvWF7KZ3HM5LLKmM6yv81ZXJLsQfPUcpSU7A"
TOKEN_SECRET = "I3unuCz3rlw4Jcf9f93r25SOkVXnvHf6ZggPXJVavrbCA"

#------------------------------------------Instances Of Tweepy Class---------------------------#

#Tweepy API wrapper setup
auth = tweepy.OAuthHandler(API_KEY ,API_SECRET)
auth.set_access_token(TOKEN,TOKEN_SECRET)

#Create an instance of the class API
twitter = tweepy.API(auth)

#------------------------------------------HTML Stripper Function--------------------------------#

#Function to remove all HTML tags
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#-------------------------------------------Main function---------------------------------------------#
def tweekibot():

    #Fetches the content from the Wikipedia page
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