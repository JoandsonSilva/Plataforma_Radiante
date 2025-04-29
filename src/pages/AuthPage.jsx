import React from 'react';
import { Link } from 'react-router-dom';

function AuthPage() {
  return (
    <div className="auth-page">
    <h1>Área de Autenticação</h1>
    <p>
      Já tem uma conta? <Link to="/login">Faça Login</Link>
    </p>
    <p>
      Novo por aqui? <Link to="/register">Cadastre-se</Link>
    </p>
  </div>
);
}

export default AuthPage;
