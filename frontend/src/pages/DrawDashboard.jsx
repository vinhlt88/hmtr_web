import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Confetti from 'react-confetti';
import { ArrowLeft, Calendar, Clock, RotateCcw, Download, Info, Trophy } from 'lucide-react';
import { MOCK_TEAMS, MOCK_GROUPS, MOCK_SCHEDULE } from '../mockData';
import * as XLSX from 'xlsx';
import './DrawDashboard.css';

// Audio Context Manager
let audioCtx = null;
const initAudio = () => {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
};

const playSound = (type) => {
  try {
    initAudio();
    if (!audioCtx) return;
    const ctx = audioCtx;
    const now = ctx.currentTime;
    
    if (type === 'click') {
      // Soft mechanical click - warm and low pitch to build tension without harshness
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      
      osc.type = 'sine';
      osc.frequency.setValueAtTime(250, now);
      osc.frequency.exponentialRampToValueAtTime(80, now + 0.03);
      
      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.03);
      
      osc.connect(gain);
      gain.connect(ctx.destination);
      
      osc.start(now);
      osc.stop(now + 0.03);
    } else if (type === 'reveal') {
      // Classic triumphant "Ta-Da!" fanfare
      const playNote = (freq, start, duration, volume = 0.05) => {
        const osc = ctx.createOscillator();
        const subOsc = ctx.createOscillator();
        const gainNode = ctx.createGain();
        
        osc.type = 'triangle'; // Warm synth brass tone
        osc.frequency.setValueAtTime(freq, start);
        
        subOsc.type = 'sine'; // Pure base body
        subOsc.frequency.setValueAtTime(freq, start);
        
        gainNode.gain.setValueAtTime(0, start);
        gainNode.gain.linearRampToValueAtTime(volume, start + 0.02); // Fast attack for tada pop
        gainNode.gain.exponentialRampToValueAtTime(0.001, start + duration);
        
        osc.connect(gainNode);
        subOsc.connect(gainNode);
        gainNode.connect(ctx.destination);
        
        osc.start(start);
        osc.stop(start + duration);
        subOsc.start(start);
        subOsc.stop(start + duration);
      };
      
      // "Ta-Da!" fanfare timing: G4 -> G4 -> C major chord (longer sustain)
      playNote(392.00, now, 0.12, 0.04);          // Ta (G4)
      playNote(392.00, now + 0.12, 0.12, 0.04);   // Da (G4)
      
      // Congrats Chord! (extended to 2.5s)
      playNote(523.25, now + 0.24, 2.5, 0.06);    // C5
      playNote(659.25, now + 0.24, 2.5, 0.04);    // E5
      playNote(783.99, now + 0.24, 2.5, 0.04);    // G5
      playNote(1046.50, now + 0.24, 2.5, 0.03);   // C6 (high sparkling bell tone)
    }
  } catch (e) {
    console.warn("Audio failed", e);
  }
};

const sportNames = {
  badminton_male: 'Cầu Lông - Đôi Nam',
  badminton_female: 'Cầu Lông - Đôi Nữ',
  badminton_mixed: 'Cầu Lông - Đôi Nam Nữ',
  volleyball_male: 'Bóng Chuyền Nam',
  volleyball_female: 'Bóng Chuyền Nữ',
  womens_football: 'Bóng Đá Nữ',
  mens_football: 'Bóng Đá Nam'
};

