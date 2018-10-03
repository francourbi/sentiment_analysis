from textblob import TextBlob
from textblob import classifiers
import tweepy
import re
import csv
class TwitterClient(object):

    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = '***'
        consumer_secret = '***'
        access_token = '***'
        access_token_secret = '***'

        # attempt authentication
        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(auth)
        except:
            print("Error: Authentication Failed")

    # Return tweets dictionary with tweet text,sentiment,polarity
    def get_tweets(self,keyword,tweetCount):

        #Stores tweet text with Polarity (positive/negative)
        tweets = []
        try:
            print('Getting tweets')
            for tweet in tweepy.Cursor(self.api.search, keyword, lang="en").items(tweetCount):

                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                parsed_tweet['clean_text'] = self.clean_tweet(tweet.text)

                # clean tweet for better analysis
                analysis = TextBlob(self.clean_tweet(tweet.text))

                # saving tweet sentiment
                parsed_tweet['sentiment'] = analysis.sentiment

                #saving tweet polarity
                if analysis.sentiment.polarity > 0:
                    parsed_tweet['polarity'] = 'positive'
                elif analysis.sentiment.polarity < 0:
                    parsed_tweet['polarity'] = 'negative'
                else:
                    parsed_tweet['polarity'] = 'neutral'

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except Exception as e:
            print(e)
            return tweets

    # Utility function to clean tweet text by removing links, special characters using simple regex statements.
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

    # Utility function to print %
    def print_percentege(self, analyzed_tweets):
        positiveCount = 0
        negativeCount = 0
        neutralCount = 0
        total = 0
        for analyzed_tweet in analyzed_tweets:
            total = total + 1
            if (analyzed_tweet['polarity'] == 'positive'):
                positiveCount = positiveCount + 1
            elif (analyzed_tweet['polarity'] == 'negative'):
                negativeCount = negativeCount + 1
            else:
                neutralCount = neutralCount + 1
        if(total!= 0):
            print("Total: Positive {0}% - Negative:{1}% - Neutral:{2}%".format(positiveCount*100/total,negativeCount*100/total,neutralCount*100/total))

    # Function to create a classifier
    def naives_bayes(self, analyzed_tweets):
        training = []
        testing = []

        #Get the number of tweets that are either positive or negative
        length = 0
        for tweet in analyzed_tweets:
            if (tweet['polarity'] != 'neutral'):
                length = length + 1

        #Build training set (80%) and testing set (20%)
        training_limit = round(length * 0.8)
        index = 0
        for tweet in analyzed_tweets:
            if (tweet['polarity'] != 'neutral'):
                row = []
                row.append(tweet['clean_text'])
                row.append(tweet['polarity'])

                if(index < training_limit):
                    training.append(row)
                else:
                    testing.append(row)
                index = index + 1


        #Create classifier
        classifier = classifiers.NaiveBayesClassifier(training)
        print("Naives Bayes Classifier - accuracy:{0}".format(classifier.accuracy(testing)))
        classifier.show_informative_features(10)

    def generate_csv(self,analyzed_tweets):

        with open('Tweets.csv', 'w', encoding='utf-8') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for tweet in analyzed_tweets:
                filewriter.writerow([tweet['text'],tweet['sentiment'],tweet['polarity']])

def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # connect to twitter and get tweets
    analyzed_tweets = api.get_tweets('#Tesla',1000)
    if(len(analyzed_tweets)!= 0):
        # generate csv with tweets (just for reading reference)
        api.generate_csv(analyzed_tweets)

        #print tweets in console
        for analyzed_tweet in analyzed_tweets:
            print("Tweet text: {0} - Polarity: {1} - {2}".format(analyzed_tweet['text'], analyzed_tweet['polarity'],analyzed_tweet['sentiment']))

        #print percentege
        api.print_percentege(analyzed_tweets)

        #genete naives bayes model
        api.naives_bayes(analyzed_tweets)


if __name__ == "__main__":
    # calling main function
    main()