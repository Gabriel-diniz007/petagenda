-- PetAgenda - script de criacao do banco (SQLite)

CREATE TABLE IF NOT EXISTS cliente (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL,
    cpf        TEXT UNIQUE,
    telefone   TEXT NOT NULL,
    email      TEXT,
    endereco   TEXT
);

CREATE TABLE IF NOT EXISTS pet (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL,
    especie     TEXT NOT NULL,          -- cachorro, gato, outro
    raca        TEXT,
    porte       TEXT CHECK (porte IN ('P', 'M', 'G')),
    nascimento  TEXT,
    cliente_id  INTEGER NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

CREATE TABLE IF NOT EXISTS servico (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT NOT NULL UNIQUE,
    descricao     TEXT,
    preco         REAL NOT NULL CHECK (preco >= 0),
    duracao_min   INTEGER NOT NULL DEFAULT 30
);

-- status: AGENDADO, CONCLUIDO, CANCELADO
CREATE TABLE IF NOT EXISTS agendamento (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id       INTEGER NOT NULL,
    servico_id   INTEGER NOT NULL,
    data         TEXT NOT NULL,          -- AAAA-MM-DD
    hora         TEXT NOT NULL,          -- HH:MM
    valor        REAL NOT NULL,
    status       TEXT NOT NULL DEFAULT 'AGENDADO'
                 CHECK (status IN ('AGENDADO', 'CONCLUIDO', 'CANCELADO')),
    observacao   TEXT,
    FOREIGN KEY (pet_id) REFERENCES pet(id),
    FOREIGN KEY (servico_id) REFERENCES servico(id)
);
