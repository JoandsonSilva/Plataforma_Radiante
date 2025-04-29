import { auth, signInWithEmailAndPassword } from './firebase-config';

const loginForm = document.getElementById('loginForm');
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        await signInWithEmailAndPassword(auth, email, password);
        window.location.href = 'dashboard.html';  // Redireciona para o Dashboard após login
    } catch (error) {
        alert("Erro de login: " + error.message);
    }
});
