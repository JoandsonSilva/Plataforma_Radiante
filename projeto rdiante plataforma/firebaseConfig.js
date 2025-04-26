// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyB3b8HR1Gcmfp4YMh7Ibj7a-X7sGYd_6uk",
  authDomain: "plataforma-radiante.firebaseapp.com",
  projectId: "plataforma-radiante",
  storageBucket: "plataforma-radiante.firebasestorage.app",
  messagingSenderId: "990096383941",
  appId: "1:990096383941:web:46541971f9a5e86ead75ac",
  measurementId: "G-VZZZYRQZFP"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Exporta os serviços que você usará (Auth e Firestore)
export const auth = getAuth(app);
export const db = getFirestore(app);

export default app;