#!/usr/bin/python

import pickle
import tweepy as tw
# Custom libraries
import get_tweets_for_user as gtfu

def main():
    # Import the predefined credentials dictionary
    creds = pickle.load(open("creds.pickle"))
    auth = tw.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_secret'])
    api = tw.API(auth)

    # Start scraping
    lowe_tweets = gtfu.get_tweets_for_user('ZachLowe_NBA', api)
    print lowe_tweets[2]

if __name__ == "__main__":
    main()
