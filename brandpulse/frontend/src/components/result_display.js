// frontend/src/components/result_display.js
import React from 'react';

// Một component con để render thanh tiến trình
const SentimentBar = ({ label, percentage, colorClass }) => (
  <div className="sentiment-bar-container">
    <div className="sentiment-bar-label">{label}</div>
    <div className="sentiment-bar-wrapper">
      <div
        className={`sentiment-bar ${colorClass}`}
        style={{ width: `${percentage}%` }}
      >
        {percentage.toFixed(1)}%
      </div>
    </div>
  </div>
);

// Component chính để hiển thị kết quả
const ResultDisplay = React.memo(({ result }) => {
  if (!result) {
    return (
      <div className="panel result-display-panel">
        <h2 className="panel-title">Kết quả Phân tích</h2>
        <div className="placeholder-text">
          <p>Kết quả sẽ được hiển thị ở đây...</p>
        </div>
      </div>
    );
  }

  const {
    overall_sentiment,
    positive_percentage,
    negative_percentage,
    highlighted_text
  } = result;

  // --- THAY ĐỔI 1: Tạo map để dịch sang tiếng Việt ---
  const sentimentDisplayMap = {
    'Positive': 'Tích cực =)',
    'Negative': 'Tiêu cực =(',
    'Mixed': 'Tổng hợp =|'
  };

  // --- THAY ĐỔI 2: Sửa lỗi logic lấy class màu sắc ---
  // Các key phải là 'Positive', 'Negative' để khớp với dữ liệu
  const sentimentClassMap = {
    'Positive': 'sentiment-positive',
    'Negative': 'sentiment-negative',
    'Mixed': 'sentiment-mixed'
  };
  const sentimentClass = sentimentClassMap[overall_sentiment];
  const displayText = sentimentDisplayMap[overall_sentiment] || overall_sentiment;

  return (
    <div className="panel result-display-panel">
      <h2 className="panel-title">Kết quả Phân tích</h2>
      
      <div className="sentiment-bars">
        <SentimentBar label="Tích cực" percentage={positive_percentage} colorClass="positive-bar" />
        <SentimentBar label="Tiêu cực" percentage={negative_percentage} colorClass="negative-bar" />
      </div>

      <div className="overall-sentiment">
        {/* --- THAY ĐỔI 3: Sử dụng biến displayText đã được dịch --- */}
        <h3>Tổng quan: <span className={sentimentClass}>{displayText}</span></h3>
      </div>
      
      <div className="highlighted-text-container">
        <h3>Từ khóa nổi bật:</h3>
        <p className="highlighted-text">
          {highlighted_text.map((item, index) => (
            <span key={index} className={`highlight-${item.sentiment}`}>
              {item.word}{' '}
            </span>
          ))}
        </p>
      </div>
    </div>
  );
});

export default ResultDisplay;