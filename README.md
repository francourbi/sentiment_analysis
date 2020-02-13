# Twitter sentiment Analysis

Sentiment Analysis is the process of ‘computationally’ determining whether a piece of writing is positive, negative or neutral. 
It’s also known as opinion mining, deriving the opinion or attitude of a speaker.

This a simple project where i use Tweepy (the python client for the official Twitter API) to get a certain amount of tweets about a particular topic, 
and then use TextBlob (python library for processing textual data) to determine the nature of the tweet (positive, negative or neutral).

### How does TextBlob works?

TextBlob has a training set with preclassified movie reviews. When you give a new text for analysis, 
it uses NaiveBayes classifier to classify the new text's polarity in pos and neg probabilities.
