import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TasksPage from './pages/TasksPage';
import RevendedoresPage from './pages/RevendedoresPage';
import AuthPage from './pages/AuthPage';
import ProductsPage from './pages/ProductsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/tasks" element={<TasksPage />} />
        <Route path="/revendedores" element={<RevendedoresPage />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/products" element={<ProductsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
