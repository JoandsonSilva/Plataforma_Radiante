import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home-page">
      <header className="hero">
        <h1>Bem-vindo à Plataforma Radiante</h1>
        <p>Explore nossos produtos e aproveite ofertas incríveis!</p>
        <Link to="/products" className="btn-primary">Ver Produtos</Link>
      </header>

      <section className="destaques">
        <h2>Destaques da Semana</h2>
        <div className="destaques-list">
          {/* Aqui você pode mapear uma lista de produtos ou destaques */}
          <div className="destaque-item">Produto 1</div>
          <div className="destaque-item">Produto 2</div>
          <div className="destaque-item">Produto 3</div>
        </div>
      </section>

      <section className="novidades">
        <h2>Novidades</h2>
        <p>Confira os lançamentos mais recentes da nossa loja.</p>
      </section>

      <footer>
        <p>© 2025 Plataforma Radiante. Todos os direitos reservados.</p>
      </footer>
    </div>
  );
}

export default Home;
