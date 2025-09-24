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

    Input:
        x: ma trận đặc trưng, kích thước (m, n).
        y: vector nhãn thực tế, kích thước (m, 1).
        theta: vector trọng số ban đầu, kích thước (n, 1).
        alpha: tốc độ học (learning rate).
        num_iters: số lần lặp.
    Output:
        theta: vector trọng số đã được tối ưu.
    """
    m = x.shape[0]
    for i in range(0, num_iters):
        # Tính toán dự đoán (hypothesis)
        z = np.dot(x, theta)
        h = sigmoid(z)

        # Tính toán gradient
        gradient = (1/m) * np.dot(x.T, (h - y))

        # Cập nhật trọng số theta
        theta = theta - alpha * gradient
        
        # (Tùy chọn) In ra chi phí sau mỗi 100 lần lặp để theo dõi
        if i % 100 == 0:
            # Tính toán chi phí (cost function J)
            J = -1./m * (np.dot(y.T, np.log(h)) + np.dot((1-y).T, np.log(1-h)))
            print(f"Iteration {i}: Cost = {np.squeeze(J)}")
            
    return theta

# --- PHẦN CHÍNH: CHUẨN BỊ DỮ LIỆU, HUẤN LUYỆN VÀ LƯU MODEL ---

if __name__ == "__main__":
    # 1. Tải và chuẩn bị dữ liệu
    print("Step 1: Loading and preparing data...")
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
    X = np.zeros((len(train_x), 6))
    for i in range(len(train_x)):
        X[i, :]= extract_features6(train_x[i], freqs)
    Y = train_y
    print("Features extracted.")

    # 4. Huấn luyện model bằng Gradient Descent
    print("\nStep 4: Training the model with Gradient Descent...")
    # Các siêu tham số (hyperparameters)
    learning_rate = 1e-9
    num_iterations = 1500
    
    # Khởi tạo trọng số theta ban đầu
    initial_theta = np.zeros((6, 1))

    # Chạy Gradient Descent để học ra trọng số tối ưu
    trained_theta = gradientDescent(X, Y, initial_theta, learning_rate, num_iterations)
    print("Model training complete.")

    # 5. Lưu các thành phần đã huấn luyện
    print("\nStep 5: Saving model artifacts...")
    # Lưu từ điển tần suất
    with open('model/freqs_colab.pkl', 'wb') as f:
        pickle.dump(freqs, f)
    print(" - Frequency dictionary saved to model/freqs_colab.pkl")

    # Lưu trọng số đã huấn luyện (chính là w6)
    with open('model/w6.pkl', 'wb') as f:
        pickle.dump(trained_theta, f)
    print(" - Trained weights saved to model/w6.pkl")

    print("\nTraining process finished successfully! ✨")