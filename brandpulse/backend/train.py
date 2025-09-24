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

        # Tính toán hàm mất mát (cost function)
        # Thêm một giá trị rất nhỏ (epsilon) để tránh lỗi log(0)
        epsilon = 1e-10
        J = -1./m * (np.dot(y.T, np.log(h + epsilon)) + np.dot((1-y).T, np.log(1-h + epsilon)))

        # Tính toán gradient
        gradient = (1/m) * np.dot(x.T, (h-y))
        
        # Cập nhật trọng số theta
        theta = theta - (alpha * gradient)

        # ===== BẮT ĐẦU THAY ĐỔI =====
        # Thêm vào để debug và theo dõi quá trình huấn luyện
        if (i % 100 == 0):
            print(f"Iteration {i}, Cost: {np.squeeze(J)}")
            # Kiểm tra nếu cost function trở thành NaN hoặc Inf
            if np.isnan(J) or np.isinf(J):
                print("Lỗi: Hàm mất mát (Cost function) đã bị NaN hoặc Inf!")
                print("Thử giảm learning_rate hoặc kiểm tra lại dữ liệu đầu vào.")
                break
        # ===== KẾT THÚC THAY ĐỔI =====

    return theta

if __name__ == '__main__':
    # Tải bộ dữ liệu mẫu từ NLTK
    nltk.download('twitter_samples')
    
    # 1. Chuẩn bị dữ liệu
    print("Step 1: Preparing data...")
    all_positive_tweets = twitter_samples.strings('positive_tweets.json')
    all_negative_tweets = twitter_samples.strings('negative_tweets.json')

    # Chia dữ liệu: 80% cho tập huấn luyện, 20% cho tập kiểm tra
    split_ratio = 0.8
    split_pos = int(len(all_positive_tweets) * split_ratio)
    split_neg = int(len(all_negative_tweets) * split_ratio)

    train_pos = all_positive_tweets[:split_pos]
    train_neg = all_negative_tweets[:split_neg]
    
    # Kết hợp các tweet tích cực và tiêu cực
    train_x = train_pos + train_neg
    
    # Tạo nhãn: 1 cho tích cực, 0 cho tiêu cực
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
    
    # Lưu trọng số đã huấn luyện
    with open('model/w6.pkl', 'wb') as f:
        pickle.dump(trained_theta, f)
        
    print("Artifacts saved successfully to 'model/' directory.")