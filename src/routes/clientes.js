const express = require('express');
const Cliente = require('../models/Cliente');
const Pet = require('../models/Pet');

const router = express.Router();

router.get('/', (req, res) => {
  const busca = (req.query.busca || '').trim();
  res.render('clientes/lista', { clientes: Cliente.listar(busca), busca });
});

router.get('/novo', (req, res) => {
  res.render('clientes/form', { cliente: null, erros: [] });
});

router.get('/:id', (req, res) => {
  const cliente = Cliente.buscarPorId(req.params.id);
  if (!cliente) return res.redirect('/clientes?erro=Cliente não encontrado');
  res.render('clientes/detalhe', { cliente, pets: Pet.listar(cliente.id) });
});

router.get('/:id/editar', (req, res) => {
  const cliente = Cliente.buscarPorId(req.params.id);
  if (!cliente) return res.redirect('/clientes?erro=Cliente não encontrado');
  res.render('clientes/form', { cliente, erros: [] });
});

function salvar(req, res) {
  const dados = {
    id: req.params.id ? Number(req.params.id) : null,
    nome: (req.body.nome || '').trim(),
    cpf: (req.body.cpf || '').trim(),
    telefone: (req.body.telefone || '').trim(),
    email: (req.body.email || '').trim(),
    endereco: (req.body.endereco || '').trim(),
  };
  const erros = [];
  if (!dados.nome) erros.push('O nome é obrigatório.');
  if (!dados.telefone) erros.push('O telefone é obrigatório.');
  if (dados.cpf && dados.cpf.replace(/\D/g, '').length !== 11) erros.push('CPF deve ter 11 números.');

  const cliente = new Cliente(dados);
  if (erros.length) return res.render('clientes/form', { cliente, erros });

  try {
    cliente.salvar();
  } catch (e) {
    if (String(e.message).includes('UNIQUE')) {
      return res.render('clientes/form', { cliente, erros: ['Já existe um cliente com esse CPF.'] });
    }
    throw e;
  }
  res.redirect('/clientes?ok=Cliente salvo com sucesso');
}

router.post('/novo', salvar);
router.post('/:id/editar', salvar);

router.post('/:id/excluir', (req, res) => {
  const erro = Cliente.excluir(req.params.id);
  if (erro) return res.redirect('/clientes?erro=' + encodeURIComponent(erro));
  res.redirect('/clientes?ok=Cliente excluído');
});

module.exports = router;
