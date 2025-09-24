# Nội dung file: brandpulse/backend/train.py
import nltk
import numpy as np
from nltk.corpus import twitter_samples
import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
import pickle

# --- CÁC HÀM TIỀN XỬ LÝ VÀ HUẤN LUYỆN TỪ COLAB ---

def process_tweet(tweet):
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    tweet = re.sub(r'\$\w*', '', tweet)
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https://[^\s\n\r]+', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)
    tweets_clean = []
    for word in tweet_tokens:
        if (word not in stopwords_english and word not in string.punctuation):
            stem_word = stemmer.stem(word)
            tweets_clean.append(stem_word)
    return tweets_clean

def build_freqs(tweets, ys):
    yslist = np.squeeze(ys).tolist()
    freqs = {}
    for y, tweet in zip(yslist, tweets):
        for word in process_tweet(tweet):
            pair = (word, y)
            freqs[pair] = freqs.get(pair, 0) + 1
    return freqs

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def gradientDescent(x, y, theta, alpha, num_iters):
    m = x.shape[0]
    for i in range(0, num_iters):
        z = np.dot(x, theta)
        h = sigmoid(z)
        J = -1./m * (np.dot(y.transpose(), np.log(h)) + np.dot((1-y).transpose(), np.log(1-h)))
        theta = theta - (alpha/m) * np.dot(x.transpose(), (h-y))
    J = float(J)
    return J, theta

def extract_features6(tweet, freqs):
    word_l = process_tweet(tweet)
    x = np.zeros((1, 6))
    x[0, 0] = 1 # bias term
    positive_emojis = [':)', ':-)', ':D', '=)', ':]', ':-]', ';)', ';-)', '^_^', '<3']
    negative_emojis = [':(', ':-(', ':(', '=(', ':[', ':-[']
    pos_count, neg_count, pos_emoji_count, neg_emoji_count = 0, 0, 0, 0
    for word in word_l:
        pos_count += freqs.get((word, 1.0), 0)
        neg_count += freqs.get((word, 0.0), 0)
    x[0, 3] = sum(1 for word in word_l if (word, 1.0) in freqs)
    x[0, 4] = sum(1 for word in word_l if (word, 0.0) in freqs)
    for emoji in positive_emojis:
        pos_emoji_count += tweet.count(emoji)
    for emoji in negative_emojis:
        neg_emoji_count += tweet.count(emoji)
    x[0, 5] = pos_emoji_count - neg_emoji_count
    x[0, 1] = pos_count
    x[0, 2] = neg_count
    return x

# --- QUÁ TRÌNH HUẤN LUYỆN CHÍNH ---
if __name__ == '__main__':
    print("Bắt đầu quá trình huấn luyện mô hình 6 features...")
    
    # Download NLTK data
    nltk.download('twitter_samples')
    nltk.download('stopwords')

    # Load data
    all_positive_tweets = twitter_samples.strings('positive_tweets.json')
    all_negative_tweets = twitter_samples.strings('negative_tweets.json')
    train_pos = all_positive_tweets[:4000]
    train_neg = all_negative_tweets[:4000]
    train_x = train_pos + train_neg
    train_y = np.append(np.ones((len(train_pos), 1)), np.zeros((len(train_neg), 1)), axis=0)

    print("Đã tải và chuẩn bị dữ liệu.")

    # Tạo từ điển tần suất
    freqs = build_freqs(train_x, train_y)
    print(f"Từ điển tần suất được tạo với {len(freqs)} mục.")

    # Tạo ma trận đặc trưng X
    X = np.zeros((len(train_x), 6))
    for i in range(len(train_x)):
        X[i, :] = extract_features6(train_x[i], freqs)

    # Huấn luyện mô hình
    Y = train_y
    J, w6 = gradientDescent(X, Y, np.zeros((6, 1)), 1e-9, 2000)
    print(f"Huấn luyện hoàn tất. Chi phí cuối cùng (J) = {J:.8f}")

    # Lưu các "sản phẩm" đã huấn luyện
    with open('model/w6.pkl', 'wb') as f:
        pickle.dump(w6, f)
    
    with open('model/freqs_colab.pkl', 'wb') as f:
        pickle.dump(freqs, f)

    print("Đã lưu thành công w6.pkl và freqs_colab.pkl vào thư mục brandpulse/backend/model/")