# Nội dung file: brandpulse/backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from model.utils import process_tweet # Sử dụng hàm tiền xử lý đã được đồng bộ

app = Flask(__name__)
CORS(app)

# --- LOAD MÔ HÌNH VÀ TỪ ĐIỂN MỚI ---
try:
    with open("model/w6.pkl", "rb") as f:
        w6 = pickle.load(f)
    with open("model/freqs_colab.pkl", "rb") as f:
        freqs = pickle.load(f)
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file w6.pkl hoặc freqs_colab.pkl.")
    print("Vui lòng chạy 'python train.py' trong thư mục backend trước khi khởi động app.")
    w6, freqs = None, None


# --- CÁC HÀM LOGIC CỦA MÔ HÌNH 6 FEATURES ---
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

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

# --- ENDPOINT API ---
@app.route("/predict", methods=['POST'])
def predict():
    if w6 is None or freqs is None:
        return jsonify({"error": "Model is not loaded. Please run the training script."}), 500

    try:
        data = request.get_json()
        text_to_analyze = data['text']

        # Sử dụng logic 6 features để dự đoán
        features = extract_features6(text_to_analyze, freqs)
        probability_raw = sigmoid(np.dot(features, w6))
        
        probability = probability_raw[0, 0]
        sentiment = "Positive" if probability > 0.5 else "Negative"

        return jsonify({
            "text": text_to_analyze,
            "sentiment": sentiment,
            "probability": float(probability) # Chuyển sang kiểu float
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)