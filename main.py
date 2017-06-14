#!/usr/bin/python

import pickle
import tweepy as tw
# Custom libraries
import get_tweets_for_user as gtfu
import get_tags_for_link as gtfl

def main():
    # Import the predefined credentials dictionary
    creds = pickle.load(open("creds.pickle"))
    auth = tw.OAuthHandler(creds['consumer_key'], creds['consumer_secret'])
    auth.set_access_token(creds['access_token'], creds['access_secret'])
    api = tw.API(auth)

    # Scraping tweets
    lowe_tweets = gtfu.get_tweets_for_user('ZachLowe_NBA', api)

    # Find URLs of Zach's articles
    zl_links = {}
    for tweet in lowe_tweets:
        for url in tweet.entities['urls']:
            link = url['expanded_url']
            if "espn.com" in link and "story" in link:
                # If this link isn't in the dict, add it and its date
                if link not in zl_links:
                    # Store the link and date in the dict
                    zl_links[link] = tweet.created_at

    zl_articles = []
    for link in zl_links:
        tags = gtfl.get_tags_for_link(link, ['og:title', 'og:description'])
        title = tags['og:title']
        desc = tags['og:description']
        zl_articles.append((title, desc, link))

    # Return the articles
    return zl_articles

if __name__ == "__main__":
    main()
