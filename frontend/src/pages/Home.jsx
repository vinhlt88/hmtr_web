import { useNavigate } from 'react-router-dom';
import { Trophy, Volleyball, Activity, Sparkles, Tv, HelpCircle } from 'lucide-react';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();

  const sports = [
    {
      id: 'mens_football',
      name: 'Bóng Đá Nam',
      desc: '21 Đội • 5 Bảng',
      icon: <Trophy size={46} />,
      type: 'primary',
      active: true,
      accent: 'red'
    },
    {
      id: 'womens_football',
      name: 'Bóng Đá Nữ',
      desc: '8 Đội • 2 Bảng',
      icon: <Trophy size={46} />,
      type: 'primary',
      active: true,
      accent: 'blue'
    },
    {
      id: 'badminton_male',
      name: 'Cầu Lông - Đôi Nam',
      desc: 'Sắp ra mắt',
      icon: <Activity size={32} />,
      type: 'ghost',
      active: false
    },
    {
      id: 'badminton_female',
      name: 'Cầu Lông - Đôi Nữ',
      desc: 'Sắp ra mắt',
      icon: <Activity size={32} />,
      type: 'ghost',
      active: false
    },
    {
      id: 'badminton_mixed',
      name: 'Cầu Lông - Đôi Nam Nữ',
      desc: 'Sắp ra mắt',
      icon: <Activity size={32} />,
      type: 'ghost',
      active: false
    },
    {
      id: 'volleyball_male',
      name: 'Bóng Chuyền Nam',
      desc: 'Sắp ra mắt',
      icon: <Volleyball size={32} />,
      type: 'ghost',
      active: false
    },
    {
      id: 'volleyball_female',
      name: 'Bóng Chuyền Nữ',
      desc: 'Sắp ra mắt',
      icon: <Volleyball size={32} />,
      type: 'ghost',
      active: false
    }
  ];

  const activeSports = sports.filter(s => s.active);
  const upcomingSports = sports.filter(s => !s.active);

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
        <div className="live-tv-badge">
          <Tv size={16} className="tv-icon" />
          <span>LIVE BROADCAST MODE</span>
        </div>
        <h1 className="title-premium">
          <span className="main-title">PHONG TRÀO HÈ TRUYỀN THỐNG</span>
          <span className="sub-title-gold">HAMU TANRAN 2026</span>
        </h1>
        <div className="draw-title-container">
          <div className="draw-line-left"></div>
          <div className="draw-title-glow">
            <span className="live-dot"></span>
            LỄ BỐC THĂM CHIA BẢNG
          </div>
          <div className="draw-line-right"></div>
        </div>
      </header>

      <main className="home-content-split">
        {/* Active Arena: Big Cards */}
        <section className="active-arena">
          <div className="section-label">
            <Sparkles size={16} className="spark-icon" />
            <span>GIẢI ĐẤU ĐANG BỐC THĂM</span>
          </div>
          <div className="active-cards-grid">
            {activeSports.map((sport) => (
              <div 
                key={sport.id}
                className={`premium-card active-card accent-${sport.accent}`}
                onClick={() => navigate(`/draw/${sport.id}`)}
              >
                <div className="card-shine"></div>
                <div className="card-glowing-border"></div>
                
                <div className="card-top">
                  <div className="sport-badge">SOCCER</div>
                  <div className="card-icon-glow">
                    {sport.icon}
                  </div>
                </div>

                <div className="card-body">
                  <h2 className="sport-title">{sport.name}</h2>
                  <div className="sport-meta">
                    <span className="meta-teams">{sport.desc.split('•')[0].trim()}</span>
                    <span className="meta-divider">•</span>
                    <span className="meta-groups">{sport.desc.split('•')[1].trim()}</span>
                  </div>
                </div>

                <div className="card-footer">
                  <button className="draw-action-btn">
                    <span>BẮT ĐẦU BỐC THĂM</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="arrow-icon">
                      <path d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Upcoming Arena: Slim Row */}
        <section className="upcoming-arena">
          <div className="section-label-muted">CÁC HẠNG MỤC THI ĐẤU TIẾP THEO</div>
          <div className="upcoming-list">
            {upcomingSports.map((sport) => (
              <div key={sport.id} className="premium-card upcoming-card">
                <div className="upcoming-icon">
                  {sport.icon}
                </div>
                <div className="upcoming-info">
                  <h4>{sport.name}</h4>
                  <span className="badge-upcoming">Đang chuẩn bị</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className="home-footer-dark">
        <p>© 2026 Hamu Tanran Sports Event Committee • Designed for Big Screen TV</p>
      </footer>
    </div>
  );
};

export default Home;
