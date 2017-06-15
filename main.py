#!/usr/bin/python

import pickle
import tweepy as tw
import feedgen.feed as feed
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
                # Store the link and date in the dict
                # Even if it already exists, overwrite it so you get the
                # *earliest* instance of the article being tweeted
                zl_links[link] = tweet.created_at

    # Travers the links and extract title and description
    #zl_articles = []
    fg = feed.FeedGenerator()
    fg.title('Zach Lowe Feed')
    fg.id('blanklink')
    for link in zl_links:
        valid_link = True
        tags = gtfl.get_tags_for_link(link, ['og:title', 'og:description'])
        try:
            title = tags['og:title'].attrs['content']
            desc = tags['og:description'].attrs['content']
            date = zl_links[link]
            #zl_articles.append((date, title, desc, link))
        except:
            # If this isn't hacky...
            # I need to fix this later
            valid_link = False

        if valid_link:
            # Add an entry to the feed
            entry = fg.add_entry()
            entry.id(link)
            entry.title(title)
            entry.description(desc)
            entry.content(desc)
            entry.author({'name': 'Zach Lowe'})
            #entry.link(link)

    # Return the articles
    print fg.atom_str(pretty=True)
    return zl_articles

if __name__ == "__main__":
    main()
