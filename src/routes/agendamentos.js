const express = require('express');
const Agendamento = require('../models/Agendamento');
const Pet = require('../models/Pet');
const Servico = require('../models/Servico');

const router = express.Router();

router.get('/', (req, res) => {
  const filtros = { data: req.query.data || '', status: req.query.status || '' };
  res.render('agendamentos/lista', {
    agendamentos: Agendamento.listar(filtros),
    filtros,
    statusLista: Agendamento.STATUS,
  });
});

function renderForm(res, agendamento, erros) {
  const pets = Pet.listar();
  if (pets.length === 0) {
    return res.redirect('/pets?erro=' + encodeURIComponent('Cadastre um pet antes de agendar'));
  }
  res.render('agendamentos/form', {
    agendamento,
    pets,
    servicos: Servico.listar(),
    statusLista: Agendamento.STATUS,
    erros,
  });
}

router.get('/novo', (req, res) => {
  const ag = req.query.pet ? new Agendamento({ pet_id: req.query.pet }) : null;
  renderForm(res, ag, []);
});

router.get('/:id/editar', (req, res) => {
  const ag = Agendamento.buscarPorId(req.params.id);
  if (!ag) return res.redirect('/agendamentos?erro=Agendamento não encontrado');
  renderForm(res, ag, []);
});

function salvar(req, res) {
  const id = req.params.id ? Number(req.params.id) : null;
  const antigo = id ? Agendamento.buscarPorId(id) : null;

  const ag = new Agendamento({
    id,
    pet_id: req.body.pet_id,
    servico_id: req.body.servico_id,
    data: req.body.data,
    hora: req.body.hora,
    status: req.body.status || 'AGENDADO',
    observacao: (req.body.observacao || '').trim(),
    // se trocar o servico o valor e recalculado
    valor: antigo && antigo.servicoId === Number(req.body.servico_id) ? antigo.valor : 0,
  });

  const erros = ag.validar();
  if (erros.length) return renderForm(res, ag, erros);

  ag.salvar();
  res.redirect('/agendamentos?ok=Agendamento salvo com sucesso');
}

router.post('/novo', salvar);
router.post('/:id/editar', salvar);

// botoes rapidos de concluir / cancelar
router.post('/:id/status', (req, res) => {
  const erro = Agendamento.alterarStatus(req.params.id, req.body.status);
  const volta = req.body.voltar === 'inicio' ? '/' : '/agendamentos';
  if (erro) return res.redirect(volta + '?erro=' + encodeURIComponent(erro));
  res.redirect(volta + '?ok=Status atualizado');
});

router.post('/:id/excluir', (req, res) => {
  Agendamento.excluir(req.params.id);
  res.redirect('/agendamentos?ok=Agendamento excluído');
});

module.exports = router;
