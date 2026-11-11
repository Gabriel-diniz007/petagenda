const db = require('../database');

class Pet {
  constructor({ id = null, nome, especie, raca = '', porte = 'M', nascimento = '', cliente_id }) {
    this.id = id;
    this.nome = nome;
    this.especie = especie;
    this.raca = raca;
    this.porte = porte;
    this.nascimento = nascimento;
    this.clienteId = cliente_id;
  }

  // idade aproximada em anos, a partir da data de nascimento
  idade() {
    if (!this.nascimento) return null;
    const nasc = new Date(this.nascimento + 'T00:00:00');
    const hoje = new Date();
    let anos = hoje.getFullYear() - nasc.getFullYear();
    const m = hoje.getMonth() - nasc.getMonth();
    if (m < 0 || (m === 0 && hoje.getDate() < nasc.getDate())) anos--;
    return anos;
  }

  static listar(clienteId = null) {
    let sql = `SELECT p.*, c.nome AS dono FROM pet p JOIN cliente c ON c.id = p.cliente_id`;
    const params = [];
    if (clienteId) {
      sql += ' WHERE p.cliente_id = ?';
      params.push(clienteId);
    }
    sql += ' ORDER BY p.nome';
    return db.prepare(sql).all(...params).map((l) => Object.assign(new Pet(l), { dono: l.dono }));
  }

  static buscarPorId(id) {
    const l = db.prepare('SELECT * FROM pet WHERE id = ?').get(id);
    return l ? new Pet(l) : null;
  }

  salvar() {
    const nasc = this.nascimento || null;
    if (this.id) {
      db.prepare('UPDATE pet SET nome=?, especie=?, raca=?, porte=?, nascimento=?, cliente_id=? WHERE id=?')
        .run(this.nome, this.especie, this.raca, this.porte, nasc, this.clienteId, this.id);
    } else {
      const r = db.prepare('INSERT INTO pet (nome, especie, raca, porte, nascimento, cliente_id) VALUES (?, ?, ?, ?, ?, ?)')
        .run(this.nome, this.especie, this.raca, this.porte, nasc, this.clienteId);
      this.id = Number(r.lastInsertRowid);
    }
    return this;
  }

  static excluir(id) {
    const ag = db.prepare(
      "SELECT COUNT(*) AS total FROM agendamento WHERE pet_id = ? AND status = 'AGENDADO'"
    ).get(id).total;
    if (ag > 0) {
      return 'Esse pet tem agendamentos em aberto. Cancele ou conclua antes de excluir.';
    }
    // apaga o historico junto
    db.prepare('DELETE FROM agendamento WHERE pet_id = ?').run(id);
    db.prepare('DELETE FROM pet WHERE id = ?').run(id);
    return null;
  }
}

module.exports = Pet;
