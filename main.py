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

    # Scraping tweets
    lowe_tweets = gtfu.get_tweets_for_user('ZachLowe_NBA', api)

    # Find URLs of Zach's articles
    zl_articles = []
    for tweet in lowe_tweets:
        for url in tweet.entities['urls']:
            link = url['expanded_url']
            if "espn.com" in link and "story" in link:
                zl_articles.append(link)
    # Return the uniq article links
    return list(set(zl_articles))

if __name__ == "__main__":
    main()
