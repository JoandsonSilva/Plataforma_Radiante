import React from 'react';
import { Link } from 'react-router-dom';

function Layout({ children }) {
  return (
    <>
      <header>
        <nav>
          <Link to="/">Home</Link> | 
          <Link to="/products">Produtos</Link> | 
          <Link to="/dashboard">Dashboard</Link> | 
          <Link to="/login">Login</Link> | 
          <Link to="/register">Registrar</Link>
        </nav>
      </header>

      <main>{children}</main>

      <footer>
        <p>© 2025 Plataforma Radiante</p>
      </footer>
    </>
  );
}

export default Layout;