const DrawDashboard = () => {
  const { sport } = useParams();
  const navigate = useNavigate();
  const [windowDimension, setWindowDimension] = useState({ width: window.innerWidth, height: window.innerHeight });

  const initialTeams = MOCK_TEAMS[sport] || [];
  const initialGroups = MOCK_GROUPS[sport] || [];
  
  const allSlots = [];
  initialGroups.forEach(g => {
    for (let i = 1; i <= g.capacity; i++) {
      allSlots.push(`${g.id}${i}`);
    }
  });

  const [unassignedTeams, setUnassignedTeams] = useState(initialTeams);
  const [availableSlots, setAvailableSlots] = useState(allSlots);
  const [assigned, setAssigned] = useState({}); 
  const [drawState, setDrawState] = useState('IDLE'); 
  const [displayTeam, setDisplayTeam] = useState(null);
  const [displaySlot, setDisplaySlot] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [lastAssignedSlot, setLastAssignedSlot] = useState(null);

  useEffect(() => {
    const handleResize = () => setWindowDimension({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    if (unassignedTeams.length === 0 && initialTeams.length > 0) {
      localStorage.setItem(`draw_completed_${sport}`, 'true');
    }
  }, [unassignedTeams, initialTeams, sport]);

  const handleStartDraw = () => {
    if (unassignedTeams.length === 0) return;
    initAudio();
    setDrawState('RANDOMIZING_TEAM');
    
    const maxSteps = 22;
    
    const roll = (currentStep, delay) => {
      const idx = Math.floor(Math.random() * unassignedTeams.length);
      const team = unassignedTeams[idx];
      setDisplayTeam(team);
      playSound('click');
      
      if (currentStep < maxSteps) {
        let nextDelay = 35;
        if (currentStep > 10) {
          nextDelay = 35 + Math.pow(currentStep - 10, 1.85) * 9;
        }
        setTimeout(() => roll(currentStep + 1, nextDelay), delay);
      } else {
        const finalIdx = Math.floor(Math.random() * unassignedTeams.length);
        const finalTeam = unassignedTeams[finalIdx];
        setDisplayTeam(finalTeam);
        setSelectedTeam(finalTeam);
        setDrawState('TEAM_REVEALED');
      }
    };
    
    roll(0, 35);
  };

  const handleDrawSlot = () => {
    if (availableSlots.length === 0) return;
    initAudio();
    setDrawState('RANDOMIZING_SLOT');
    
    const maxSteps = 24;
    
    const roll = (currentStep, delay) => {
      const idx = Math.floor(Math.random() * availableSlots.length);
      const slot = availableSlots[idx];
      setDisplaySlot(slot);
      playSound('click');
      
      if (currentStep < maxSteps) {
        let nextDelay = 35;
        if (currentStep > 10) {
          nextDelay = 35 + Math.pow(currentStep - 10, 1.85) * 9;
        }
        setTimeout(() => roll(currentStep + 1, nextDelay), delay);
      } else {
        const finalIdx = Math.floor(Math.random() * availableSlots.length);
        const finalSlot = availableSlots[finalIdx]; 
        
        setDisplaySlot(finalSlot);
        setSelectedSlot(finalSlot);
        
        setAssigned(prev => ({ ...prev, [finalSlot]: selectedTeam }));
        setUnassignedTeams(prev => prev.filter(t => t.id !== selectedTeam.id));
        setAvailableSlots(prev => prev.filter(s => s !== finalSlot));
        setLastAssignedSlot(finalSlot);
        
        setDrawState('SLOT_REVEALED');
        playSound('reveal');
      }
    };
    
    roll(0, 35);
  };

  const resetDraw = () => {
    const confirm1 = window.confirm('Bạn có muốn đặt lại toàn bộ kết quả bốc thăm của giải đấu này?');
    if (confirm1) {
      const confirm2 = window.confirm('CẢNH BÁO QUAN TRỌNG: Hành động này sẽ XÓA SẠCH toàn bộ kết quả hiện tại và không thể khôi phục! Bạn có thực sự chắc chắn không?');
      if (confirm2) {
        setUnassignedTeams(initialTeams);
        setAvailableSlots(allSlots);
        setAssigned({});
        setDrawState('IDLE');
        setSelectedTeam(null);
        setSelectedSlot(null);
        setLastAssignedSlot(null);
        localStorage.removeItem(`draw_completed_${sport}`);
      }
    }
  };

  const exportResults = () => {
    const data = [];
    initialGroups.forEach(group => {
      for (let i = 1; i <= group.capacity; i++) {
        const slotId = `${group.id}${i}`;
        const team = assigned[slotId];
        data.push({ "Bảng": group.id, "Vị trí": slotId, "Đội bóng": team ? team.name : "---" });
      }
    });
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Kết quả");
    XLSX.writeFile(wb, `KetQua_BocTham_${sport}.xlsx`);
  };

  const handleNext = () => {
    setSelectedTeam(null);
    setSelectedSlot(null);
    setDrawState('IDLE');
  };

  return (
    <div className={`draw-layout dark-theme draw-layout-${sport}`}>
      {/* Ambient background particles & glows */}
      <div className="ambient-glow glow-1"></div>
      <div className="ambient-glow glow-2"></div>
      <div className="ambient-glow glow-3"></div>
      
      <div className="particles-container">
        {[...Array(12)].map((_, i) => (
          <div key={i} className={`particle particle-${i + 1}`}></div>
        ))}
      </div>

      {drawState === 'SLOT_REVEALED' && <Confetti width={windowDimension.width} height={windowDimension.height} recycle={false} numberOfPieces={300} />}
      
      <header className="top-bar">
        <button className="back-btn" onClick={() => navigate('/')}>
          <ArrowLeft size={20} /> QUAY LẠI
        </button>
        
        <div className="header-title-wrapper">
          <p className="header-subtitle">Lễ Bốc Thăm Chia Bảng</p>
          <h1 className="header-title">{sportNames[sport]?.toUpperCase() || 'GIẢI ĐẤU'} - HAMU TANRAN 2026</h1>
        </div>

        <div className="top-actions">
          <button className="icon-btn danger" onClick={resetDraw} title="Đặt lại">
            <RotateCcw size={20} />
          </button>
        </div>
      </header>

      <main className="main-content">
        <section className="draw-arena">
          <div className="arena-header">
            <span className="arena-status">
              {drawState === 'IDLE' && 'Sẵn sàng'}
              {drawState === 'RANDOMIZING_TEAM' && 'Đang chọn đội...'}
              {drawState === 'TEAM_REVEALED' && 'Chọn vị trí'}
              {drawState === 'RANDOMIZING_SLOT' && 'Đang bốc thăm...'}
              {drawState === 'SLOT_REVEALED' && 'Kết quả!'}
            </span>
          </div>

          <div className="arena-body">
            {drawState === 'IDLE' && unassignedTeams.length > 0 && (
              <button className="huge-btn" onClick={handleStartDraw}>BẮT ĐẦU BỐC THĂM</button>
            )}

            {drawState === 'IDLE' && unassignedTeams.length === 0 && Object.keys(assigned).length > 0 && (
              <div className="draw-finished-container">
                <Trophy className="trophy-finished-icon" size={80} />
                <h2 className="finished-title">BỐC THĂM HOÀN THÀNH</h2>
                <p className="finished-subtitle">Bảng đấu đã được thiết lập thành công</p>
                <button className="huge-btn download-btn" onClick={exportResults}>
                  <Download size={22} className="download-icon" /> TẢI FILE EXCEL
                </button>
              </div>
            )}

            {drawState === 'RANDOMIZING_TEAM' && (
              <div className="randomizing-container">
                <p className="random-text">{displayTeam?.name}</p>
              </div>
            )}

            {drawState === 'TEAM_REVEALED' && (
              <div className="revealed-card">
                <p className="revealed-team-title">
                  {sport.includes('badminton') ? 'Cặp đấu tiếp theo:' : 'Đội bóng tiếp theo:'}
                </p>
                <h2 className="revealed-text">{selectedTeam?.name}</h2>
                <button className="huge-btn mt-4" onClick={handleDrawSlot}>BỐC THĂM</button>
              </div>
            )}

            {drawState === 'RANDOMIZING_SLOT' && (
              <div className="randomizing-container">
                <p className="random-text">{displaySlot}</p>
              </div>
            )}

            {drawState === 'SLOT_REVEALED' && (
              <div className="slot-reveal-container">
                <div className="revealed-card">
                  <p className="revealed-team-title">
                    {sport.includes('badminton') ? 'CẶP ĐẤU' : 'ĐỘI BÓNG'} {selectedTeam?.name?.toUpperCase()}
                  </p>
                  <div className="slot-result-card">
                    <span className="group-letter">{selectedSlot?.charAt(0)}</span>
                    <span className="pos-number">{selectedSlot?.slice(1)}</span>
                  </div>
                </div>
                <button className="huge-btn" onClick={handleNext}>TIẾP TỤC</button>
              </div>
            )}
          </div>
        </section>

        <section className="draw-board">
          <div className="board-header">
            <h2>DANH SÁCH BẢNG ĐẤU</h2>
            <span className="progress-badge">
              ĐÃ BỐC: {Object.keys(assigned).length}/{initialTeams.length}
            </span>
          </div>

          <div className={`groups-grid sport-${sport}`}>
            {initialGroups.map(group => (
              <div key={group.id} className="group-card">
                <div className="group-header">BẢNG {group.id}</div>
                <div className="group-slots">
                  {Array.from({ length: group.capacity }).map((_, i) => {
                    const sid = `${group.id}${i + 1}`;
                    const team = assigned[sid];
                    return (
                      <div key={sid} className={`slot-item ${team ? 'filled' : ''} ${lastAssignedSlot === sid ? 'newest-assigned' : ''}`}>
                        <span className="slot-id">{sid}</span>
                        <span className="team-name">{team ? team.name : '---'}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className="bottom-bar">
        <span className="bottom-label">
          {sport.includes('badminton') ? 'CÁC CẶP CHƯA BỐC:' : 'CÁC ĐỘI CHƯA BỐC:'}
        </span>
        <div className="pill-container">
          {unassignedTeams.map(t => (
            <span key={t.id} className="team-pill">{t.name}</span>
          ))}
          {unassignedTeams.length === 0 && <span className="team-pill success">Đã hoàn thành bốc thăm!</span>}
        </div>
      </footer>
    </div>
  );
};

export default DrawDashboard;
