import React from 'react';

const MetricsPanel = ({ history }) => {
  const positiveCount = history.filter(item => item.result.sentiment === 'Tích cực').length;
  const negativeCount = history.filter(item => item.result.sentiment === 'Tiêu cực').length;

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
};

export default MetricsPanel;