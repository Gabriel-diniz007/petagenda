const db = require('../database');

const STATUS = ['AGENDADO', 'CONCLUIDO', 'CANCELADO'];

class Agendamento {
  constructor({ id = null, pet_id, servico_id, data, hora, valor = 0, status = 'AGENDADO', observacao = '' }) {
    this.id = id;
    this.petId = Number(pet_id);
    this.servicoId = Number(servico_id);
    this.data = data;
    this.hora = hora;
    this.valor = Number(valor);
    this.status = status;
    this.observacao = observacao;
  }

  // filtros: { data, status }
  static listar(filtros = {}) {
    let sql = `
      SELECT a.*, p.nome AS pet_nome, p.especie, c.nome AS cliente_nome, c.telefone,
             s.nome AS servico_nome
      FROM agendamento a
      JOIN pet p ON p.id = a.pet_id
      JOIN cliente c ON c.id = p.cliente_id
      JOIN servico s ON s.id = a.servico_id
      WHERE 1 = 1`;
    const params = [];
    if (filtros.data) {
      sql += ' AND a.data = ?';
      params.push(filtros.data);
    }
    if (filtros.status) {
      sql += ' AND a.status = ?';
      params.push(filtros.status);
    }
    sql += ' ORDER BY a.data DESC, a.hora';
    return db.prepare(sql).all(...params).map((l) =>
      Object.assign(new Agendamento(l), {
        petNome: l.pet_nome,
        especie: l.especie,
        clienteNome: l.cliente_nome,
        telefone: l.telefone,
        servicoNome: l.servico_nome,
      })
    );
  }

  static buscarPorId(id) {
    const l = db.prepare('SELECT * FROM agendamento WHERE id = ?').get(id);
    return l ? new Agendamento(l) : null;
  }

  // verifica as regras antes de salvar. Retorna uma lista de erros (vazia = ok)
  validar() {
    const erros = [];
    if (!this.petId) erros.push('Selecione o pet.');
    if (!this.servicoId) erros.push('Selecione o serviço.');
    if (!this.data || !this.hora) erros.push('Informe a data e a hora.');
    if (!STATUS.includes(this.status)) erros.push('Status inválido.');
    if (erros.length) return erros;

    // nao deixa marcar no passado (so vale para agendamentos em aberto)
    const quando = new Date(`${this.data}T${this.hora}:00`);
    if (this.status === 'AGENDADO' && quando < new Date()) {
      erros.push('Não é possível agendar para uma data/hora que já passou.');
    }

    // horario de funcionamento: 08:00 as 18:00
    if (this.hora < '08:00' || this.hora > '18:00') {
      erros.push('O pet shop atende das 08:00 às 18:00.');
    }

    // conflito de horario: outro agendamento ativo no mesmo dia e hora
    if (this.status === 'AGENDADO') {
      const conflito = db.prepare(`
        SELECT COUNT(*) AS total FROM agendamento
        WHERE data = ? AND hora = ? AND status = 'AGENDADO' AND id <> ?
      `).get(this.data, this.hora, this.id || 0).total;
      if (conflito > 0) erros.push('Já existe um agendamento nesse dia e horário.');
    }
    return erros;
  }

  salvar() {
    // o valor vem do servico no momento do agendamento
    if (!this.valor) {
      const s = db.prepare('SELECT preco FROM servico WHERE id = ?').get(this.servicoId);
      this.valor = s ? s.preco : 0;
    }
    if (this.id) {
      db.prepare(`UPDATE agendamento SET pet_id=?, servico_id=?, data=?, hora=?, valor=?, status=?, observacao=?
                  WHERE id=?`)
        .run(this.petId, this.servicoId, this.data, this.hora, this.valor, this.status, this.observacao, this.id);
    } else {
      const r = db.prepare(`INSERT INTO agendamento (pet_id, servico_id, data, hora, valor, status, observacao)
                            VALUES (?, ?, ?, ?, ?, ?, ?)`)
        .run(this.petId, this.servicoId, this.data, this.hora, this.valor, this.status, this.observacao);
      this.id = Number(r.lastInsertRowid);
    }
    return this;
  }

  static alterarStatus(id, status) {
    if (!STATUS.includes(status)) return 'Status inválido.';
    db.prepare('UPDATE agendamento SET status = ? WHERE id = ?').run(status, id);
    return null;
  }

  static excluir(id) {
    db.prepare('DELETE FROM agendamento WHERE id = ?').run(id);
  }

  // valor dos atendimentos concluidos no mes (AAAA-MM)
  static faturamentoDoMes(anoMes) {
    return db.prepare(`
      SELECT COALESCE(SUM(valor), 0) AS total FROM agendamento
      WHERE status = 'CONCLUIDO' AND substr(data, 1, 7) = ?
    `).get(anoMes).total;
  }
}

Agendamento.STATUS = STATUS;
module.exports = Agendamento;
