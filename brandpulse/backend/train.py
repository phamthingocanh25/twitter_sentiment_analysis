# backend/train.py

import nltk
import pickle
import numpy as np
from nltk.corpus import twitter_samples

# Import các hàm cần thiết từ file utils
# sigmoid được cần cho gradient descent
from model.utils import process_tweet, extract_features6, sigmoid

def build_freqs(tweets, ys):
    """Xây dựng từ điển tần suất từ các tweet."""
    yslist = np.squeeze(ys).tolist()
    freqs = {}
    for y, tweet in zip(yslist, tweets):
        for word in process_tweet(tweet):
            pair = (word, y)
            freqs[pair] = freqs.get(pair, 0) + 1
    return freqs

def gradientDescent(x, y, theta, alpha, num_iters):
    """
    Hàm thực hiện Gradient Descent để tối ưu trọng số theta.
    """
    m = x.shape[0]
    # <<< THAY ĐỔI: Thêm epsilon để tránh lỗi log(0)
    epsilon = 1e-12
    for i in range(0, num_iters):
        z = np.dot(x, theta)
        h = sigmoid(z)

        # Tính toán hàm mất mát (cost function)
        J = -1./m * (np.dot(y.T, np.log(h + epsilon)) + np.dot((1-y).T, np.log(1-h + epsilon)))

        # Tính toán gradient
        gradient = (1/m) * np.dot(x.T, (h-y))

        # Cập nhật trọng số theta
        theta = theta - (alpha * gradient)

        if (i % 1000 == 0): # In ra mỗi 1000 vòng lặp
            print(f"Iteration {i}, Cost: {np.squeeze(J):.6f}")
            if np.isnan(J) or np.isinf(J):
                print("Lỗi: Hàm mất mát (Cost function) đã bị NaN hoặc Inf!")
                break
    return theta

if __name__ == '__main__':
    # Tải bộ dữ liệu mẫu từ NLTK
    nltk.download('twitter_samples')

    # 1. Chuẩn bị dữ liệu
    print("Step 1: Preparing data...")
    all_positive_tweets = twitter_samples.strings('positive_tweets.json')
    all_negative_tweets = twitter_samples.strings('negative_tweets.json')

    train_pos = all_positive_tweets[:4000]
    train_neg = all_negative_tweets[:4000]
    train_x = train_pos + train_neg
    train_y = np.append(np.ones((len(train_pos), 1)), np.zeros((len(train_neg), 1)), axis=0)

    # 2. Xây dựng từ điển tần suất
    print("\nStep 2: Building frequency dictionary...")
    freqs = build_freqs(train_x, train_y)
    print(f"Frequency dictionary built. Total pairs: {len(freqs)}")

    # 3. Trích xuất đặc trưng
    print("\nStep 3: Extracting features...")
    # <<< THAY ĐỔI: Khởi tạo ma trận X với 7 cột cho 7 đặc trưng (6 features + 1 bias)
    X = np.zeros((len(train_x), 7))
    for i in range(len(train_x)):
        # Hàm extract_features6 bây giờ trả về vector (1, 7)
        X[i, :] = extract_features6(train_x[i], freqs)
    Y = train_y
    print("Features extracted. Shape of X:", X.shape)

    # 4. Huấn luyện model bằng Gradient Descent
    print("\nStep 4: Training the model with Gradient Descent...")
    # <<< THAY ĐỔI: Cập nhật siêu tham số để khớp với notebook
    learning_rate = 1e-4
    num_iterations = 20000

    # <<< THAY ĐỔI: Khởi tạo theta với 7 hàng
    initial_theta = np.zeros((7, 1))

    # Chạy Gradient Descent để học ra trọng số tối ưu
    trained_theta = gradientDescent(X, Y, initial_theta, learning_rate, num_iterations)
    print("Model training complete.")

    # 5. Lưu các thành phần đã huấn luyện
    print("\nStep 5: Saving model artifacts...")
    # Lưu từ điển tần suất
    with open('model/freqs_colab.pkl', 'wb') as f:
        pickle.dump(freqs, f)

    # Lưu trọng số đã huấn luyện (giờ là w7)
    with open('model/w6.pkl', 'wb') as f: # Vẫn lưu tên w6.pkl để app.py không cần đổi
        pickle.dump(trained_theta, f)

    print("Artifacts saved successfully to 'model/' directory.")