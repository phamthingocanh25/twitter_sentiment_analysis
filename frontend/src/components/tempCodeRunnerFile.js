import React, { useState, useCallback } from 'react';
import axios from 'axios';

// TỐI ƯU: Sử dụng React.lazy để tải các component khi cần thiết
const AnalysisForm = React.lazy(() => import('./components/analysis_form'));
const ResultGauge = React.lazy(() => import('./components/result_gauge'));
const HistoryFeed = React.lazy(() => import('./components/history_feed'));
const MetricsPanel = React.lazy(() => import('./components/metric_panel'));

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/predict';

function Dashboard() {
  const [tweet, setTweet] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!tweet.trim()) return;

    setIsLoading(true);
    setResult(null);

    try {
      const response = await axios.post(API_URL, { tweet });
      const newResult = response.data;
      setResult(newResult);
      setHistory(prevHistory => [{ tweet, result: newResult }, ...prevHistory]);
    } catch (error) {
      console.error("Lỗi khi phân tích:", error);
      // Có thể thêm thông báo lỗi cho người dùng ở đây
    } finally {
      setIsLoading(false);
    }
  }, [tweet]);

  return (
    <div className="dashboard">
      <AnalysisForm
        tweet={tweet}
        setTweet={setTweet}
        onSubmit={handleSubmit}
        isLoading={isLoading}
      />
      <ResultGauge result={result} />
      <HistoryFeed history={history} />
      <MetricsPanel history={history} />
    </div>
  );
}

export default Dashboard;