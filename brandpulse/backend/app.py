from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

# Import các hàm cần thiết từ file utils
from model.utils import predict_single_tweet

app = Flask(__name__)
CORS(app)

# Load the frequency dictionary and the model weights
with open('model/freqs_colab.pkl', 'rb') as f:
    freqs = pickle.load(f)

with open('model/w6.pkl', 'rb') as f:
    w6 = pickle.load(f)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    tweet_text = data.get('brand') # Vẫn dùng key 'brand' từ frontend

    if not tweet_text:
        return jsonify({"error": "No text provided"}), 400

    # Thực hiện dự đoán bằng hàm đã import
    prob_positive_raw = predict_single_tweet(tweet_text, freqs, w6)
    prob_positive = prob_positive_raw[0][0]
    prob_negative = 1 - prob_positive

    sentiment = "Positive" if prob_positive > 0.5 else "Negative"

    response_data = {
        "positive_percentage": round(prob_positive * 100, 2),
        "negative_percentage": round(prob_negative * 100, 2),
        "neutral_percentage": 0,
        "tweets": [
            {
                "text": tweet_text,
                "sentiment": sentiment
            }
        ]
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)