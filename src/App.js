import { Routes, Route } from 'react-router-dom';
import Home from './pages/HomePage';
import Login from './pages/LoginPage.jsx';
import DashboardPage from './pages/DashboardPage';
import ProductsPage from './pages/ProductsPage';
import RevendedoresPage from './pages/RevendedoresPage';
import TasksPage from './pages/TasksPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/products" element={<ProductsPage />} />
      <Route path="/revendedores" element={<RevendedoresPage />} />
      <Route path="/tasks" element={<TasksPage />} />
    </Routes>
  );
}

export default App;
