import numpy as np
import math
from .utils import process_tweet

FIRST_SECOND_PRONOUNS = {
    "i", "me", "my", "mine", "we", "us", "our", "ours",
    "you", "your", "yours", "u", "ya"
}

def extract_features_6(tweet, freqs):
    """
    Input:
        tweet: a string containing a tweet
        freqs: a dictionary mapping (word, sentiment) to frequency
    Output:
        x: a feature vector of dimension (1, 7)
    """
    # process_tweet tokenizes, stems, and removes stopwords
    word_l = process_tweet(tweet)
    wc = len(word_l)

    # 1 x 7 vector
    x = np.zeros((1, 7))

    # bias term is set to 1
    x[0,0] = 1

    # x1: count(positive lexicon words in doc)
    # x2: count(negative lexicon words in doc)
    pos_sum = 0.0
    neg_sum = 0.0
    for word in word_l:
        pos_sum += freqs.get((word, 1.0), 0)
        neg_sum += freqs.get((word, 0.0), 0)
    x[0,1] = pos_sum
    x[0,2] = neg_sum

    # x3: 1 if "no" appears, else 0
    x[0,3] = 1.0 if "no" in word_l else 0.0

    # x4: count of 1st & 2nd person pronouns
    x[0,4] = sum(1 for w in word_l if w in FIRST_SECOND_PRONOUNS)

    # x5: 1 if "!" appears, else 0
    x[0,5] = 1.0 if ("!" in (tweet or "")) else 0.0

    # x6: log(word_count) of the document
    x[0,6] = math.log(max(1, wc))

    assert(x.shape == (1, 7))
    return x