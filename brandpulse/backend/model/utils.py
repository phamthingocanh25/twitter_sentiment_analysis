import re
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

def process_tweet(tweet):
    """
    Xử lý tweet: loại bỏ các thành phần không cần thiết, tokenize và stemming.
    Input:
        tweet: Một chuỗi (string)
    Output:
        tweets_clean: Một danh sách các từ đã được xử lý
    """
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    # Xóa các mã cổ phiếu như $GE
    tweet = re.sub(r'\$\w*', '', tweet)
    # Xóa retweet "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    # Xóa hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    # Xóa ký tự '#' nhưng giữ lại từ
    tweet = re.sub(r'#', '', tweet)
    # Tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)

    tweets_clean = []
    for word in tweet_tokens:
        if (word not in stopwords_english and
                word not in string.punctuation):
            stem_word = stemmer.stem(word)
            tweets_clean.append(stem_word)
    return tweets_clean

def extract_features6(tweet, freqs):
    '''
    Input:
        tweet: a list of words for one tweet
        freqs: a dictionary corresponding to the frequencies of each tuple (word, label)
    Output:
        x: a feature vector of dimension (1, 6)
    '''
    # process_tweet tokenizes, stems, and removes stopwords
    word_l = process_tweet(tweet)

    # 6 features
    x = np.zeros(6)

    # bias term is set to 1
    x[0] = 1

    # loop through each word in the list of words
    for word in word_l:
        # increment the word count for the positive label 1
        x[1] += freqs.get((word, 1.0), 0)

        # increment the word count for the negative label 0
        x[2] += freqs.get((word, 0.0), 0)

    # feature 3: number of positive words
    x[3] = len([word for word in word_l if (word, 1.0) in freqs])

    # feature 4: number of negative words
    x[4] = len([word for word in word_l if (word, 0.0) in freqs])

    # feature 5: log ratio
    # To avoid division by zero, add 1 to the numerator and denominator
    log_ratio = np.log((x[1] + 1) / (x[2] + 1))
    x[5] = log_ratio

    # assert(x.shape == (6,)) # This line can be removed or kept for debugging
    return x

def sigmoid(z):
    """
    Tính toán hàm sigmoid.
    """
    h = 1 / (1 + np.exp(-z))
    return h

def predict_single_tweet(tweet, freqs, theta):
    """
    Dự đoán cảm xúc cho một câu tweet sử dụng mô hình 6 features.
    """
    # Trích xuất 6 features (cộng bias)
    x = extract_features6(tweet, freqs)  # <-- THAY ĐỔI QUAN TRỌNG NHẤT LÀ Ở ĐÂY

    # Tính toán xác suất dự đoán
    y_pred_prob = sigmoid(np.dot(x, theta))

    if y_pred_prob > 0.5:
        sentiment = "Positive"
    else:
        sentiment = "Negative"

    return sentiment, float(y_pred_prob)