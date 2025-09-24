import React, { useState, useRef, useEffect, Suspense, lazy } from 'react';
import './App.css';

// TỐI ƯU: Sử dụng React.lazy để tải Dashboard component khi cần thiết.
// Thao tác này sẽ chỉ bắt đầu sau khi người dùng tương tác với màn hình chờ.
const Dashboard = lazy(() => import('./Dashboard'));

function App() {
  // State để kiểm tra người dùng đã tương tác (nhấp chuột) hay chưa
  const [userInteracted, setUserInteracted] = useState(false);

  // Ref để tham chiếu đến thẻ <audio>
  const audioRef = useRef(null);

  // useEffect này sẽ chạy khi `userInteracted` thay đổi từ false -> true
  useEffect(() => {
    // Nếu người dùng đã nhấp chuột và thẻ audio đã sẵn sàng...
    if (userInteracted && audioRef.current) {
      // Đặt âm lượng
      audioRef.current.volume = 0.3;
      
      // Bắt đầu phát nhạc và bắt lỗi nếu trình duyệt chặn
      audioRef.current.play().catch(error => {
        console.error("Lỗi khi cố gắng phát âm thanh:", error);
      });
    }
  }, [userInteracted]); // Phụ thuộc vào state `userInteracted`

  // Hàm xử lý sự kiện khi người dùng nhấp vào màn hình chờ
  const handleStartInteraction = () => {
    setUserInteracted(true);
  };

  // Nếu người dùng chưa tương tác, hiển thị màn hình chờ
  if (!userInteracted) {
    return (
      <div className="start-screen" onClick={handleStartInteraction}>
        <div className="start-content">
          <img src="/assets/logo.png" alt="Logo" className="app-logo" />
          <h1>Phân tích cảm xúc Tweet</h1>
          <p>Nhấn vào bất kỳ đâu để bắt đầu!</p>
        </div>
      </div>
    );
  }

  // Sau khi người dùng đã tương tác, hiển thị giao diện chính của ứng dụng
  return (
    <div className="App">
      <audio
        ref={audioRef}
        src="/assets/music.mp3"
        loop
      />
      
      <header className="app-header">
        <img src="/assets/logo.png" alt="BrandPulse Logo" className="app-logo" />
        <h1>Phân tích cảm xúc Tweet</h1>
      </header>
      <main>
        {/*
          TỐI ƯU: Bọc Dashboard trong Suspense.
          Nó sẽ hiển thị một thông báo fallback trong khi đợi tệp Dashboard.js và các component con của nó được tải về.
        */}
        <Suspense fallback={<div className="loading-dashboard">Đang tải giao diện...</div>}>
          <Dashboard />
        </Suspense>
      </main>
    </div>
  );
}

export default App;