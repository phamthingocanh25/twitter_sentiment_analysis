import React from 'react';

// Component này chịu trách nhiệm cho form nhập liệu và nút bấm
const SentimentForm = ({ tweet, setTweet, handleSubmit, isLoading }) => {
  return (
    <form className="sentiment-form" onSubmit={handleSubmit}>
      <textarea
        placeholder="Nhập tweet của bạn vào đây..."
        value={tweet}
        onChange={(e) => setTweet(e.target.value)}
        required
      />
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Đang phân tích...' : 'Phân tích'}
      </button>
    </form>
  );
};

export default SentimentForm;
