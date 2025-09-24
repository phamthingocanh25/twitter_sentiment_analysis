// frontend/src/components/history_feed.js
import React from 'react';

const HistoryFeed = React.memo(({ history, onItemSelect }) => {
  // --- THÊM MỚI: Tạo map để dịch sang tiếng Việt ---
  const sentimentDisplayMap = {
    'Positive': 'Tích cực',
    'Negative': 'Tiêu cực',
    'Mixed': 'Tổng hợp'
  };

  return (
    <div className="panel history-feed-panel">
      <h2 className="panel-title">Lịch sử Phân tích</h2>
      <div className="history-feed">
        {history.length === 0 ? (
          <p className="placeholder-text">Chưa có phân tích nào.</p>
        ) : (
          history.map((item, index) => {
            const { overall_sentiment, positive_percentage } = item.result;

            // Lấy text tiếng Việt từ map
            const displayText = sentimentDisplayMap[overall_sentiment] || overall_sentiment;

            const sentimentClass = {
              'Positive': 'history-item-positive',
              'Negative': 'history-item-negative',
              'Mixed': 'history-item-mixed'
            }[overall_sentiment];

            return (
              <div
                key={index}
                className={`history-item ${sentimentClass}`}
                onClick={() => onItemSelect(item)}
                title="Nhấp để xem chi tiết"
              >
                <p>"{item.tweet}"</p>
                <span>
                  {/* --- THAY ĐỔI: Sử dụng displayText thay cho overall_sentiment --- */}
                  {displayText} ({positive_percentage.toFixed(1)}% Tích cực)
                </span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
});

export default HistoryFeed;