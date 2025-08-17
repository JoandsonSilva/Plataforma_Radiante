// Importar as funções necessárias do Firebase
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { getFirestore, enableIndexedDbPersistence } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";
import { getStorage } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-storage.js";

// Configuração do Firebase
const firebaseConfig = {
    apiKey: "AIzaSyB3b8HR1Gcmfp4YMh7Ibj7a-X7sGYd_6uk",
    authDomain: "plataforma-radiante.firebaseapp.com",
    projectId: "plataforma-radiante",
    storageBucket: "plataforma-radiante.appspot.com",
    messagingSenderId: "990096383941",
    appId: "1:990096383941:web:46541971f9a5e86ead75ac",
    measurementId: "G-VZZZYRQZFP"
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);

// Inicializar serviços
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

// Habilitar persistência offline
enableIndexedDbPersistence(db)
    .catch((err) => {
        if (err.code === 'failed-precondition') {
            console.log('Múltiplas abas abertas, persistência não pode ser habilitada');
        } else if (err.code === 'unimplemented') {
            console.log('O navegador não suporta persistência');
        }
    });

// Exportar as referências
export { auth, db, storage }; 