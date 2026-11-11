const db = require('../database');

class Servico {
  constructor({ id = null, nome, descricao = '', preco = 0, duracao_min = 30 }) {
    this.id = id;
    this.nome = nome;
    this.descricao = descricao;
    this.preco = Number(preco);
    this.duracaoMin = Number(duracao_min);
  }

  static listar() {
    return db.prepare('SELECT * FROM servico ORDER BY nome').all().map((l) => new Servico(l));
  }

  static buscarPorId(id) {
    const l = db.prepare('SELECT * FROM servico WHERE id = ?').get(id);
    return l ? new Servico(l) : null;
  }

  salvar() {
    if (this.id) {
      db.prepare('UPDATE servico SET nome=?, descricao=?, preco=?, duracao_min=? WHERE id=?')
        .run(this.nome, this.descricao, this.preco, this.duracaoMin, this.id);
    } else {
      const r = db.prepare('INSERT INTO servico (nome, descricao, preco, duracao_min) VALUES (?, ?, ?, ?)')
        .run(this.nome, this.descricao, this.preco, this.duracaoMin);
      this.id = Number(r.lastInsertRowid);
    }
    return this;
  }

  static excluir(id) {
    const usado = db.prepare('SELECT COUNT(*) AS total FROM agendamento WHERE servico_id = ?').get(id).total;
    if (usado > 0) {
      return 'Esse serviço já foi usado em agendamentos e não pode ser excluído.';
    }
    db.prepare('DELETE FROM servico WHERE id = ?').run(id);
    return null;
  }
}

module.exports = Servico;
