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

// Serviço para gerenciar produtos
export const ProductService = {
    // Criar um novo produto
    async createProduct(productData) {
        try {
            // Validar dados
            if (!productData.name || !productData.description || !productData.price || !productData.category || !productData.size || !productData.type) {
                throw new Error('Todos os campos são obrigatórios');
            }

            // Adicionar metadados
            const data = {
                ...productData,
                createdAt: serverTimestamp(),
                updatedAt: serverTimestamp()
            };

            // Salvar no Firestore
            const docRef = await addDoc(collection(db, 'products'), data);
            console.log('Produto criado com sucesso! ID:', docRef.id);
            return docRef.id;
        } catch (error) {
            console.error('Erro ao criar produto:', error);
            throw error;
        }
    },

    // Atualizar um produto existente
    async updateProduct(productId, productData) {
        try {
            // Validar dados
            if (!productId) {
                throw new Error('ID do produto é obrigatório');
            }

            // Adicionar metadados
            const data = {
                ...productData,
                updatedAt: serverTimestamp()
            };

            // Atualizar no Firestore
            const docRef = doc(db, 'products', productId);
            await updateDoc(docRef, data);
            console.log('Produto atualizado com sucesso!');
        } catch (error) {
            console.error('Erro ao atualizar produto:', error);
            throw error;
        }
    },

    // Buscar um produto pelo ID
    async getProductById(productId) {
        try {
            const docRef = doc(db, 'products', productId);
            const docSnap = await getDoc(docRef);

            if (docSnap.exists()) {
                return {
                    id: docSnap.id,
                    ...docSnap.data()
                };
            } else {
                throw new Error('Produto não encontrado');
            }
        } catch (error) {
            console.error('Erro ao buscar produto:', error);
            throw error;
        }
    },

    // Listar todos os produtos
    async listProducts() {
        try {
            const querySnapshot = await getDocs(collection(db, 'products'));
            return querySnapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
        } catch (error) {
            console.error('Erro ao listar produtos:', error);
            throw error;
        }
    },

    // Buscar produtos por categoria
    async getProductsByCategory(category) {
        try {
            const q = query(
                collection(db, 'products'),
                where('category', '==', category)
            );
            
            const querySnapshot = await getDocs(q);
            return querySnapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
        } catch (error) {
            console.error('Erro ao buscar produtos por categoria:', error);
            throw error;
        }
    },

    // Buscar produtos por tipo
    async getProductsByType(type) {
        try {
            const q = query(
                collection(db, 'products'),
                where('type', '==', type)
            );
            
            const querySnapshot = await getDocs(q);
            return querySnapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
        } catch (error) {
            console.error('Erro ao buscar produtos por tipo:', error);
            throw error;
        }
    },

    // Buscar produtos por nome
    async searchProductsByName(name) {
        try {
            const q = query(
                collection(db, 'products'),
                where('name', '>=', name),
                where('name', '<=', name + '\uf8ff')
            );
            
            const querySnapshot = await getDocs(q);
            return querySnapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
        } catch (error) {
            console.error('Erro ao buscar produtos:', error);
            throw error;
        }
    },

    // Excluir um produto
    async deleteProduct(productId) {
        try {
            await deleteDoc(doc(db, 'products', productId));
            console.log('Produto excluído com sucesso!');
        } catch (error) {
            console.error('Erro ao excluir produto:', error);
            throw error;
        }
    }
}; 