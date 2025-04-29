import React from 'react';
import { Link } from 'react-router-dom';

const ProductsPage = ({ products }) => {
  return (
    <div className="container">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Gestão de Produtos</h1>
        <Link to="/dashboard" className="btn btn-outline-primary">
          <i className="fas fa-arrow-left"></i> Voltar ao Dashboard
        </Link>
      </div>

      <div className="card">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Descrição</th>
                  <th>Preço</th>
                  <th>Estoque</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id}>
                    <td>{product.name}</td>
                    <td>{product.description}</td>
                    <td>R$ {product.price.toFixed(2)}</td>
                    <td>{product.stock}</td>
                    <td>
                      <button className="btn btn-sm btn-primary">
                        <i className="fas fa-edit"></i>
                      </button>
                      <button className="btn btn-sm btn-danger">
                        <i className="fas fa-trash"></i>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductsPage;

