import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import RevendedoresPage from './pages/RevendedoresPage';
import ProductsPage from './pages/ProductsPage';
import TasksPage from './pages/TasksPage';
import './assets/css/style.css';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/revendedores" element={<RevendedoresPage />} />
        <Route path="/produtos" element={<ProductsPage />} />
        <Route path="/tarefas" element={<TasksPage />} />
      </Routes>
    </Router>
  );
}

export default App;
