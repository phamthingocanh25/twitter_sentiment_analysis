import React from 'react';

// TỐI ƯU: Bọc component trong React.memo
const MetricsPanel = React.memo(({ history }) => {
  // SỬA LỖI: Cập nhật logic lọc để khớp với cấu trúc dữ liệu đúng từ API
  const positiveCount = history.filter(item => item.result.tweets[0].sentiment === 'Positive').length;
  const negativeCount = history.filter(item => item.result.tweets[0].sentiment === 'Negative').length;

  return (
    <div className="panel metrics-panel">
      <h2 className="panel-title">Thống kê</h2>
      <div className="metrics-container">
        <div className="metric-item">
          <h3 className="sentiment-positive">{positiveCount}</h3>
          <p>Tích cực</p>
        </div>
        <div className="metric-item">
          <h3 className="sentiment-negative">{negativeCount}</h3>
          <p>Tiêu cực</p>
        </div>
      </div>
    </div>
  );
});

export default MetricsPanel;