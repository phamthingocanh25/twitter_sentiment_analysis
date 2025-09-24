# backend/model/utils.py

import re
import string
import numpy as np
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer


# <<< THAY ĐỔI: Thêm danh sách các đại từ
# Đại từ ngôi 1 & 2 (dùng cho feature x4). Viết ở lowercase vì process_tweet đã lowercase.
FIRST_SECOND_PRONOUNS = {
    "i", "me", "my", "mine", "we", "us", "our", "ours",
    "you", "your", "yours", "u", "ya"
}

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
    # <<< THAY ĐỔI: Đồng bộ hóa logic xóa hyperlink với file notebook
    tweet = re.sub(r'https?://[^\s\n\r]+', '', tweet)
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
    """
    Trích xuất 7 đặc trưng từ một tweet (6 features + 1 bias).
    """
    # Kiểm tra '!' trên raw text
    has_exclaim = ("!" in (tweet or ""))

    # Xử lý token (stem, remove stopwords...)
    word_l = process_tweet(tweet)
    wc = len(word_l)

    # Khởi tạo vector [bias + 6 features]
    x = np.zeros((1, 7))
    x[0, 0] = 1.0  # bias

    # x1, x2: tổng tần suất từ theo freqs
    pos_sum, neg_sum = 0.0, 0.0
    for w in word_l:
        pos_sum += freqs.get((w, 1.0), 0)
        neg_sum += freqs.get((w, 0.0), 0)

    # x3: có từ "no"? (sau khi đã stemming)
    has_no = 1.0 if "no" in word_l else 0.0

    # x4: đếm đại từ ngôi 1&2
    pron_count = sum(1 for w in word_l if w in FIRST_SECOND_PRONOUNS)

    # x5: có dấu '!' trong raw text?
    exclaim = 1.0 if has_exclaim else 0.0

    # x6: ln(word_count)
    ln_wc = math.log(max(1, wc))

    # Gán vào vector
    x[0, 1] = pos_sum
    x[0, 2] = neg_sum
    x[0, 3] = has_no
    x[0, 4] = pron_count
    x[0, 5] = exclaim
    x[0, 6] = ln_wc

    assert x.shape == (1, 7)
    return x

def sigmoid(z):
    """
    Tính toán hàm sigmoid.
    """
    h = 1 / (1 + np.exp(-z))
    return h

def predict_single_tweet(tweet, freqs, theta):
    """
    Dự đoán cảm xúc cho một câu tweet sử dụng mô hình 7 features (6 + bias).
    """
    # Trích xuất 7 features
    x = extract_features6(tweet, freqs)

    # Tính toán xác suất dự đoán
    y_pred_prob = sigmoid(np.dot(x, theta))

    if y_pred_prob > 0.5:
        sentiment = "Positive"
    else:
        sentiment = "Negative"

    # Trả về cảm xúc và xác suất là Positive
    return sentiment, float(y_pred_prob)

def get_word_sentiments(tweet, freqs):
    '''
    Phân tích từng từ trong tweet để xác định cảm xúc dựa trên freqs.
    Input:
        tweet: chuỗi string gốc
        freqs: từ điển tần suất
    Output:
        Một danh sách các tuple, ví dụ: [('im', 'neutral'), ('very', 'neutral'), ('happi', 'positive'), ('but', 'neutral'), ('im', 'neutral'), ('very', 'neutral'), ('sad', 'negative')]
    '''
    # Xử lý tweet để lấy danh sách từ đã được stem
    processed_words = process_tweet(tweet)
    word_sentiments = []

    # Tạo một set các từ đã xử lý để tra cứu nhanh
    processed_set = set(processed_words)

    # Tokenize tweet gốc để giữ lại các từ gốc
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    original_tokens = tokenizer.tokenize(tweet)
    stemmer = PorterStemmer()

    for token in original_tokens:
        stemmed_token = stemmer.stem(token)
        if stemmed_token in processed_set:
            pos_freq = freqs.get((stemmed_token, 1.0), 0)
            neg_freq = freqs.get((stemmed_token, 0.0), 0)

            if pos_freq > neg_freq:
                word_sentiments.append({'word': token, 'sentiment': 'positive'})
            elif neg_freq > pos_freq:
                word_sentiments.append({'word': token, 'sentiment': 'negative'})
            else:
                # Nếu từ không có trong từ điển hoặc tần suất bằng nhau
                word_sentiments.append({'word': token, 'sentiment': 'neutral'})
        else:
            # Các từ bị loại bỏ (stopwords, punctuation...)
            word_sentiments.append({'word': token, 'sentiment': 'neutral'})

    return word_sentiments