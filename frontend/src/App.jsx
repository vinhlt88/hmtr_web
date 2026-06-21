import { useState } from 'react';
import { BrowserRouter, Routes, Route, useParams } from 'react-router-dom';
import { Lock, ArrowRight, ShieldAlert } from 'lucide-react';
import Home from './pages/Home';
import DrawDashboard from './pages/DrawDashboard';

const DrawDashboardWrapper = () => {
  const { sport } = useParams();
  return <DrawDashboard key={sport} />;
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem('hmtr_auth_2026') === 'true';
  });
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === 'hmtr2026') {
      localStorage.setItem('hmtr_auth_2026', 'true');
      setIsAuthenticated(true);
      setError(false);
    } else {
      setError(true);
      setPassword('');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="lock-screen dark-theme">
        <div className="ambient-glow glow-1"></div>
        <div className="ambient-glow glow-2"></div>
        <div className="lock-card">
          <div className="lock-icon-wrapper">
            <Lock className="lock-icon" size={36} />
          </div>
          <h2 className="lock-title">HAMU TANRAN 2026</h2>
          <p className="lock-subtitle">Nhập mật khẩu để truy cập hệ thống bốc thăm</p>
          
          <form onSubmit={handleSubmit} className="lock-form">
            <div className={`input-wrapper ${error ? 'shake-error' : ''}`}>
              <input
                type="password"
                placeholder="Mật khẩu truy cập"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (error) setError(false);
                }}
                autoFocus
                className="lock-input"
              />
              <button type="submit" className="lock-submit-btn">
                <ArrowRight size={20} />
              </button>
            </div>
            {error && (
              <div className="error-message">
                <ShieldAlert size={16} /> Mật khẩu không chính xác!
              </div>
            )}
          </form>
        </div>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/draw/:sport" element={<DrawDashboardWrapper />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
