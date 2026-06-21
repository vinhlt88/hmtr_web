import { BrowserRouter, Routes, Route, useParams } from 'react-router-dom';
import Home from './pages/Home';
import DrawDashboard from './pages/DrawDashboard';

const DrawDashboardWrapper = () => {
  const { sport } = useParams();
  return <DrawDashboard key={sport} />;
};

function App() {
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
