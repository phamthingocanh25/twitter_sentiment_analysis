# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from model.utils import predict_single_tweet # Đảm bảo import đúng
import os
from model.utils import predict_single_tweet, get_word_sentiments

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app)  # Bật CORS cho tất cả các route

# Xác định đường dẫn đến các tệp model
base_dir = os.path.dirname(os.path.abspath(__file__))
freqs_path = os.path.join(base_dir, 'model/freqs_colab.pkl')
w_path = os.path.join(base_dir, 'model/w6.pkl') # Tên file model không đổi

# Tải các tệp model
with open(freqs_path, 'rb') as f:
    freqs = pickle.load(f)

with open(w_path, 'rb') as f:
    w = pickle.load(f) # Tải trọng số đã được huấn luyện lại

# Định nghĩa route cho API
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON provided"}), 400

    tweet_text = data.get('tweet')
    if not tweet_text:
        return jsonify({"error": "No 'tweet' key provided in JSON"}), 400

    # 1. Lấy kết quả dự đoán cốt lõi (không thay đổi)
    sentiment, prob_positive = predict_single_tweet(tweet_text, freqs, w)

    # 2. Thêm logic cho trạng thái "Mixed"
    final_sentiment = sentiment
    # Nếu xác suất rất gần 50% (ví dụ: trong khoảng 40-60%), ta coi là "Mixed"
    if 0.4 < prob_positive < 0.6:
        final_sentiment = "Mixed"

    # 3. Lấy thông tin highlight từ khóa
    word_sentiments = get_word_sentiments(tweet_text, freqs)

    # 4. Tính toán các giá trị phần trăm
    positive_percentage = prob_positive * 100
    negative_percentage = (1 - prob_positive) * 100

    # 5. Tạo response MỚI với cấu trúc dữ liệu phong phú hơn
    response_data = {
        'original_text': tweet_text,
        'overall_sentiment': final_sentiment, # 'Positive', 'Negative', hoặc 'Mixed'
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'highlighted_text': word_sentiments # Dữ liệu cho việc highlight
    }
    
    # (Tùy chọn - Bước tiếp theo) Ở đây bạn sẽ thêm code để lưu response_data vào database

    return jsonify(response_data)

# Chạy ứng dụng
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')