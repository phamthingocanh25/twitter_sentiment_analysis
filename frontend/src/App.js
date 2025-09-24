// frontend/src/App.js

import React, { useState, useRef, useEffect, Suspense, lazy } from 'react';
import './App.css';

// SỬA LỖI 1: Import trực tiếp logo và file nhạc
import logo from './assets/logo.png';
import backgroundMusic from './assets/music.mp3'; // Đảm bảo file music.mp3 có trong thư mục 'src/assets'

const Dashboard = lazy(() => import('./Dashboard'));

function App() {
  const [userInteracted, setUserInteracted] = useState(false);
  const audioRef = useRef(null);

  useEffect(() => {
    if (userInteracted && audioRef.current) {
      audioRef.current.volume = 0.3;
      audioRef.current.play().catch(error => {
        console.error("Lỗi khi phát nhạc:", error);
      });
    }
  }, [userInteracted]);

  const handleStartInteraction = () => {
    setUserInteracted(true);
  };

  if (!userInteracted) {
    return (
      <div className="start-screen" onClick={handleStartInteraction}>
        <div className="start-content">
          {/* SỬA LỖI 2: Dùng biến logo đã import */}
          <img src={logo} alt="Logo" className="app-logo" />
          <h1>Phân tích cảm xúc Tweet</h1>
          <p>Hãy cùng Team "Mai Làm" bắt đầu phân tích nhé! </p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <audio
        ref={audioRef}
        // SỬA LỖI 3: Dùng biến backgroundMusic đã import
        src={backgroundMusic}
        loop
      />
      
      <header className="app-header">
        {/* SỬA LỖI 4: Dùng lại biến logo */}
        <img src={logo} alt="BrandPulse Logo" className="app-logo" />
        <h1>Phân tích cảm xúc Tweet</h1>
      </header>
      <main>
        <Suspense fallback={<div className="loading-fallback">Đang tải dashboard...</div>}>
          <Dashboard />
        </Suspense>
      </main>
    </div>
  );
}

export default App;