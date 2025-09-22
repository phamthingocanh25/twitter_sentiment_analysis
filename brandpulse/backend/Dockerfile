# Sử dụng một base image Python gọn nhẹ
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt trước để tận dụng caching của Docker
COPY requirements.txt .

# Cài đặt các gói phụ thuộc
RUN pip install --no-cache-dir -r requirements.txt

# Tải xuống các tài nguyên NLTK cần thiết trong quá trình build image
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader twitter_samples

# Sao chép toàn bộ code của ứng dụng vào thư mục làm việc
COPY . .

# Mở cổng 5000 để ứng dụng Flask có thể nhận request
EXPOSE 5000

# Lệnh để chạy ứng dụng khi container khởi động
CMD ["python", "app.py"]