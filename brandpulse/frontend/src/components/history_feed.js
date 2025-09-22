import React from 'react';

const HistoryFeed = ({ history }) => {
  return (
    <div className="panel history-feed-panel">
      <h2 className="panel-title">Lịch sử Phân tích</h2>
      <div className="history-feed">
        {history.length === 0 ? (
          <p>Chưa có phân tích nào.</p>
        ) : (
          history.map((item, index) => (
            <div
              key={index}
              className={`history-item ${
                item.result.sentiment === 'Tích cực'
                  ? 'history-item-positive'
                  : 'history-item-negative'
              }`}
            >
              <p>"{item.tweet}"</p>
              <span>{`Độ tin cậy: ${(item.result.confidence * 100).toFixed(1)}%`}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default HistoryFeed;