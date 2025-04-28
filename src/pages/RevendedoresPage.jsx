import React from 'react';

function RevendedoresPage() {
  return (
    <div className="container mt-5">
      <h1 className="mb-4">Revendedores</h1>

      <div className="d-flex justify-content-end mb-3">
        <button className="btn btn-primary">
          <i className="fas fa-user-plus"></i> Novo Revendedor
        </button>
      </div>

      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-primary">
            <tr>
              <th>Nome</th>
              <th>Email</th>
              <th>Telefone</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {/* Aqui futuramente você vai mapear os revendedores do banco */}
            <tr>
              <td>João da Silva</td>
              <td>joao@email.com</td>
              <td>(11) 98765-4321</td>
              <td><span className="badge bg-success">Ativo</span></td>
              <td>
                <button className="btn btn-sm btn-warning me-2">
                  <i className="fas fa-edit"></i>
                </button>
                <button className="btn btn-sm btn-danger">
                  <i className="fas fa-trash-alt"></i>
                </button>
              </td>
            </tr>
            {/* Você vai colocar mais registros aqui depois */}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RevendedoresPage;
