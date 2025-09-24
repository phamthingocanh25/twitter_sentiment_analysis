// frontend/src/components/metric_panel.js
import React, { useMemo } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts';
import WordCloud from 'react-d3-cloud'; // Đã thay đổi: Import thư viện mới

// TỐI ƯU: Bọc component trong React.memo
const MetricsPanel = React.memo(({ history }) => {
    
  // Tính toán dữ liệu cho biểu đồ tròn (Giữ nguyên)
  const pieData = useMemo(() => {
    const counts = history.reduce((acc, item) => {
      const sentiment = item.result.overall_sentiment || 'N/A';
      acc[sentiment] = (acc[sentiment] || 0) + 1;
      return acc;
    }, {});
    return Object.keys(counts).map(key => ({ name: key, value: counts[key] }));
  }, [history]);

  // Xử lý dữ liệu cho Word Cloud (Giữ nguyên)
  const wordCloudData = useMemo(() => {
    const positiveWords = {};
    const negativeWords = {};

    history.forEach(item => {
      const sentiment = item.result.overall_sentiment;
      if (sentiment === 'Positive' || sentiment === 'Negative') {
        item.result.highlighted_text.forEach(wordItem => {
          if (wordItem.sentiment === 'positive') {
            positiveWords[wordItem.word] = (positiveWords[wordItem.word] || 0) + 1;
          } else if (wordItem.sentiment === 'negative') {
            negativeWords[wordItem.word] = (negativeWords[wordItem.word] || 0) + 1;
          }
        });
      }
    });
    
    // Dữ liệu đã có sẵn định dạng { text, value } phù hợp cho react-d3-cloud
    const formatForCloud = (words) => Object.keys(words).map(key => ({ text: key, value: words[key] * 10 })).sort((a,b) => b.value - a.value).slice(0, 30);
    
    return {
      positive: formatForCloud(positiveWords),
      negative: formatForCloud(negativeWords)
    };
  }, [history]);

  const COLORS = {
    'Positive': 'var(--positive-color)',
    'Negative': 'var(--negative-color)',
    'Mixed': 'var(--accent-secondary)'
  };
  
  // Các hàm helper để tùy chỉnh WordCloud mới
  // Xác định kích thước font chữ dựa trên tần suất (value) của từ
  const fontSizeMapper = word => Math.log2(word.value) * 8 + 20;
  // Xác định góc xoay của từ (ngẫu nhiên 0 độ hoặc -90 độ)
  const rotate = () => (Math.random() > 0.5 ? 0 : -90);

  return (
    <div className="panel metrics-panel">
      <h2 className="panel-title">Thống kê Tổng quan</h2>
      {history.length > 0 ? (
        <>
          {/* Biểu đồ tròn (Giữ nguyên) */}
          <div className="chart-container">
            <h3>Phân bổ cảm xúc</h3>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60} label>
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
                  ))}
                </Pie>
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
          
          {/* Word Clouds (Đã cập nhật) */}
          <div className="word-clouds-container">
            {wordCloudData.positive.length > 0 && 
              <div className="word-cloud">
                <h3 className="sentiment-positive">Từ khóa tích cực</h3>
                {/* Sử dụng component WordCloud mới và truyền props */}
                <WordCloud
                  data={wordCloudData.positive}
                  fontSize={fontSizeMapper}
                  rotate={rotate}
                  padding={2}
                />
              </div>
            }
            {wordCloudData.negative.length > 0 &&
              <div className="word-cloud">
                <h3 className="sentiment-negative">Từ khóa tiêu cực</h3>
                {/* Sử dụng component WordCloud mới và truyền props */}
                <WordCloud
                  data={wordCloudData.negative}
                  fontSize={fontSizeMapper}
                  rotate={rotate}
                  padding={2}
                />
              </div>
            }
          </div>
        </>
      ) : (
        <p className="placeholder-text">Chưa có đủ dữ liệu để thống kê.</p>
      )}
    </div>
  );
});

export default MetricsPanel;