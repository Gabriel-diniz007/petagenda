const db = require('../database');

class Cliente {
  constructor({ id = null, nome, cpf = '', telefone, email = '', endereco = '' }) {
    this.id = id;
    this.nome = nome;
    this.cpf = cpf;
    this.telefone = telefone;
    this.email = email;
    this.endereco = endereco;
  }

  static listar(busca = '') {
    const linhas = db.prepare(`
      SELECT c.*, (SELECT COUNT(*) FROM pet p WHERE p.cliente_id = c.id) AS qtd_pets
      FROM cliente c
      WHERE c.nome LIKE ? OR c.telefone LIKE ?
      ORDER BY c.nome
    `).all(`%${busca}%`, `%${busca}%`);
    return linhas.map((l) => Object.assign(new Cliente(l), { qtdPets: l.qtd_pets }));
  }

  static buscarPorId(id) {
    const l = db.prepare('SELECT * FROM cliente WHERE id = ?').get(id);
    return l ? new Cliente(l) : null;
  }

  salvar() {
    const cpf = this.cpf ? this.cpf : null; // vazio vira NULL por causa do UNIQUE
    if (this.id) {
      db.prepare('UPDATE cliente SET nome = ?, cpf = ?, telefone = ?, email = ?, endereco = ? WHERE id = ?')
        .run(this.nome, cpf, this.telefone, this.email, this.endereco, this.id);
    } else {
      const r = db.prepare('INSERT INTO cliente (nome, cpf, telefone, email, endereco) VALUES (?, ?, ?, ?, ?)')
        .run(this.nome, cpf, this.telefone, this.email, this.endereco);
      this.id = Number(r.lastInsertRowid);
    }
    return this;
  }

  // retorna uma mensagem de erro ou null
  static excluir(id) {
    const pets = db.prepare('SELECT COUNT(*) AS total FROM pet WHERE cliente_id = ?').get(id).total;
    if (pets > 0) {
      return 'Esse cliente possui pets cadastrados. Exclua os pets primeiro.';
    }
    db.prepare('DELETE FROM cliente WHERE id = ?').run(id);
    return null;
  }
}

module.exports = Cliente;
