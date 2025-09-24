import nltk
from nltk.corpus import twitter_samples
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from model.utils import process_tweet # Đảm bảo import hàm này
from model.feature_engineering import extract_features
import os

# --- THÊM PHẦN ĐỊNH NGHĨA HÀM BUILD_FREQS ---
def build_freqs(tweets, ys):
    """Build frequencies.
    Input:
        tweets: a list of tweets
        ys: an m x 1 array with the sentiment label of each tweet (0 or 1)
    Output:
        freqs: a dictionary mapping each (word, sentiment) pair to its frequency
    """
    # Convert np array to list since zip requires an iterable
    yslist = np.squeeze(ys).tolist()

    # Start with an empty dictionary and populate it by looping over all tweets
    # and over all processed words in each tweet.
    freqs = {}
    for y, tweet in zip(yslist, tweets):
        for word in process_tweet(tweet):
            pair = (word, y)
            freqs[pair] = freqs.get(pair, 0) + 1

    return freqs
# --------------------------------------------------

# --- THÊM PHẦN TẢI DỮ LIỆU ---
# download the twitter samples
nltk.download('twitter_samples')

# load positive and negative tweets
all_positive_tweets = twitter_samples.strings('positive_tweets.json')
all_negative_tweets = twitter_samples.strings('negative_tweets.json')

# split the data into two pieces, one for training and one for testing (validation)
# 80% for training, 20% for testing
train_pos = all_positive_tweets[:4000]
test_pos = all_positive_tweets[4000:]
train_neg = all_negative_tweets[:4000]
test_neg = all_negative_tweets[4000:]

train_x = train_pos + train_neg
test_x = test_pos + test_neg

# combine positive and negative labels
train_y = np.append(np.ones((len(train_pos), 1)), np.zeros((len(train_neg), 1)), axis=0)
test_y = np.append(np.ones((len(test_pos), 1)), np.zeros((len(test_neg), 1)), axis=0)
# --------------------------------------------------

# --- PHẦN CODE GỐC CỦA BẠN (Cần thêm hàm gradient_descent) ---
# Giả sử bạn có hàm gradient_descent ở đâu đó, nếu không, bạn cần thêm nó vào.
# Ví dụ một hàm gradient_descent cơ bản:
def gradient_descent(x, y, theta, alpha, num_iters):
    m = x.shape[0]
    for i in range(0, num_iters):
        z = np.dot(x, theta)
        h = 1 / (1 + np.exp(-z))
        J = -1./m * (np.dot(y.transpose(), np.log(h)) + np.dot((1-y).transpose(), np.log(1-h)))
        theta = theta - (alpha/m) * np.dot(x.transpose(),(h-y))
    J = float(J)
    return J, theta

# create frequency dictionary
print("Building frequencies...")
freqs = build_freqs(train_x, train_y)

# Collect the features 'x' and stack them into a matrix 'X'
print("Extracting features...")
X = np.zeros((len(train_x), 7))
for i in range(len(train_x)):
    X[i, :]= extract_features(train_x[i], freqs)

Y = train_y

# Chuẩn hóa dữ liệu
print("Scaling data...")
scaler = StandardScaler()
X_scaled = X.copy()
X_scaled[:, 1:] = scaler.fit_transform(X[:, 1:])

# Training logistic regression model
print("Training model...")
J, theta = gradient_descent(X_scaled, Y, np.zeros((7, 1)), 1e-4, 20000)

# Lưu lại scaler và model
print("Saving model files...")
model_dir = 'model'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

with open(os.path.join(model_dir, 'freqs.pkl'), 'wb') as f:
    pickle.dump(freqs, f)

with open(os.path.join(model_dir, 'model.pkl'), 'wb') as f:
    pickle.dump(theta, f)

with open(os.path.join(model_dir, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)

print("\nTraining completed!")
print(f"Model cost: {J:.6f}")
print("`freqs.pkl`, `model.pkl`, and `scaler.pkl` are saved in the 'model' directory.")