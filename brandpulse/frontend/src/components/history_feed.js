import React from 'react';

// TỐI ƯU: Bọc component trong React.memo
const HistoryFeed = React.memo(({ history }) => {
  return (
    <div className="panel history-feed-panel">
      <h2 className="panel-title">Lịch sử Phân tích</h2>
      <div className="history-feed">
        {history.length === 0 ? (
          <p>Chưa có phân tích nào.</p>
        ) : (
          history.map((item, index) => {
            // SỬA LỖI: Khai báo biến isPositive ở đây
            const isPositive = item.result.tweets[0].sentiment === 'Positive';

            // Lấy ra phần trăm tương ứng
            const confidence = isPositive 
              ? item.result.positive_percentage 
              : item.result.negative_percentage;

            // Xác định class CSS dựa trên kết quả
            const sentimentClass = isPositive 
              ? 'history-item-positive' 
              : 'history-item-negative';

            return (
              <div
                key={index}
                className={`history-item ${sentimentClass}`}
              >
                <p>"{item.tweet}"</p>
                {/* Sử dụng biến confidence đã được tính toán */}
                <span>{`Độ tin cậy: ${confidence.toFixed(1)}%`}</span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
});

export default HistoryFeed;