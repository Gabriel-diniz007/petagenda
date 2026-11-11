const express = require('express');
const Servico = require('../models/Servico');

const router = express.Router();

router.get('/', (req, res) => {
  res.render('servicos/lista', { servicos: Servico.listar() });
});

router.get('/novo', (req, res) => {
  res.render('servicos/form', { servico: null, erros: [] });
});

router.get('/:id/editar', (req, res) => {
  const servico = Servico.buscarPorId(req.params.id);
  if (!servico) return res.redirect('/servicos?erro=Serviço não encontrado');
  res.render('servicos/form', { servico, erros: [] });
});

function salvar(req, res) {
  const servico = new Servico({
    id: req.params.id ? Number(req.params.id) : null,
    nome: (req.body.nome || '').trim(),
    descricao: (req.body.descricao || '').trim(),
    preco: String(req.body.preco || '0').replace(',', '.'),
    duracao_min: req.body.duracao_min,
  });

  const erros = [];
  if (!servico.nome) erros.push('Informe o nome do serviço.');
  if (isNaN(servico.preco) || servico.preco < 0) erros.push('Preço inválido.');
  if (!servico.duracaoMin || servico.duracaoMin <= 0) erros.push('A duração deve ser maior que zero.');
  if (erros.length) return res.render('servicos/form', { servico, erros });

  try {
    servico.salvar();
  } catch (e) {
    if (String(e.message).includes('UNIQUE')) {
      return res.render('servicos/form', { servico, erros: ['Já existe um serviço com esse nome.'] });
    }
    throw e;
  }
  res.redirect('/servicos?ok=Serviço salvo com sucesso');
}

router.post('/novo', salvar);
router.post('/:id/editar', salvar);

router.post('/:id/excluir', (req, res) => {
  const erro = Servico.excluir(req.params.id);
  if (erro) return res.redirect('/servicos?erro=' + encodeURIComponent(erro));
  res.redirect('/servicos?ok=Serviço excluído');
});

module.exports = router;
