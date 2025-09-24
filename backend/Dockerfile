FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Thêm dòng này để tải tài nguyên NLTK
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('twitter_samples')"

COPY . .

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:10000", "app:app"]