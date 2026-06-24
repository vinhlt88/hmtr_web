import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Trophy, Volleyball, Activity, Sparkles, Tv, Lock, CheckCircle2, RotateCcw, Unlock } from 'lucide-react';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();
  const [completedSports, setCompletedSports] = useState({});
  const [freeDrawMode, setFreeDrawMode] = useState(false);

  const sportsOrder = [
    {
      id: 'badminton_male',
      name: 'Cầu Lông - Đôi Nam',
      desc: '12 Đôi • 4 Bảng',
      icon: <Activity size={36} />,
      accent: 'yellow',
      category: 'badminton',
      catLabel: 'CẦU LÔNG'
    },
    {
      id: 'badminton_female',
      name: 'Cầu Lông - Đôi Nữ',
      desc: '9 Đôi • 2 Bảng',
      icon: <Activity size={36} />,
      accent: 'yellow',
      category: 'badminton',
      catLabel: 'CẦU LÔNG'
    },
    {
      id: 'badminton_mixed',
      name: 'Cầu Lông - Đôi Nam Nữ',
      desc: '10 Đôi • 2 Bảng',
      icon: <Activity size={36} />,
      accent: 'yellow',
      category: 'badminton',
      catLabel: 'CẦU LÔNG'
    },
    {
      id: 'volleyball_male',
      name: 'Bóng Chuyền Nam',
      desc: '6 Đội • 2 Bảng',
      icon: <Volleyball size={36} />,
      accent: 'orange',
      category: 'volleyball',
      catLabel: 'BÓNG CHUYỀN'
    },
    {
      id: 'volleyball_female',
      name: 'Bóng Chuyền Nữ',
      desc: '6 Đội • 2 Bảng',
      icon: <Volleyball size={36} />,
      accent: 'orange',
      category: 'volleyball',
      catLabel: 'BÓNG CHUYỀN'
    },
    {
      id: 'womens_football',
      name: 'Bóng Đá Nữ',
      desc: '11 Đội • 2 Bảng',
      icon: <Trophy size={40} />,
      accent: 'blue',
      category: 'football',
      catLabel: 'BÓNG ĐÁ'
    },
    {
      id: 'mens_football',
      name: 'Bóng Đá Nam',
      desc: '20 Đội • 5 Bảng',
      icon: <Trophy size={40} />,
      accent: 'red',
      category: 'football',
      catLabel: 'BÓNG ĐÁ'
    }
  ];

  // Load completed state from localStorage
  const loadProgress = () => {
    const completed = {};
    sportsOrder.forEach(sport => {
      completed[sport.id] = localStorage.getItem(`draw_completed_${sport.id}`) === 'true';
    });
    setCompletedSports(completed);
  };

  useEffect(() => {
    loadProgress();
  }, []);

  // Determine which sport is currently active
  let activeIndex = sportsOrder.findIndex(sport => !completedSports[sport.id]);
  if (activeIndex === -1 && Object.keys(completedSports).length > 0) {
    activeIndex = sportsOrder.length; // all completed
  }

  const getSportState = (sportId, index) => {
    if (completedSports[sportId]) return 'completed';
    if (index === activeIndex) return 'active';
    if (freeDrawMode) return 'free'; // Special state: unlocked under free draw mode
    return 'locked';
  };

  const handleCardClick = (sport, state) => {
    if (state !== 'locked') {
      navigate(`/draw/${sport.id}`);
    }
  };

  const handleToggleFreeDraw = () => {
    setFreeDrawMode(prev => !prev);
  };

  const handleResetProgress = () => {
    if (window.confirm('Đặt lại toàn bộ tiến trình bốc thăm? (Tất cả các môn sẽ quay lại trạng thái chờ bốc thăm)')) {
      sportsOrder.forEach(sport => {
        localStorage.removeItem(`draw_completed_${sport.id}`);
        localStorage.removeItem(`draw_assigned_${sport.id}`);
        localStorage.removeItem(`draw_unassigned_${sport.id}`);
        localStorage.removeItem(`draw_slots_${sport.id}`);
      });
      loadProgress();
    }
  };

  // Group sports by category
  const categories = {
    badminton: {
      title: 'Cụm 1: Cầu Lông',
      subtitle: 'Bốc thăm trước',
      accent: 'yellow',
      items: sportsOrder.filter(s => s.category === 'badminton')
    },
    volleyball: {
      title: 'Cụm 2: Bóng Chuyền',
      subtitle: 'Bốc thăm giữa',
      accent: 'orange',
      items: sportsOrder.filter(s => s.category === 'volleyball')
    },
    football: {
      title: 'Cụm 3: Bóng Đá',
      subtitle: 'Nữ trước, Nam sau',
      accent: 'football-glow',
      items: sportsOrder.filter(s => s.category === 'football')
    }
  };

  return (
    <div className="home-container app-container dark-theme">
      {/* Ambient background particles & glows */}
      <div className="ambient-glow glow-1"></div>
      <div className="ambient-glow glow-2"></div>
      <div className="ambient-glow glow-3"></div>
      
      <div className="particles-container">
        {[...Array(12)].map((_, i) => (
          <div key={i} className={`particle particle-${i + 1}`}></div>
        ))}
      </div>

      <header className="home-header">
        <div className="header-top-line">
          <div className="live-tv-badge">
            <Tv size={16} className="tv-icon" />
            <span>LIVE BROADCAST MODE</span>
          </div>

          <div className="header-admin-actions">
            <button 
              className={`free-draw-toggle-btn ${freeDrawMode ? 'active-mode' : ''}`} 
              onClick={handleToggleFreeDraw}
              title="Mở khóa tất cả các môn bốc thăm khẩn cấp"
            >
              <span className="toggle-dot"></span>
              <span>BỐC TỰ DO: {freeDrawMode ? 'BẬT' : 'TẮT'}</span>
            </button>
            
            <button className="reset-progress-btn" onClick={handleResetProgress} title="Đặt lại toàn bộ tiến trình">
              <RotateCcw size={14} />
              <span>Đặt Lại Lộ Trình</span>
            </button>
          </div>
        </div>

        <h1 className="title-premium">
          <span className="main-title">PHONG TRÀO HÈ TRUYỀN THỐNG</span>
          <span className="sub-title-gold">HAMU TANRAN 2026</span>
        </h1>
        
        <div className="draw-title-container">
          <div className="draw-line-left"></div>
          <div className="draw-title-glow">
            <span className="live-dot"></span>
            LỘ TRÌNH LỄ BỐC THĂM CHIA BẢNG
          </div>
          <div className="draw-line-right"></div>
        </div>
      </header>

      <main className="roadmap-container">
        {Object.entries(categories).map(([catKey, cat], catIdx) => (
          <div key={catKey} className={`roadmap-category-block block-${catKey}`}>
            <div className="category-header-glow">
              <div className="cat-title">{cat.title}</div>
              <div className="cat-subtitle">{cat.subtitle}</div>
            </div>

            <div className="category-cards-list">
              {cat.items.map((sport) => {
                const globalIndex = sportsOrder.findIndex(s => s.id === sport.id);
                const state = getSportState(sport.id, globalIndex);
                
                return (
                  <div 
                    key={sport.id}
                    className={`roadmap-card state-${state} accent-${sport.accent}`}
                    onClick={() => handleCardClick(sport, state)}
                  >
                    <div className="card-shine"></div>
                    <div className="card-status-indicator">
                      {state === 'completed' && <CheckCircle2 className="icon-completed" size={20} />}
                      {state === 'active' && <span className="live-badge-glow">LIVE</span>}
                      {state === 'free' && <Unlock className="icon-free-draw" size={16} />}
                      {state === 'locked' && <Lock className="icon-locked" size={16} />}
                    </div>

                    <div className="roadmap-card-body">
                      <div className="card-icon-wrapper">
                        {sport.icon}
                      </div>
                      <div className="card-text-wrapper">
                        <h3>{sport.name}</h3>
                        <p>{state === 'locked' ? 'Chờ đến lượt bốc' : sport.desc}</p>
                      </div>
                    </div>

                    {state === 'active' && (
                      <div className="card-footer-action">
                        <span>BẮT ĐẦU NGAY</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="arrow-icon">
                          <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                      </div>
                    )}
                    {state === 'free' && (
                      <div className="card-footer-free">
                        <span>BỐC TỰ DO</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="arrow-icon">
                          <path d="M5 12h14M12 5l7 7-7 7" />
                        </svg>
                      </div>
                    )}
                    {state === 'completed' && (
                      <div className="card-footer-completed">
                        <span>XEM KẾT QUẢ</span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
            
            {catIdx < 2 && (
              <div className="roadmap-connector">
                <div className="connector-line"></div>
                <div className="connector-arrow"></div>
              </div>
            )}
          </div>
        ))}
      </main>

      <footer className="home-footer-dark">
        {activeIndex === sportsOrder.length ? (
          <p className="success-banner">🎉 TẤT CẢ CÁC MÔN THI ĐẤU ĐÃ HOÀN THÀNH BỐC THĂM TRỌN VẸN! 🎉</p>
        ) : (
          <p>© 2026 Hamu Tanran Sports Event Committee • Designed for Big Screen TV</p>
        )}
      </footer>
    </div>
  );
};

export default Home;
