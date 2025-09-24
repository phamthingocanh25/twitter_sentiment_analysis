import numpy as np
import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
from .utils import process_tweet # Giả sử utils.py cùng thư mục

def extract_features_6(tweet, freqs):
    # process_tweet để lấy pos/neg frequencies
    word_l = process_tweet(tweet)
    x = np.zeros(7)
    
    # Feature 0: Bias
    x[0] = 1

    # Feature 1 & 2: Positive và Negative Frequencies
    for word in word_l:
        x[1] += freqs.get((word, 1.0), 0)
        x[2] += freqs.get((word, 0.0), 0)

    # Tokenize tweet gốc để tính các feature khác
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)

    # Feature 3: 'no' count (tính trên tweet gốc)
    x[3] = tweet_tokens.count('no')

    # Feature 4: Pronoun count (tính trên tweet gốc)
    pronouns = ["i", "me", "my", "mine", "we", "us", "our", "ours", "you", "your", "yours", 
                "he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"]
    x[4] = sum(1 for word in tweet_tokens if word in pronouns)

    # Feature 5: '!' count (tính trên tweet gốc)
    x[5] = tweet.count('!')

    # Feature 6: Log word count (tính trên tweet gốc)
    word_count = len(tweet.split())
    x[6] = np.log(word_count) if word_count > 0 else 0

    x = x.reshape(1, -1)
    
    return x
