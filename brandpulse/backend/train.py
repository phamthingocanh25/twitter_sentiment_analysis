# backend/train.py
import nltk
from nltk.corpus import twitter_samples
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from model.utils import process_tweet, sigmoid
from model.feature_engineering import extract_features_6
import os

# ... (các phần code tải dữ liệu và build_freqs giữ nguyên) ...

# create frequency dictionary
freqs = build_freqs(train_x, train_y)

# Collect the features 'x' and stack them into a matrix 'X'
X = np.zeros((len(train_x), 7))
for i in range(len(train_x)):
    X[i, :]= extract_features_6(train_x[i], freqs)

Y = train_y

# --- THÊM MỚI: CHUẨN HÓA DỮ LIỆU ---
# Bỏ qua cột bias đầu tiên (cột toàn số 1)
scaler = StandardScaler()
X_scaled = X.copy()
X_scaled[:, 1:] = scaler.fit_transform(X[:, 1:])
# ------------------------------------

# training logistic regression model
# Sử dụng X_scaled để train
J, theta = gradient_descent(X_scaled, Y, np.zeros((7, 1)), 1e-4, 20000)

# --- LƯU LẠI SCALER VÀ MODEL ---
model_dir = 'model'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

with open(os.path.join(model_dir, 'freqs.pkl'), 'wb') as f:
    pickle.dump(freqs, f)

with open(os.path.join(model_dir, 'model.pkl'), 'wb') as f:
    pickle.dump(theta, f)

with open(os.path.join(model_dir, 'scaler.pkl'), 'wb') as f:
    pickle.dump(scaler, f)
# --------------------------------

print("Training completed. `freqs.pkl`, `model.pkl`, and `scaler.pkl` are saved.")