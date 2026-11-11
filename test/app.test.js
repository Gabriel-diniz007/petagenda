// Testes basicos do CRUD - rodar com: npm test
const { test, before, after } = require('node:test');
const assert = require('node:assert');
const path = require('path');
const os = require('os');
const fs = require('fs');

// usa um banco separado so pros testes
const dbTeste = path.join(os.tmpdir(), `petagenda-teste-${Date.now()}.db`);
process.env.DB_PATH = dbTeste;
const app = require('../src/app');

let servidor;
let base;

before(async () => {
  servidor = app.listen(0);
  await new Promise((r) => servidor.once('listening', r));
  base = `http://localhost:${servidor.address().port}`;
});

after(() => {
  servidor.close();
  try { fs.unlinkSync(dbTeste); } catch (e) { /* tanto faz */ }
});

async function post(url, dados) {
  const r = await fetch(base + url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(dados),
    redirect: 'manual',
  });
  return { status: r.status, local: decodeURIComponent(r.headers.get('location') || ''), html: await r.text() };
}

async function get(url) {
  const r = await fetch(base + url);
  return { status: r.status, html: await r.text() };
}

function amanha() {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  return d.toISOString().slice(0, 10);
}

test('todas as paginas abrem', async () => {
  for (const u of ['/', '/clientes', '/clientes/novo', '/pets', '/servicos', '/servicos/novo', '/agendamentos']) {
    assert.strictEqual((await get(u)).status, 200, u);
  }
  assert.strictEqual((await get('/nao-existe')).status, 404);
});

test('CRUD de cliente', async () => {
  let r = await post('/clientes/novo', { nome: '', telefone: '' });
  assert.match(r.html, /nome é obrigatório/);

  r = await post('/clientes/novo', { nome: 'Maria Souza', telefone: '(43) 99999-1111', cpf: '123.456.789-00' });
  assert.strictEqual(r.status, 302);
  assert.match((await get('/clientes')).html, /Maria Souza/);

  r = await post('/clientes/novo', { nome: 'Outra', telefone: '1', cpf: '123.456.789-00' });
  assert.match(r.html, /mesmo CPF|esse CPF/);

  r = await post('/clientes/1/editar', { nome: 'Maria Souza Lima', telefone: '(43) 98888-2222', cpf: '123.456.789-00' });
  assert.strictEqual(r.status, 302);
  assert.match((await get('/clientes/1')).html, /Maria Souza Lima/);
  assert.match((await get('/clientes?busca=Lima')).html, /Maria Souza Lima/);
});

test('CRUD de pet e regra de exclusao do cliente', async () => {
  let r = await post('/pets/novo', { nome: 'Thor', especie: 'Cachorro', raca: 'Labrador', porte: 'G', nascimento: '2020-03-10', cliente_id: 1 });
  assert.strictEqual(r.status, 302);
  assert.match((await get('/pets')).html, /Thor/);

  r = await post('/clientes/1/excluir', {});
  assert.match(r.local, /possui pets/);

  r = await post('/pets/1/editar', { nome: 'Thor', especie: 'Cachorro', raca: '', porte: 'G', nascimento: '', cliente_id: 1 });
  assert.strictEqual(r.status, 302);
});

test('CRUD de servico', async () => {
  let r = await post('/servicos/novo', { nome: 'Hidratação', preco: '35,50', duracao_min: 30 });
  assert.strictEqual(r.status, 302);
  assert.match((await get('/servicos')).html, /Hidratação/);
  r = await post('/servicos/novo', { nome: 'Hidratação', preco: '10', duracao_min: 30 });
  assert.match(r.html, /mesmo nome|esse nome/);
});

test('agendamento com regras de horario', async () => {
  const dia = amanha();
  let r = await post('/agendamentos/novo', { pet_id: 1, servico_id: 1, data: dia, hora: '10:00' });
  assert.strictEqual(r.status, 302);

  r = await post('/agendamentos/novo', { pet_id: 1, servico_id: 2, data: dia, hora: '10:00' });
  assert.match(r.html, /Já existe um agendamento/);

  r = await post('/agendamentos/novo', { pet_id: 1, servico_id: 2, data: '2020-01-01', hora: '10:00' });
  assert.match(r.html, /já passou/);

  r = await post('/agendamentos/novo', { pet_id: 1, servico_id: 2, data: dia, hora: '22:00' });
  assert.match(r.html, /08:00 às 18:00/);

  // pet com agendamento em aberto nao pode ser excluido
  r = await post('/pets/1/excluir', {});
  assert.match(r.local, /agendamentos em aberto/);

  r = await post('/agendamentos/1/status', { status: 'CONCLUIDO' });
  assert.strictEqual(r.status, 302);
  assert.match((await get('/agendamentos?status=CONCLUIDO')).html, /Thor/);

  // servico usado nao pode ser excluido
  r = await post('/servicos/1/excluir', {});
  assert.match(r.local, /não pode ser excluído/);

  r = await post('/agendamentos/1/excluir', {});
  assert.strictEqual(r.status, 302);
  r = await post('/pets/1/excluir', {});
  assert.match(r.local, /Pet excluído/);
  r = await post('/clientes/1/excluir', {});
  assert.match(r.local, /Cliente excluído/);
});
