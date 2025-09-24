import numpy as np
from .utils import process_tweet
from nltk.tokenize import TweetTokenizer

def extract_features(tweet, freqs):
    """
    Hàm này trích xuất 6 features từ một tweet.
    Input:
        tweet (str): một chuỗi string là nội dung tweet
        freqs (dict): một dictionary ánh xạ mỗi cặp (từ, label) tới tần suất của nó
    Output:
        x (np.array): một vector feature có chiều (1, 7)
    """
    # Xử lý tweet (tokenize, stemming, loại bỏ stop words)
    word_l = process_tweet(tweet)

    # Khởi tạo vector feature với 7 phần tử (1 bias + 6 features)
    x = np.zeros(7)

    # Feature 0: Bias term
    x[0] = 1

    # Feature 1 & 2: Tổng tần suất các từ tích cực và tiêu cực
    for word in word_l:
        # Tăng tổng điểm tích cực
        x[1] += freqs.get((word, 1.0), 0)
        # Tăng tổng điểm tiêu cực
        x[2] += freqs.get((word, 0.0), 0)

    # Sử dụng TweetTokenizer để phân tích tweet gốc cho các feature tiếp theo
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)

    # Feature 3: Đếm các từ phủ định (ví dụ: 'not', 'no', 'never')
    # Giúp model hiểu được các câu như "I'm not happy"
    negation_words = ['not', 'no', 'never', "don't", "can't", "isn't"]
    x[3] = sum(1 for word in tweet_tokens if word in negation_words)

    # Feature 4: Đếm các đại từ nhân xưng (pronouns)
    # Tweet mang tính cá nhân cao thường thể hiện cảm xúc mạnh hơn
    pronouns = ["i", "me", "my", "mine", "we", "us", "our", "ours", "you", "your",
                "he", "him", "his", "she", "her", "hers", "it", "its", "they",
                "them", "their", "theirs"]
    x[4] = sum(1 for word in tweet_tokens if word.lower() in pronouns)

    # Feature 5: Đếm số dấu chấm than (!)
    # Thường được dùng để nhấn mạnh cảm xúc
    x[5] = tweet.count('!')

    # Feature 6: Đếm số lượng hashtag (#)
    # Hashtag thường tóm tắt chủ đề hoặc cảm xúc chính của tweet
    x[6] = tweet.count('#')

    # Đảm bảo shape của vector là (1, 7)
    x = x.reshape((1, 7))
    return x