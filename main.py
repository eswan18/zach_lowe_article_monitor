#!/usr/bin/python

import pickle, pytz
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
    gmt = pytz.timezone('GMT')
    for tweet in lowe_tweets:
        for url in tweet.entities['urls']:
            link = url['expanded_url']
            if "espn.com" in link and "story" in link:
                # Store the link and date in the dict
                # Even if it already exists, overwrite it so you get the
                # *earliest* instance of the article being tweeted
                zl_links[link] = gmt.localize(tweet.created_at)

    # Now convert the dict to a list of tuples
    zl_links = [(zl_links[link], link) for link in zl_links]
    # Sort the tuples by their first value (the date)
    zl_links = sorted(zl_links, key=lambda x: x[0], reverse=True)

    # Traverse the links and extract title and description
    fg = feed.FeedGenerator()
    fg.id('blank_id')
    fg.title('Zach Lowe Feed')
    # Iterate over the link tuples
    for link in zl_links:
        valid_link = True
        date = link[0]
        url = link[1]
        tags = gtfl.get_tags_for_link(url, ['og:title', 'og:description'])
        try:
            title = tags['og:title'].attrs['content']
            desc = tags['og:description'].attrs['content']
        except:
            # If this isn't hacky...
            # I need to fix this later
            valid_link = False

        if valid_link:
            # Add an entry to the feed
            entry = fg.add_entry()
            entry.id(url)
            entry.title(title)
            entry.description(desc)
            entry.content(desc)
            entry.updated(date)
            entry.author({'name': 'Zach Lowe'})
            entry.link({'href':url})

    print fg.atom_str(pretty=True)


if __name__ == "__main__":
    main()
