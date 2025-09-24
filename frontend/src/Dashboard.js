// frontend/src/Dashboard.js
import React, { useState, useCallback, Suspense } from 'react';
import axios from 'axios';

// TỐI ƯU: Sử dụng React.lazy
const AnalysisForm = React.lazy(() => import('./components/analysis_form'));
const ResultDisplay = React.lazy(() => import('./components/result_display')); // THAY ĐỔI
const HistoryFeed = React.lazy(() => import('./components/history_feed'));
const MetricsPanel = React.lazy(() => import('./components/metric_panel'));

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/analyze';

function Dashboard() {
  const [tweet, setTweet] = useState('');
  // THAY ĐỔI: `currentResult` sẽ hiển thị kết quả mới nhất hoặc kết quả được chọn từ lịch sử
  const [currentResult, setCurrentResult] = useState(null); 
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!tweet.trim()) return;

    setIsLoading(true);
    setCurrentResult(null);

    try {
      const response = await axios.post(API_URL, { tweet }, { timeout: 15000 });
      
      // THAY ĐỔI: Thêm timestamp vào kết quả để dùng cho biểu đồ xu hướng
      const newResult = { ...response.data, timestamp: new Date() };
      
      setCurrentResult(newResult);
      // Giữ nguyên `tweet` và `result` trong history để các component con không bị lỗi
      setHistory(prevHistory => [{ tweet, result: newResult }, ...prevHistory]);

    } catch (error) {
      console.error("Lỗi khi phân tích:", error);
      if (error.code === 'ECONNABORTED') {
        alert("Không nhận được phản hồi từ máy chủ. Vui lòng thử lại sau.");
      } else {
        alert("Đã xảy ra lỗi trong quá trình phân tích.");
      }
    } finally {
      setIsLoading(false);
    }
  }, [tweet]);

  // THÊM MỚI: Hàm để xem lại kết quả chi tiết từ lịch sử
  const handleHistorySelect = useCallback((selectedItem) => {
    setCurrentResult(selectedItem.result);
  }, []);

  return (
    <div className="dashboard">
      <AnalysisForm
        tweet={tweet}
        setTweet={setTweet}
        onSubmit={handleSubmit}
        isLoading={isLoading}
      />
      {/* THAY ĐỔI: Sử dụng ResultDisplay và truyền vào currentResult */}
      <Suspense fallback={<div>Đang tải...</div>}>
        <ResultDisplay result={currentResult} />
        <HistoryFeed history={history} onItemSelect={handleHistorySelect} />
        <MetricsPanel history={history} />
      </Suspense>
    </div>
  );
}

export default Dashboard;