# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from model.feature_engineering import extract_features_6
from model.utils import sigmoid

app = Flask(__name__)
CORS(app)

# Load the frequency dictionary, the trained model, and the scaler
with open('model/freqs.pkl', 'rb') as f:
    freqs = pickle.load(f)

with open('model/model.pkl', 'rb') as f:
    theta = pickle.load(f)

with open('model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def predict_tweet(tweet):
    """
    Input:
        tweet: a string
    Output:
        y_pred: the probability of a tweet being positive or negative
    """
    # extract the features of the tweet and store it into x
    x = extract_features_6(tweet, freqs)

    # --- THÊM MỚI: CHUẨN HÓA DỮ LIỆU ĐẦU VÀO ---
    x_scaled = x.copy()
    x_scaled[:, 1:] = scaler.transform(x[:, 1:])
    # -------------------------------------------

    # make the prediction using scaled x and theta
    y_pred = sigmoid(np.dot(x_scaled, theta))

    return y_pred

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    tweet = data['tweet']
    prediction = predict_tweet(tweet)
    sentiment = 'Positive' if prediction > 0.5 else 'Negative'
    return jsonify({
        'sentiment': sentiment,
        'probability': float(prediction)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
