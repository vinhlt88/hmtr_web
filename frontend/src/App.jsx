import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import DrawDashboard from './pages/DrawDashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/draw/:sport" element={<DrawDashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
