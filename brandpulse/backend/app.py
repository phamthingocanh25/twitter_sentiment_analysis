from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
# THÊM LẠI DÒNG IMPORT STANDARDSCALER
from sklearn.preprocessing import StandardScaler
from model.feature_engineering import extract_features_6
from model.utils import sigmoid

app = Flask(__name__)
CORS(app)

# Tải frequency dictionary, model và scaler
with open('model/freqs.pkl', 'rb') as f:
    freqs = pickle.load(f)

with open('model/model.pkl', 'rb') as f:
    theta = pickle.load(f)

# KHÔI PHỤC VIỆC TẢI SCALER
with open('model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def predict_tweet(tweet):
    # Trích xuất đặc trưng
    x = extract_features_6(tweet, freqs)

    # KHÔI PHỤC LẠI BƯỚC CHUẨN HÓA DỮ LIỆU
    # Bỏ qua cột bias đầu tiên khi chuẩn hóa
    x_scaled = x.copy()
    x_scaled[:, 1:] = scaler.transform(x[:, 1:])

    # Dự đoán bằng vector đặc trưng đã được chuẩn hóa (x_scaled)
    y_pred = sigmoid(np.dot(x_scaled, theta))

    return y_pred

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    tweet = data.get('tweet', '') # Thêm get để tránh lỗi nếu không có 'tweet'
    if not tweet:
        return jsonify({'error': 'No tweet provided'}), 400
        
    prediction = predict_tweet(tweet)
    
    # Kiểm tra nếu kết quả là NaN
    if np.isnan(prediction):
        return jsonify({
            'sentiment': 'Error',
            'probability': 'NaN'
        })
        
    sentiment = 'Positive' if prediction > 0.5 else 'Negative'
    return jsonify({
        'sentiment': sentiment,
        'probability': float(prediction)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)