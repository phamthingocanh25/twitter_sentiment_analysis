import React, { useState, useRef, useEffect, Suspense, lazy } from 'react';
import './App.css';

// 1. IMPORT CÁC FILE ASSET TRỰC TIẾP VÀO CODE
import logo from './assets/logo.png'; 
import backgroundMusic from './assets/music.mp3';

// TỐI ƯU: Sử dụng React.lazy để tải Dashboard component khi cần thiết.
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
          {/* 2. SỬ DỤNG BIẾN 'logo' ĐÃ IMPORT */}
          <img src={logo} alt="Logo" className="app-logo" />
          <h1>Phân tích cảm xúc Tweet</h1>
          <p>Hãy cùng Team "Mai Làm" bắt đầu phân tích nhé! </p>
        </div>
      </div>
    );
  }

  // Sau khi người dùng đã tương tác, hiển thị giao diện chính của ứng dụng
  return (
    <div className="App">
      <audio
        ref={audioRef}
        // 3. SỬ DỤNG BIẾN 'backgroundMusic' ĐÃ IMPORT
        src={backgroundMusic}
        loop
      />
      
      <header className="app-header">
        {/* 4. SỬ DỤNG LẠI BIẾN 'logo' */}
        <img src={logo} alt="BrandPulse Logo" className="app-logo" />
        <h1>Phân tích cảm xúc Tweet</h1>
      </header>
      <main>
        {/*
          TỐI ƯU: Bọc Dashboard trong Suspense.
          Nó sẽ hiển thị một thông báo fallback trong khi đợi tải component Dashboard.
        */}
        <Suspense fallback={<div className="loading-fallback">Đang tải dashboard...</div>}>
          <Dashboard />
        </Suspense>
      </main>
    </div>
  );
}

export default App;