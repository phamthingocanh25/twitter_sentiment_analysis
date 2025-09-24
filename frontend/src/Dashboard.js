// frontend/src/Dashboard.js
import React, { useState, useCallback, Suspense } from 'react';
import axios from 'axios';

// TỐI ƯU: Sử dụng React.lazy để tải component khi cần
const AnalysisForm = React.lazy(() => import('./components/analysis_form'));
const ResultDisplay = React.lazy(() => import('./components/result_display'));
const HistoryFeed = React.lazy(() => import('./components/history_feed'));
const MetricsPanel = React.lazy(() => import('./components/metric_panel'));

// --- CHỈNH SỬA QUAN TRỌNG NHẤT ---
// Dòng này sẽ sử dụng biến môi trường nếu có, nếu không sẽ mặc định là URL của Render.
// ❗️ HÃY THAY THẾ 'your-service-name' BẰNG TÊN BACKEND SERVICE CỦA BẠN TRÊN RENDER.
const API_URL = process.env.REACT_APP_API_URL || 'https://twitter-sentiment-analysis-2-qs7y.onrender.com/analyze';

function Dashboard() {
  const [tweet, setTweet] = useState('');
  const [currentResult, setCurrentResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(''); // Thêm state để quản lý và hiển thị lỗi

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!tweet.trim()) return;

    setIsLoading(true);
    setCurrentResult(null);
    setError(''); // Xóa lỗi cũ mỗi khi bắt đầu một yêu cầu mới

    try {
      // Gọi API bằng URL đã được cấu hình ở trên
      const response = await axios.post(API_URL, { tweet }, { timeout: 20000 }); // Tăng timeout lên 20s

      const newResult = { ...response.data, timestamp: new Date() };

      setCurrentResult(newResult);
      setHistory(prevHistory => [{ tweet, result: newResult }, ...prevHistory]);

    } catch (error) {
      console.error("Lỗi khi phân tích:", error);
      // Cung cấp thông báo lỗi thân thiện hơn cho người dùng
      if (error.code === 'ECONNABORTED' || error.response?.status === 503) {
        setError("Máy chủ mất quá nhiều thời gian để phản hồi. Vui lòng thử lại sau.");
      } else {
        setError("Đã xảy ra lỗi trong quá trình phân tích. Vui lòng kiểm tra lại tweet và thử lại.");
      }
    } finally {
      setIsLoading(false);
    }
  }, [tweet]); // Dependency array chỉ cần 'tweet' là đủ

  const handleHistorySelect = useCallback((selectedItem) => {
    setCurrentResult(selectedItem.result);
  }, []);

  return (
    <div className="dashboard">
      {/* Suspense dùng để hiển thị fallback UI trong khi component đang được tải lười */}
      <Suspense fallback={<div className="loading-fallback">Đang tải giao diện...</div>}>
        <AnalysisForm
          tweet={tweet}
          setTweet={setTweet}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />

        {/* Hiển thị thông báo lỗi một cách rõ ràng nếu có */}
        {error && <div className="error-message">{error}</div>}

        {/* Chỉ hiển thị các component kết quả khi không có lỗi */}
        {!error && (
          <>
            <ResultDisplay result={currentResult} />
            <HistoryFeed history={history} onItemSelect={handleHistorySelect} />
            <MetricsPanel history={history} />
          </>
        )}
      </Suspense>
    </div>
  );
}

export default Dashboard;