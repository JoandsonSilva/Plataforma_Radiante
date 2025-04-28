import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../services/firebaseConfig';
import { signOut } from 'firebase/auth';

function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!auth.currentUser) {
      navigate('/login');
    } else {
      setUser(auth.currentUser);
    }
  }, [navigate]);

  const handleLogout = () => {
    signOut(auth)
      .then(() => {
        navigate('/login');
      })
      .catch((error) => {
        console.error('Erro ao sair:', error);
      });
  };

  return (
    <div className="dashboard">
      <h1>Bem-vindo, {user ? user.displayName : 'Usuário'}!</h1>
      <p>Você está logado no seu painel de controle.</p>

      <section className="user-info">
        <h2>Informações da Conta</h2>
        <p>Email: {user ? user.email : 'Carregando...'}</p>
      </section>

      <button onClick={handleLogout} className="logout-btn">
        Sair
      </button>
    </div>
  );
}

export default Dashboard;
