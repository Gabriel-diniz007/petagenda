const express = require('express');
const Pet = require('../models/Pet');
const Cliente = require('../models/Cliente');

const router = express.Router();

router.get('/', (req, res) => {
  res.render('pets/lista', { pets: Pet.listar() });
});

router.get('/novo', (req, res) => {
  const clientes = Cliente.listar();
  if (clientes.length === 0) {
    return res.redirect('/clientes/novo?erro=' + encodeURIComponent('Cadastre o tutor (cliente) antes do pet'));
  }
  // permite ja vir com o dono selecionado (?cliente=ID)
  const pet = req.query.cliente ? new Pet({ cliente_id: Number(req.query.cliente) }) : null;
  res.render('pets/form', { pet, novo: true, clientes, erros: [] });
});

router.get('/:id/editar', (req, res) => {
  const pet = Pet.buscarPorId(req.params.id);
  if (!pet) return res.redirect('/pets?erro=Pet não encontrado');
  res.render('pets/form', { pet, novo: false, clientes: Cliente.listar(), erros: [] });
});

function salvar(req, res) {
  const pet = new Pet({
    id: req.params.id ? Number(req.params.id) : null,
    nome: (req.body.nome || '').trim(),
    especie: req.body.especie,
    raca: (req.body.raca || '').trim(),
    porte: req.body.porte,
    nascimento: req.body.nascimento,
    cliente_id: Number(req.body.cliente_id),
  });

  const erros = [];
  if (!pet.nome) erros.push('Informe o nome do pet.');
  if (!pet.especie) erros.push('Informe a espécie.');
  if (!['P', 'M', 'G'].includes(pet.porte)) erros.push('Porte inválido.');
  if (!Cliente.buscarPorId(pet.clienteId)) erros.push('Selecione o tutor.');
  if (pet.nascimento && pet.nascimento > new Date().toISOString().slice(0, 10)) {
    erros.push('A data de nascimento não pode ser no futuro.');
  }

  if (erros.length) {
    return res.render('pets/form', { pet, novo: !pet.id, clientes: Cliente.listar(), erros });
  }
  pet.salvar();
  res.redirect('/pets?ok=Pet salvo com sucesso');
}

router.post('/novo', salvar);
router.post('/:id/editar', salvar);

router.post('/:id/excluir', (req, res) => {
  const erro = Pet.excluir(req.params.id);
  if (erro) return res.redirect('/pets?erro=' + encodeURIComponent(erro));
  res.redirect('/pets?ok=Pet excluído');
});

module.exports = router;
