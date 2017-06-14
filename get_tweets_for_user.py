# Credit to @yanofsky on github for most of this script
def get_tweets_for_user(user, api):
    #initialize a list to hold all the tweepy Tweets
    all_tweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=user, count=200)
    
    #save most recent tweets
    all_tweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
            #all subsequent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=user, count=200,max_id=oldest)
            
            #save most recent tweets
            all_tweets.extend(new_tweets)
            
            #update the id of the oldest tweet less one
            oldest = all_tweets[-1].id - 1
            
    #transform the tweepy tweets into a 2D array that will populate the csv
    return all_tweets

    #outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in all_tweets]
