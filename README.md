# 🐾 PetAgenda

Sistema web de agendamento para pet shop, feito para a disciplina **Desenvolvimento de Projetos II** (UniFil).

## Dupla

| Nome | GitHub |
|------|--------|
| Gabriel Diniz | [@Gabriel-diniz007](https://github.com/Gabriel-diniz007) |
| Gabriel Satin | [@Gabriel-satin](https://github.com/Gabriel-satin) |

## O que o sistema faz

- CRUD de **clientes** (tutores), com busca por nome ou telefone
- CRUD de **pets**, cada um ligado ao seu tutor
- CRUD de **serviços** (banho, tosa, consulta...) com preço e duração
- CRUD de **agendamentos**, com filtro por data e status
- Painel com a **agenda do dia**, indicadores e faturamento do mês

Regras que o sistema confere:

- não deixa marcar dois atendimentos no mesmo dia e horário
- não deixa agendar no passado nem fora do horário (08h às 18h)
- não deixa excluir cliente que tem pet, pet com agendamento em aberto ou serviço que já foi usado

## Tecnologias

- Node.js (22.13+) + Express
- EJS para as telas
- SQLite usando o módulo nativo `node:sqlite` (não precisa instalar banco)
- `node:test` para os testes

## Como rodar

```bash
npm install
npm start
```

Abra http://localhost:3000. O banco (`database/petagenda.db`) é criado sozinho na primeira execução, já com alguns serviços cadastrados.

Para rodar os testes:

```bash
npm test
```

## Estrutura

```
petagenda/
├── src/
│   ├── app.js            # servidor e painel inicial
│   ├── database.js       # conexão com o SQLite
│   ├── models/           # Cliente, Pet, Servico, Agendamento
│   └── routes/           # rotas de cada CRUD
├── views/                # telas (EJS)
├── public/css/
├── database/schema.sql   # criação das tabelas
├── test/                 # testes automatizados
└── docs/                 # documentação, diagramas e prints
```

## Documentação

- [Parte I - Documentação e modelagem (PDF)](docs/PetAgenda_Parte1_Documentacao.pdf)
- [Parte II - Implementação (PDF)](docs/PetAgenda_Parte2_Implementacao.pdf)
- Diagramas separados em [`docs/diagramas`](docs/diagramas) (caso de uso, DER, atividade, classes e sequência)
- Prints das telas em [`docs/telas`](docs/telas)
