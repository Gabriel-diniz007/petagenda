const express = require('express');
const path = require('path');

const Agendamento = require('./models/Agendamento');
const Cliente = require('./models/Cliente');
const Pet = require('./models/Pet');

const app = express();
const PORTA = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '..', 'views'));
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '..', 'public')));

// mensagens de sucesso/erro passadas pela url depois de um redirect (?ok=... ou ?erro=...)
app.use((req, res, next) => {
  res.locals.msgOk = req.query.ok || null;
  res.locals.msgErro = req.query.erro || null;
  res.locals.paginaAtual = req.path.split('/')[1] || 'inicio';
  res.locals.moeda = (v) => Number(v || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  res.locals.dataBR = (d) => (d ? d.split('-').reverse().join('/') : '');
  next();
});

function hojeISO() {
  const d = new Date();
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset()); // ajusta pro fuso local
  return d.toISOString().slice(0, 10);
}

// painel inicial
app.get('/', (req, res) => {
  const hoje = hojeISO();
  const agendaHoje = Agendamento.listar({ data: hoje }).sort((a, b) => a.hora.localeCompare(b.hora));
  res.render('index', {
    hoje,
    agendaHoje,
    totalClientes: Cliente.listar().length,
    totalPets: Pet.listar().length,
    pendentes: Agendamento.listar({ status: 'AGENDADO' }).length,
    faturamento: Agendamento.faturamentoDoMes(hoje.slice(0, 7)),
  });
});

app.use('/clientes', require('./routes/clientes'));
app.use('/pets', require('./routes/pets'));
app.use('/servicos', require('./routes/servicos'));
app.use('/agendamentos', require('./routes/agendamentos'));

app.use((req, res) => {
  res.status(404).render('404');
});

// so sobe o servidor se rodar direto (nos testes o app e importado)
if (require.main === module) {
  app.listen(PORTA, () => {
    console.log(`PetAgenda rodando em http://localhost:${PORTA}`);
  });
}

module.exports = app;
