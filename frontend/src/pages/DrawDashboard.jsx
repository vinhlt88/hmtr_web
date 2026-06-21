import { useState, useEffect, useRef } from 'react';
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
      // --- LUCKY DRAW PREMIUM FANFARE (~8 SECONDS) ---
      
      // 1. Setup Master Bus with Dynamics Compressor to glue the mix & prevent clipping
      const masterGain = ctx.createGain();
      masterGain.gain.setValueAtTime(0.8, now);
      
      const compressor = ctx.createDynamicsCompressor();
      compressor.threshold.setValueAtTime(-12, now);
      compressor.knee.setValueAtTime(24, now);
      compressor.ratio.setValueAtTime(3, now);
      compressor.attack.setValueAtTime(0.005, now);
      compressor.release.setValueAtTime(0.20, now);
      
      masterGain.connect(compressor);
      compressor.connect(ctx.destination);
      
      // 2. Generate White Noise Buffer for Whoosh & Crash (7.0 seconds duration)
      const bufferSize = ctx.sampleRate * 7.0; 
      const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = noiseBuffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }

      // -- ELEMENT A: Accelerating Ticks (0.0s to 1.4s) --
      for (let i = 0; i < 16; i++) {
        const tickTime = now + 1.4 * (1 - Math.pow((16 - i) / 16, 1.8));
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(250 + i * 20, tickTime);
        osc.frequency.exponentialRampToValueAtTime(60, tickTime + 0.025);
        
        gain.gain.setValueAtTime(0.05, tickTime);
        gain.gain.exponentialRampToValueAtTime(0.001, tickTime + 0.025);
        
        osc.connect(gain);
        gain.connect(masterGain);
        osc.start(tickTime);
        osc.stop(tickTime + 0.025);
      }

      // -- ELEMENT B: Whoosh Sweeper (0.0s to 1.5s) --
      const whooshSource = ctx.createBufferSource();
      whooshSource.buffer = noiseBuffer;
      
      const whooshFilter = ctx.createBiquadFilter();
      whooshFilter.type = 'bandpass';
      whooshFilter.Q.setValueAtTime(2.5, now);
      whooshFilter.frequency.setValueAtTime(80, now);
      whooshFilter.frequency.exponentialRampToValueAtTime(2400, now + 1.5);
      
      const whooshGain = ctx.createGain();
      whooshGain.gain.setValueAtTime(0, now);
      whooshGain.gain.linearRampToValueAtTime(0.045, now + 1.2);
      whooshGain.gain.exponentialRampToValueAtTime(0.001, now + 1.5);
      
      whooshSource.connect(whooshFilter);
      whooshFilter.connect(whooshGain);
      whooshGain.connect(masterGain);
      whooshSource.start(now);

      // -- ELEMENT C: Accelerating Timpani Drum Roll (0.4s to 1.5s) --
      for (let i = 0; i < 20; i++) {
        const hitTime = now + 0.4 + 1.1 * Math.pow(i / 19, 1.6);
        const vol = 0.01 + Math.pow(i / 19, 1.5) * 0.08;
        
        // Mallet hit click (noise transient)
        const transient = ctx.createBufferSource();
        transient.buffer = noiseBuffer;
        const transientFilter = ctx.createBiquadFilter();
        transientFilter.type = 'bandpass';
        transientFilter.frequency.setValueAtTime(200, hitTime);
        transientFilter.Q.setValueAtTime(1.0, hitTime);
        
        const transientGain = ctx.createGain();
        transientGain.gain.setValueAtTime(vol * 0.4, hitTime);
        transientGain.gain.exponentialRampToValueAtTime(0.001, hitTime + 0.015);
        
        transient.connect(transientFilter);
        transientFilter.connect(transientGain);
        transientGain.connect(masterGain);
        transient.start(hitTime);
        transient.stop(hitTime + 0.015);
        
        // Low pitch triangle body
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        
        osc.type = 'triangle';
        const freq = 65 + (i / 19) * 25;
        osc.frequency.setValueAtTime(freq, hitTime);
        osc.frequency.exponentialRampToValueAtTime(freq * 0.8, hitTime + 0.12);
        
        gain.gain.setValueAtTime(vol, hitTime);
        gain.gain.exponentialRampToValueAtTime(0.001, hitTime + 0.12);
        
        osc.connect(gain);
        gain.connect(masterGain);
        osc.start(hitTime);
        osc.stop(hitTime + 0.12);
      }

      // -- ELEMENT D: Cymbal Crash (Hits at 1.5s, decays smoothly to 6.5s) --
      const crashSource = ctx.createBufferSource();
      crashSource.buffer = noiseBuffer;
      
      const crashFilter = ctx.createBiquadFilter();
      crashFilter.type = 'highpass';
      crashFilter.frequency.setValueAtTime(6000, now + 1.5);
      
      const crashGain = ctx.createGain();
      crashGain.gain.setValueAtTime(0, now + 1.5);
      crashGain.gain.linearRampToValueAtTime(0.08, now + 1.52);
      crashGain.gain.exponentialRampToValueAtTime(0.001, now + 6.5);
      
      crashSource.connect(crashFilter);
      crashFilter.connect(crashGain);
      crashGain.connect(masterGain);
      crashSource.start(now + 1.5);

      // -- ELEMENT E: Detuned Synth Brass Horns (Chord Progression C -> Dm -> Em -> F -> Grand C) --
      const playBrass = (freq, start, duration, volume = 0.05) => {
        const oscSaw1 = ctx.createOscillator();
        const oscSaw2 = ctx.createOscillator();
        const oscTri = ctx.createOscillator();
        const filter = ctx.createBiquadFilter();
        const gainNode = ctx.createGain();
        
        oscSaw1.type = 'sawtooth';
        oscSaw1.frequency.setValueAtTime(freq, start);
        oscSaw1.detune.setValueAtTime(-12, start);
        
        oscSaw2.type = 'sawtooth';
        oscSaw2.frequency.setValueAtTime(freq, start);
        oscSaw2.detune.setValueAtTime(12, start);
        
        oscTri.type = 'triangle';
        oscTri.frequency.setValueAtTime(freq, start);
        oscTri.detune.setValueAtTime(0, start);
        
        filter.type = 'lowpass';
        filter.Q.setValueAtTime(1.2, start);
        filter.frequency.setValueAtTime(freq * 4.0, start);
        filter.frequency.exponentialRampToValueAtTime(freq * 1.8, start + 0.15);
        filter.frequency.linearRampToValueAtTime(freq * 1.4, start + duration);
        
        gainNode.gain.setValueAtTime(0, start);
        gainNode.gain.linearRampToValueAtTime(volume, start + 0.04); 
        gainNode.gain.setValueAtTime(volume, start + duration - 0.12);
        gainNode.gain.exponentialRampToValueAtTime(0.001, start + duration);
        
        oscSaw1.connect(filter);
        oscSaw2.connect(filter);
        oscTri.connect(filter);
        filter.connect(gainNode);
        gainNode.connect(masterGain);
        
        oscSaw1.start(start);
        oscSaw1.stop(start + duration);
        oscSaw2.start(start);
        oscSaw2.stop(start + duration);
        oscTri.start(start);
        oscTri.stop(start + duration);
      };

      // 1.5s: C major triad
      playBrass(261.63, now + 1.5, 0.25, 0.035); // C4
      playBrass(329.63, now + 1.5, 0.25, 0.035); // E4
      playBrass(392.00, now + 1.5, 0.25, 0.035); // G4
      
      // 1.8s: D minor triad
      playBrass(293.66, now + 1.8, 0.25, 0.035); // D4
      playBrass(349.23, now + 1.8, 0.25, 0.035); // F4
      playBrass(440.00, now + 1.8, 0.25, 0.035); // A4
      
      // 2.1s: E minor triad
      playBrass(329.63, now + 2.1, 0.25, 0.035); // E4
      playBrass(392.00, now + 2.1, 0.25, 0.035); // G4
      playBrass(493.88, now + 2.1, 0.25, 0.035); // B4
      
      // 2.4s: F major triad
      playBrass(349.23, now + 2.4, 0.35, 0.035); // F4
      playBrass(440.00, now + 2.4, 0.35, 0.035); // A4
      playBrass(523.25, now + 2.4, 0.35, 0.035); // C5
      
      // 2.8s: Grand Final Majestic Chord (Decays over 5.0s)
      playBrass(392.00, now + 2.8, 5.0, 0.035); // G4
      playBrass(523.25, now + 2.8, 5.0, 0.045); // C5
      playBrass(659.25, now + 2.8, 5.0, 0.035); // E5
      playBrass(783.99, now + 2.8, 5.0, 0.035); // G5
      playBrass(1046.50, now + 2.8, 5.0, 0.025); // C6

      // -- ELEMENT F: Sparkling Magical Chimes (Sparkle) (3.0s to 7.5s) --
      const playChime = (freq, start, vol = 0.015) => {
        const osc1 = ctx.createOscillator();
        const osc2 = ctx.createOscillator();
        const gainNode = ctx.createGain();
        
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(freq, start);
        
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(freq * 2.52, start); // inharmonic overtone for realistic metal ring
        
        gainNode.gain.setValueAtTime(0, start);
        gainNode.gain.linearRampToValueAtTime(vol, start + 0.01);
        gainNode.gain.exponentialRampToValueAtTime(0.001, start + 0.4);
        
        osc1.connect(gainNode);
        
        const overtoneGain = ctx.createGain();
        overtoneGain.gain.setValueAtTime(0.3, start);
        osc2.connect(overtoneGain);
        overtoneGain.connect(gainNode);
        
        gainNode.connect(masterGain);
        
        osc1.start(start);
        osc1.stop(start + 0.4);
        osc2.start(start);
        osc2.stop(start + 0.4);
      };

      for (let i = 0; i < 30; i++) {
        const bellTime = now + 3.0 + i * 0.15;
        const freq = 2000 - i * 45 + Math.sin(i * 2.0) * 150;
        playChime(freq, bellTime, 0.015);
      }
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

  const [unassignedTeams, setUnassignedTeams] = useState(() => {
    const saved = localStorage.getItem(`draw_unassigned_${sport}`);
    return saved ? JSON.parse(saved) : initialTeams;
  });
  const [availableSlots, setAvailableSlots] = useState(() => {
    const saved = localStorage.getItem(`draw_slots_${sport}`);
    return saved ? JSON.parse(saved) : allSlots;
  });
  const [assigned, setAssigned] = useState(() => {
    const saved = localStorage.getItem(`draw_assigned_${sport}`);
    return saved ? JSON.parse(saved) : {};
  }); 
  const [drawState, setDrawState] = useState('IDLE'); 
  const [displayTeam, setDisplayTeam] = useState(null);
  const [displaySlot, setDisplaySlot] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [lastAssignedSlot, setLastAssignedSlot] = useState(null);
  const timerRef = useRef(null);

  useEffect(() => {
    const handleResize = () => setWindowDimension({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Auto-fill fallback if marked completed but no saved draw data exists
  useEffect(() => {
    const completedKey = `draw_completed_${sport}`;
    const assignedKey = `draw_assigned_${sport}`;
    
    if (localStorage.getItem(completedKey) === 'true' && !localStorage.getItem(assignedKey)) {
      const tempAssigned = {};
      const tempTeams = [...initialTeams];
      const tempSlots = [...allSlots];
      
      while (tempTeams.length > 0 && tempSlots.length > 0) {
        const teamIdx = Math.floor(Math.random() * tempTeams.length);
        const team = tempTeams.splice(teamIdx, 1)[0];
        
        const slotIdx = Math.floor(Math.random() * tempSlots.length);
        const slot = tempSlots.splice(slotIdx, 1)[0];
        
        tempAssigned[slot] = team;
      }
      
      localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(tempAssigned));
      localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify([]));
      localStorage.setItem(`draw_slots_${sport}`, JSON.stringify(tempSlots));
      
      setAssigned(tempAssigned);
      setUnassignedTeams([]);
      setAvailableSlots(tempSlots);
    }
  }, [sport, initialTeams, allSlots]);

  useEffect(() => {
    if (unassignedTeams.length === 0 && initialTeams.length > 0) {
      localStorage.setItem(`draw_completed_${sport}`, 'true');
    }
  }, [unassignedTeams, initialTeams, sport]);

  const handleStartDraw = () => {
    if (unassignedTeams.length === 0) return;
    initAudio();
    
    // Automatically assign the last team to the last slot
    if (unassignedTeams.length === 1 && availableSlots.length === 1) {
      const lastTeam = unassignedTeams[0];
      const lastSlot = availableSlots[0];
      
      setDisplayTeam(lastTeam);
      setSelectedTeam(lastTeam);
      setDisplaySlot(lastSlot);
      setSelectedSlot(lastSlot);
      
      setAssigned(prev => {
        const next = { ...prev, [lastSlot]: lastTeam };
        localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setUnassignedTeams([]);
      localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify([]));
      setAvailableSlots([]);
      localStorage.setItem(`draw_slots_${sport}`, JSON.stringify([]));
      
      setLastAssignedSlot(lastSlot);
      setDrawState('SLOT_REVEALED');
      playSound('reveal');
      return;
    }
    
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
        timerRef.current = setTimeout(() => roll(currentStep + 1, nextDelay), delay);
      } else {
        const finalIdx = Math.floor(Math.random() * unassignedTeams.length);
        const finalTeam = unassignedTeams[finalIdx];
        setDisplayTeam(finalTeam);
        setSelectedTeam(finalTeam);
        setDrawState('TEAM_REVEALED');
        timerRef.current = null;
      }
    };
    
    roll(0, 35);
  };

  const handleDrawSlot = () => {
    if (availableSlots.length === 0) return;
    initAudio();
    
    // Automatically assign the last team to the last slot
    if (availableSlots.length === 1 && selectedTeam) {
      const finalSlot = availableSlots[0];
      
      setDisplaySlot(finalSlot);
      setSelectedSlot(finalSlot);
      
      setAssigned(prev => {
        const next = { ...prev, [finalSlot]: selectedTeam };
        localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setUnassignedTeams(prev => {
        const next = prev.filter(t => t.id !== selectedTeam.id);
        localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setAvailableSlots(prev => {
        const next = prev.filter(s => s !== finalSlot);
        localStorage.setItem(`draw_slots_${sport}`, JSON.stringify(next));
        return next;
      });
      setLastAssignedSlot(finalSlot);
      
      setDrawState('SLOT_REVEALED');
      playSound('reveal');
      return;
    }
    
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
        timerRef.current = setTimeout(() => roll(currentStep + 1, nextDelay), delay);
      } else {
        const finalIdx = Math.floor(Math.random() * availableSlots.length);
        const finalSlot = availableSlots[finalIdx]; 
        
        setDisplaySlot(finalSlot);
        setSelectedSlot(finalSlot);
        
        setAssigned(prev => {
          const next = { ...prev, [finalSlot]: selectedTeam };
          localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
          return next;
        });
        setUnassignedTeams(prev => {
          const next = prev.filter(t => t.id !== selectedTeam.id);
          localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify(next));
          return next;
        });
        setAvailableSlots(prev => {
          const next = prev.filter(s => s !== finalSlot);
          localStorage.setItem(`draw_slots_${sport}`, JSON.stringify(next));
          return next;
        });
        setLastAssignedSlot(finalSlot);
        
        setDrawState('SLOT_REVEALED');
        playSound('reveal');
        timerRef.current = null;
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
        localStorage.removeItem(`draw_assigned_${sport}`);
        localStorage.removeItem(`draw_unassigned_${sport}`);
        localStorage.removeItem(`draw_slots_${sport}`);
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
    if (unassignedTeams.length === 1 && availableSlots.length === 1) {
      // Automatically assign the last team to the last slot
      const lastTeam = unassignedTeams[0];
      const lastSlot = availableSlots[0];
      
      setDisplayTeam(lastTeam);
      setSelectedTeam(lastTeam);
      setDisplaySlot(lastSlot);
      setSelectedSlot(lastSlot);
      
      setAssigned(prev => {
        const next = { ...prev, [lastSlot]: lastTeam };
        localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setUnassignedTeams([]);
      localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify([]));
      setAvailableSlots([]);
      localStorage.setItem(`draw_slots_${sport}`, JSON.stringify([]));
      
      setLastAssignedSlot(lastSlot);
      setDrawState('SLOT_REVEALED');
      playSound('reveal');
    } else {
      setSelectedTeam(null);
      setSelectedSlot(null);
      setDrawState('IDLE');
    }
  };

  const handleShortcutN = () => {
    // 1. Clear active animation timers
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    
    // 2. Decide action based on current state
    if (drawState === 'RANDOMIZING_TEAM') {
      if (unassignedTeams.length === 0) return;
      
      if (unassignedTeams.length === 1 && availableSlots.length === 1) {
        const lastTeam = unassignedTeams[0];
        const lastSlot = availableSlots[0];
        setDisplayTeam(lastTeam);
        setSelectedTeam(lastTeam);
        setDisplaySlot(lastSlot);
        setSelectedSlot(lastSlot);
        setAssigned(prev => {
          const next = { ...prev, [lastSlot]: lastTeam };
          localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
          return next;
        });
        setUnassignedTeams([]);
        localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify([]));
        setAvailableSlots([]);
        localStorage.setItem(`draw_slots_${sport}`, JSON.stringify([]));
        setLastAssignedSlot(lastSlot);
        setDrawState('SLOT_REVEALED');
        playSound('reveal');
        return;
      }
      
      const finalIdx = Math.floor(Math.random() * unassignedTeams.length);
      const finalTeam = unassignedTeams[finalIdx];
      setDisplayTeam(finalTeam);
      setSelectedTeam(finalTeam);
      setDrawState('TEAM_REVEALED');
    } 
    else if (drawState === 'RANDOMIZING_SLOT') {
      if (availableSlots.length === 0 || !selectedTeam) return;
      const finalSlot = availableSlots[0];
      
      setDisplaySlot(finalSlot);
      setSelectedSlot(finalSlot);
      
      setAssigned(prev => {
        const next = { ...prev, [finalSlot]: selectedTeam };
        localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setUnassignedTeams(prev => {
        const next = prev.filter(t => t.id !== selectedTeam.id);
        localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setAvailableSlots(prev => {
        const next = prev.filter(s => s !== finalSlot);
        localStorage.setItem(`draw_slots_${sport}`, JSON.stringify(next));
        return next;
      });
      setLastAssignedSlot(finalSlot);
      setDrawState('SLOT_REVEALED');
      playSound('reveal');
    }
    else if (drawState === 'IDLE') {
      if (unassignedTeams.length === 0 || availableSlots.length === 0) return;
      
      // Auto-assign the last team to the last slot instantly
      if (unassignedTeams.length === 1 && availableSlots.length === 1) {
        const lastTeam = unassignedTeams[0];
        const lastSlot = availableSlots[0];
        
        setDisplayTeam(lastTeam);
        setSelectedTeam(lastTeam);
        setDisplaySlot(lastSlot);
        setSelectedSlot(lastSlot);
        
        setAssigned(prev => {
          const next = { ...prev, [lastSlot]: lastTeam };
          localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
          return next;
        });
        setUnassignedTeams([]);
        localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify([]));
        setAvailableSlots([]);
        localStorage.setItem(`draw_slots_${sport}`, JSON.stringify([]));
        
        setLastAssignedSlot(lastSlot);
        setDrawState('SLOT_REVEALED');
        playSound('reveal');
        return;
      }
      
      const teamIdx = Math.floor(Math.random() * unassignedTeams.length);
      const team = unassignedTeams[teamIdx];
      
      const slotIdx = Math.floor(Math.random() * availableSlots.length);
      const slot = availableSlots[slotIdx];
      
      setDisplayTeam(team);
      setSelectedTeam(team);
      setDisplaySlot(slot);
      setSelectedSlot(slot);
      
      setAssigned(prev => {
        const next = { ...prev, [slot]: team };
        localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setUnassignedTeams(prev => {
        const next = prev.filter(t => t.id !== team.id);
        localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setAvailableSlots(prev => {
        const next = prev.filter(s => s !== slot);
        localStorage.setItem(`draw_slots_${sport}`, JSON.stringify(next));
        return next;
      });
      setLastAssignedSlot(slot);
      setDrawState('SLOT_REVEALED');
      playSound('reveal');
    }
    else if (drawState === 'TEAM_REVEALED') {
      if (availableSlots.length === 0 || !selectedTeam) return;
      
      const slotIdx = Math.floor(Math.random() * availableSlots.length);
      const slot = availableSlots[slotIdx];
      
      setDisplaySlot(slot);
      setSelectedSlot(slot);
      
      setAssigned(prev => {
        const next = { ...prev, [slot]: selectedTeam };
        localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setUnassignedTeams(prev => {
        const next = prev.filter(t => t.id !== selectedTeam.id);
        localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify(next));
        return next;
      });
      setAvailableSlots(prev => {
        const next = prev.filter(s => s !== slot);
        localStorage.setItem(`draw_slots_${sport}`, JSON.stringify(next));
        return next;
      });
      setLastAssignedSlot(slot);
      setDrawState('SLOT_REVEALED');
      playSound('reveal');
    }
    else if (drawState === 'SLOT_REVEALED') {
      const currentUnassigned = unassignedTeams;
      if (currentUnassigned.length === 0) {
        setSelectedTeam(null);
        setSelectedSlot(null);
        setDrawState('IDLE');
      } else if (currentUnassigned.length === 1 && availableSlots.length === 1) {
        // Automatically assign the last team to the last slot
        const lastTeam = currentUnassigned[0];
        const lastSlot = availableSlots[0];
        
        setDisplayTeam(lastTeam);
        setSelectedTeam(lastTeam);
        setDisplaySlot(lastSlot);
        setSelectedSlot(lastSlot);
        
        setAssigned(prev => {
          const next = { ...prev, [lastSlot]: lastTeam };
          localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
          return next;
        });
        setUnassignedTeams([]);
        localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify([]));
        setAvailableSlots([]);
        localStorage.setItem(`draw_slots_${sport}`, JSON.stringify([]));
        
        setLastAssignedSlot(lastSlot);
        setDrawState('SLOT_REVEALED');
        playSound('reveal');
      } else {
        const teamIdx = Math.floor(Math.random() * currentUnassigned.length);
        const team = currentUnassigned[teamIdx];
        
        const slotIdx = Math.floor(Math.random() * availableSlots.length);
        const slot = availableSlots[slotIdx];
        
        setDisplayTeam(team);
        setSelectedTeam(team);
        setDisplaySlot(slot);
        setSelectedSlot(slot);
        
        setAssigned(prev => {
          const next = { ...prev, [slot]: team };
          localStorage.setItem(`draw_assigned_${sport}`, JSON.stringify(next));
          return next;
        });
        setUnassignedTeams(prev => {
          const next = prev.filter(t => t.id !== team.id);
          localStorage.setItem(`draw_unassigned_${sport}`, JSON.stringify(next));
          return next;
        });
        setAvailableSlots(prev => {
          const next = prev.filter(s => s !== slot);
          localStorage.setItem(`draw_slots_${sport}`, JSON.stringify(next));
          return next;
        });
        setLastAssignedSlot(slot);
        setDrawState('SLOT_REVEALED');
        playSound('reveal');
      }
    }
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'n' || e.key === 'N') {
        if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') {
          return;
        }
        handleShortcutN();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [drawState, unassignedTeams, availableSlots, selectedTeam]);

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

      {drawState === 'SLOT_REVEALED' && <Confetti width={windowDimension.width} height={windowDimension.height} recycle={false} numberOfPieces={500} />}
      
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
              {drawState === 'RANDOMIZING_TEAM' && 'Đang chọn đội...'}
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
                <div className="finished-actions">
                  <button className="huge-btn download-btn" onClick={exportResults}>
                    <Download size={22} className="download-icon" /> TẢI FILE EXCEL
                  </button>
                  <button className="huge-btn home-btn" onClick={() => navigate('/')}>
                    KẾT THÚC BỐC THĂM
                  </button>
                </div>
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
        {unassignedTeams.length > 0 ? (
          <>
            <span className="bottom-label">
              {sport.includes('badminton') ? 'CÁC CẶP CHƯA BỐC:' : 'CÁC ĐỘI CHƯA BỐC:'}
            </span>
            <div className="pill-container">
              {unassignedTeams.map(t => (
                <span key={t.id} className="team-pill">{t.name}</span>
              ))}
            </div>
          </>
        ) : (
          <div className="pill-container" style={{ justifyContent: 'center' }}>
            <span className="team-pill success" style={{ margin: '0 auto' }}>Đã hoàn thành bốc thăm!</span>
          </div>
        )}
      </footer>
    </div>
  );
};

export default DrawDashboard;
