import { db } from '../firebase-config.js';
import { 
    collection, 
    addDoc, 
    updateDoc, 
    deleteDoc, 
    doc, 
    getDoc, 
    getDocs, 
    query, 
    where,
    serverTimestamp 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

// Serviço para gerenciar revendedores
export const ResellerService = {
    // Criar um novo revendedor
    async createReseller(resellerData) {
        try {
            // Validar dados
            if (!resellerData.name || !resellerData.email || !resellerData.document || !resellerData.commission_rate) {
                throw new Error('Nome, email, CPF/CNPJ e taxa de comissão são obrigatórios');
            }

            // Adicionar metadados
            const data = {
                ...resellerData,
                createdAt: serverTimestamp(),
                updatedAt: serverTimestamp()
            };

            // Salvar no Firestore
            const docRef = await addDoc(collection(db, 'resellers'), data);
            console.log('Revendedor criado com sucesso! ID:', docRef.id);
            return docRef.id;
        } catch (error) {
            console.error('Erro ao criar revendedor:', error);
            throw error;
        }
    },

    // Atualizar um revendedor existente
    async updateReseller(resellerId, resellerData) {
        try {
            // Validar dados
            if (!resellerId) {
                throw new Error('ID do revendedor é obrigatório');
            }

            // Adicionar metadados
            const data = {
                ...resellerData,
                updatedAt: serverTimestamp()
            };

            // Atualizar no Firestore
            const docRef = doc(db, 'resellers', resellerId);
            await updateDoc(docRef, data);
            console.log('Revendedor atualizado com sucesso!');
        } catch (error) {
            console.error('Erro ao atualizar revendedor:', error);
            throw error;
        }
    },

    // Buscar um revendedor pelo ID
    async getResellerById(resellerId) {
        try {
            const docRef = doc(db, 'resellers', resellerId);
            const docSnap = await getDoc(docRef);

            if (docSnap.exists()) {
                return {
                    id: docSnap.id,
                    ...docSnap.data()
                };
            } else {
                throw new Error('Revendedor não encontrado');
            }
        } catch (error) {
            console.error('Erro ao buscar revendedor:', error);
            throw error;
        }
    },

    // Listar todos os revendedores
    async listResellers() {
        try {
            const querySnapshot = await getDocs(collection(db, 'resellers'));
            return querySnapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
        } catch (error) {
            console.error('Erro ao listar revendedores:', error);
            throw error;
        }
    },

    // Buscar revendedores por nome
    async searchResellersByName(name) {
        try {
            const q = query(
                collection(db, 'resellers'),
                where('name', '>=', name),
                where('name', '<=', name + '\uf8ff')
            );
            
            const querySnapshot = await getDocs(q);
            return querySnapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
        } catch (error) {
            console.error('Erro ao buscar revendedores:', error);
            throw error;
        }
    },

    // Excluir um revendedor
    async deleteReseller(resellerId) {
        try {
            await deleteDoc(doc(db, 'resellers', resellerId));
            console.log('Revendedor excluído com sucesso!');
        } catch (error) {
            console.error('Erro ao excluir revendedor:', error);
            throw error;
        }
    }
}; 