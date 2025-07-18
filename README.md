# Twitter Sentiment Analysis

Sentiment Analysis is the process of ‘computationally’ determining whether a piece of writing is positive, negative or neutral. 
It’s also known as opinion mining, deriving the opinion or attitude of a speaker.

This project develops a sentiment analysis tool leveraging **Tweepy** to programmatically extract tweets on a given topic. It then utilizes **TextBlob** to process the textual data and classify each tweet's sentiment as positive, negative, or neutral.

### How TextBlob Works:

TextBlob employs a **Naive Bayes classifier**, pre-trained on a dataset of movie reviews, to analyze new text. It determines the polarity of the input by calculating probabilities for positive and negative classifications.
