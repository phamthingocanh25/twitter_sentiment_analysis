import React from 'react';
import { RadialBarChart, RadialBar, PolarAngleAxis, ResponsiveContainer } from 'recharts';

// TỐI ƯU: Bọc toàn bộ component trong React.memo
const ResultGauge = React.memo(({ result }) => {
  if (!result) {
    return (
      <div className="panel result-gauge-panel">
        <h2 className="panel-title">Kết quả Phân tích</h2>
        <div className="gauge-placeholder">
          <p>Kết quả sẽ được hiển thị ở đây...</p>
        </div>
      </div>
    );
  }

  // SỬA LỖI: Đọc đúng thuộc tính sentiment từ API
  const isPositive = result.tweets[0].sentiment === 'Positive';
  
  // SỬA LỖI: Lấy đúng phần trăm độ tin cậy
  const confidence = Math.round(
    isPositive ? result.positive_percentage : result.negative_percentage
  );
  
  const data = [{ name: 'Confidence', value: confidence }];

  // Cải tiến: Tự động lấy màu từ file CSS để đồng bộ
  const positiveColor = getComputedStyle(document.documentElement).getPropertyValue('--positive-color').trim();
  const negativeColor = getComputedStyle(document.documentElement).getPropertyValue('--negative-color').trim();
  const barColor = isPositive ? positiveColor : negativeColor;

  return (
    <div className="panel result-gauge-panel">
      <h2 className="panel-title">Kết quả Phân tích</h2>
      <ResponsiveContainer width="100%" height={200}>
        <RadialBarChart
          innerRadius="70%"
          outerRadius="100%"
          data={data}
          startAngle={180}
          endAngle={0}
          barSize={30}
        >
          <PolarAngleAxis
            type="number"
            domain={[0, 100]}
            angleAxisId={0}
            tick={false}
          />
          <RadialBar
            background
            clockWise
            dataKey="value"
            cornerRadius={15}
            fill={barColor}
          />
          <text
            x="50%"
            y="55%"
            textAnchor="middle"
            dominantBaseline="middle"
            className="gauge-percentage" 
          >
            {`${confidence}%`}
          </text>
        </RadialBarChart>
      </ResponsiveContainer>
      {/* Hiển thị nhãn Tích cực/Tiêu cực dựa trên biến isPositive */}
      <div className={`gauge-sentiment ${isPositive ? 'sentiment-positive' : 'sentiment-negative'}`}>
        {isPositive ? 'Tích cực' : 'Tiêu cực'}
      </div>
    </div>
  );
});

export default ResultGauge;
