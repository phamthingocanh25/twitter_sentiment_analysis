import pickle
import numpy as np
import nltk
from nltk.corpus import twitter_samples
from model.utils import process_tweet
from model.feature_engineering import extract_features

# Tải dữ liệu NLTK
nltk.download('twitter_samples')

# --- Các hàm từ notebook ---

def build_freqs(tweets, ys):
    """Xây dựng từ điển tần suất."""
    yslist = np.squeeze(ys).tolist()
    freqs = {}
    for y, tweet in zip(yslist, tweets):
        for word in process_tweet(tweet):
            pair = (word, y)
            freqs[pair] = freqs.get(pair, 0) + 1
    return freqs

def sigmoid(z):
    """Hàm sigmoid."""
    return 1 / (1 + np.exp(-z))

def gradient_descent(x, y, theta, alpha, num_iters):
    """Thuật toán Gradient Descent."""
    m = x.shape[0]
    for i in range(0, num_iters):
        z = np.dot(x, theta)
        h = sigmoid(z)
        J = -1./m * (np.dot(y.transpose(), np.log(h)) + np.dot((1-y).transpose(), np.log(1-h)))
        theta = theta - (alpha/m) * np.dot(x.transpose(),(h-y))
    J = float(J)
    return J, theta

# --- Tải và chuẩn bị dữ liệu ---
all_positive_tweets = twitter_samples.strings('positive_tweets.json')
all_negative_tweets = twitter_samples.strings('negative_tweets.json')

# Chia dữ liệu train/test
train_pos = all_positive_tweets[:4000]
train_neg = all_negative_tweets[:4000]
train_x = train_pos + train_neg
train_y = np.append(np.ones((len(train_pos), 1)), np.zeros((len(train_neg), 1)), axis=0)

# --- Xây dựng Freqs ---
print("Đang xây dựng từ điển tần suất...")
freqs = build_freqs(train_x, train_y)
print(f"Xây dựng xong. Kích thước: {len(freqs)} cặp (từ, nhãn).")

# --- Trích xuất đặc trưng ---
print("Đang trích xuất đặc trưng cho tập huấn luyện...")
X = np.zeros((len(train_x), 7))
for i in range(len(train_x)):
    X[i, :]= extract_features(train_x[i], freqs)
Y = train_y

# --- Huấn luyện mô hình ---
print("Đang huấn luyện mô hình Logistic Regression...")
# Lưu ý: alpha và num_iters được chọn từ notebook của bạn
J, theta = gradient_descent(X, Y, np.zeros((7, 1)), 1e-4, 20000)
print(f"Huấn luyện xong. Chi phí cuối cùng (cost): {J:.6f}.")

# --- Lưu mô hình và freqs ---
model_to_save = {'weights': theta}
with open('backend/model/model.pkl', 'wb') as f:
    pickle.dump(model_to_save, f)

with open('backend/model/freqs.pkl', 'wb') as f:
    pickle.dump(freqs, f)

print("\nĐã lưu model.pkl và freqs.pkl vào thư mục backend/model/")
