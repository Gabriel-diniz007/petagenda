// Conexao com o banco SQLite usando o modulo nativo do Node (node:sqlite)
const { DatabaseSync } = require('node:sqlite');
const fs = require('fs');
const path = require('path');

const caminho = process.env.DB_PATH || path.join(__dirname, '..', 'database', 'petagenda.db');
const db = new DatabaseSync(caminho);

db.exec('PRAGMA foreign_keys = ON;');

// cria as tabelas se ainda nao existirem
const schema = fs.readFileSync(path.join(__dirname, '..', 'database', 'schema.sql'), 'utf-8');
db.exec(schema);

// se a tabela de servicos estiver vazia, ja coloca alguns basicos
const qtdServicos = db.prepare('SELECT COUNT(*) AS total FROM servico').get().total;
if (qtdServicos === 0) {
  const ins = db.prepare('INSERT INTO servico (nome, descricao, preco, duracao_min) VALUES (?, ?, ?, ?)');
  ins.run('Banho', 'Banho com shampoo neutro e secagem', 45, 40);
  ins.run('Tosa', 'Tosa higiênica ou na máquina', 60, 60);
  ins.run('Banho e Tosa', 'Pacote completo', 95, 90);
  ins.run('Consulta Veterinária', 'Atendimento clínico geral', 120, 30);
}

module.exports = db;
