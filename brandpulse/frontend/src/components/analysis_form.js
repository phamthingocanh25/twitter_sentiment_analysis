import React from 'react';

// SỬA LỖI: Thêm "setTweet" vào danh sách props để component có thể nhận và sử dụng nó.
function AnalysisForm({ tweet, setTweet, onSubmit, isLoading }) {
  return (
    <div className="panel analysis-form-panel">
      <h2 className="panel-title">Phân tích Tweet</h2>
      <form onSubmit={onSubmit} className="analysis-form">
        <textarea
          placeholder="Nhập tweet của bạn vào đây..."
          value={tweet}
          onChange={(e) => setTweet(e.target.value)}
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !tweet.trim()}>
          {isLoading ? 'Đang phân tích...' : 'Phân tích'}
        </button>
      </form>
    </div>
  );
}

export default AnalysisForm;
