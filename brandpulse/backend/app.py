 # File chính chạy API server (Flask/FastAPI)
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from model.feature_engineering import extract_features

app = Flask(__name__)
CORS(app)  # Cho phép truy cập từ các domain khác (frontend)

# --- Tải mô hình và từ điển tần suất đã được huấn luyện ---
try:
    with open('model/model.pkl', 'rb') as f:
        model_data = pickle.load(f)
        weights = model_data['weights']

    with open('model/freqs.pkl', 'rb') as f:
        freqs = pickle.load(f)
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file model.pkl hoặc freqs.pkl.")
    print("Vui lòng chạy file train.py để huấn luyện và tạo các file này trước.")
    weights = None
    freqs = None

# --- Các hàm cần thiết ---
def sigmoid(z):
    """Hàm sigmoid."""
    return 1 / (1 + np.exp(-z))

def predict_tweet(tweet, freqs, theta):
    """
    Dự đoán cảm xúc của một tweet.
    Input:
        tweet: một chuỗi string
        freqs: từ điển tần suất
        theta: trọng số của mô hình
    Output:
        y_pred: xác suất tweet là tích cực
    """
    x = extract_features(tweet, freqs)
    y_pred = sigmoid(np.dot(x, theta))
    return y_pred

@app.route('/predict', methods=['POST'])
def predict():
    if not weights or not freqs:
        return jsonify({'error': 'Mô hình chưa được tải. Vui lòng kiểm tra console của server.'}), 500

    data = request.get_json()
    tweet_text = data.get('tweet', '')

    if not tweet_text:
        return jsonify({'error': 'Không có tweet nào được cung cấp.'}), 400

    # Dự đoán
    confidence = predict_tweet(tweet_text, freqs, weights)
    
    # Chuyển đổi xác suất thành nhãn
    sentiment = 'Tích cực' if confidence > 0.5 else 'Tiêu cực'

    response = {
        'sentiment': sentiment,
        'confidence': float(confidence)
    }

    return jsonify(response)

if __name__ == '__main__':
    # Chạy Flask app trên cổng 5000
    app.run(host='0.0.0.0', port=5000, debug=True)