"""
Script que gera as imagens dos diagramas da documentacao (PNG).
Os arquivos .puml da mesma pasta tem a versao em PlantUML dos mesmos diagramas.

Uso:  python docs/diagramas/desenhar.py
Precisa do matplotlib (pip install matplotlib)
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, Circle, Polygon

PASTA = os.path.dirname(os.path.abspath(__file__))
COR_CAIXA = "#fef9e7"
COR_BORDA = "#8a6d3b"
COR_CAB = "#f5e6b8"
FONTE = 9


def nova_figura(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def salvar(fig, nome):
    fig.savefig(os.path.join(PASTA, nome + ".png"), dpi=150, facecolor="white")
    plt.close(fig)
    print("gerado:", nome + ".png")


def seta(ax, x1, y1, x2, y2, tracejada=False, aberta=False, cor="black"):
    estilo = "->" if aberta else "-|>"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=estilo, color=cor, lw=1,
                                linestyle="--" if tracejada else "-",
                                shrinkA=0, shrinkB=0, mutation_scale=12))


def boneco(ax, x, y, nome, escala=1.0):
    """desenha o ator (boneco palito); (x, y) = pe do boneco"""
    s = escala
    ax.add_patch(Circle((x, y + 0.62 * s), 0.1 * s, fill=False, lw=1.2))
    ax.plot([x, x], [y + 0.52 * s, y + 0.22 * s], color="black", lw=1.2)
    ax.plot([x - 0.18 * s, x + 0.18 * s], [y + 0.42 * s, y + 0.42 * s], color="black", lw=1.2)
    ax.plot([x, x - 0.15 * s], [y + 0.22 * s, y], color="black", lw=1.2)
    ax.plot([x, x + 0.15 * s], [y + 0.22 * s, y], color="black", lw=1.2)
    ax.text(x, y - 0.12, nome, ha="center", va="top", fontsize=FONTE, weight="bold")



def tabela(ax, x, y_topo, largura, titulo, campos, cor_cab=COR_CAB):
    alt_linha = 0.26
    altura = 0.35 + alt_linha * len(campos) + 0.1
    ax.add_patch(Rectangle((x, y_topo - altura), largura, altura, facecolor=COR_CAIXA, edgecolor=COR_BORDA, lw=1.2))
    ax.add_patch(Rectangle((x, y_topo - 0.35), largura, 0.35, facecolor=cor_cab, edgecolor=COR_BORDA, lw=1.2))
    ax.text(x + largura / 2, y_topo - 0.175, titulo, ha="center", va="center", fontsize=10, weight="bold")
    yy = y_topo - 0.35 - 0.18
    for campo in campos:
        negrito = "PK" in campo
        ax.text(x + 0.1, yy, campo, va="center", fontsize=8.5, weight="bold" if negrito else "normal")
        yy -= alt_linha
    return (x, y_topo - altura, largura, altura)  # x, y_base, w, h


def pe_galinha(ax, x, y, direcao, tipo):
    """direcao = +1 se a linha sai para a direita do ponto, -1 para a esquerda.
    tipo: 'um', 'zero_um', 'muitos', 'zero_muitos'"""
    d = direcao
    if tipo in ("um", "zero_um"):
        ax.plot([x + d * 0.12, x + d * 0.12], [y - 0.1, y + 0.1], color="black", lw=1)
        if tipo == "um":
            ax.plot([x + d * 0.2, x + d * 0.2], [y - 0.1, y + 0.1], color="black", lw=1)
        else:
            ax.add_patch(Circle((x + d * 0.27, y), 0.06, facecolor="white", edgecolor="black", lw=1, zorder=3))
    else:
        ax.plot([x, x + d * 0.2], [y + 0.12, y], color="black", lw=1)
        ax.plot([x, x + d * 0.2], [y - 0.12, y], color="black", lw=1)
        ax.plot([x, x + d * 0.2], [y, y], color="black", lw=1)
        if tipo == "zero_muitos":
            ax.add_patch(Circle((x + d * 0.3, y), 0.06, facecolor="white", edgecolor="black", lw=1, zorder=3))
        else:
            ax.plot([x + d * 0.28, x + d * 0.28], [y - 0.1, y + 0.1], color="black", lw=1)


def ligacao(ax, x1, y1, x2, y2, tipo1, tipo2, texto=""):
    xm = (x1 + x2) / 2
    ax.plot([x1, xm, xm, x2], [y1, y1, y2, y2], color="black", lw=1, zorder=1)
    pe_galinha(ax, x1, y1, 1 if x2 > x1 else -1, tipo1)
    pe_galinha(ax, x2, y2, -1 if x2 > x1 else 1, tipo2)
    if texto and abs(y1 - y2) < 0.05:
        ax.text(xm, y1 + 0.12, texto, fontsize=8, style="italic", ha="center")
    elif texto:
        ax.text(xm + 0.05, (y1 + y2) / 2, texto, fontsize=8, style="italic", va="center")



def classe(ax, x, y_topo, largura, nome, atributos, metodos):
    lh = 0.24
    h_nome = 0.4
    h_attr = lh * len(atributos) + 0.12
    h_met = lh * len(metodos) + 0.12
    total = h_nome + h_attr + h_met
    base = y_topo - total
    ax.add_patch(Rectangle((x, base), largura, total, facecolor=COR_CAIXA, edgecolor=COR_BORDA, lw=1.2))
    ax.add_patch(Rectangle((x, y_topo - h_nome), largura, h_nome, facecolor=COR_CAB, edgecolor=COR_BORDA, lw=1.2))
    ax.plot([x, x + largura], [y_topo - h_nome - h_attr] * 2, color=COR_BORDA, lw=1.2)
    ax.text(x + largura / 2, y_topo - h_nome / 2, nome, ha="center", va="center", fontsize=10, weight="bold")
    yy = y_topo - h_nome - 0.18
    for a in atributos:
        ax.text(x + 0.1, yy, a, fontsize=8, va="center")
        yy -= lh
    yy = y_topo - h_nome - h_attr - 0.18
    for m in metodos:
        sublinhado = m.startswith("+ $")
        ax.text(x + 0.1, yy, m.replace("$", ""), fontsize=8, va="center", style="italic" if sublinhado else "normal")
        yy -= lh
    return (x, base, largura, total)



# ------------------------------------------------------------------
# DIAGRAMAS DE SEQUENCIA
# ------------------------------------------------------------------
def sequencia(nome, titulo, participantes, passos):
    """participantes: lista de (id, rotulo, tipo) tipo = ator | objeto | banco
    passos: ('m', de, para, texto) mensagem | ('r', de, para, texto) retorno |
            ('s', quem, texto) auto-mensagem | ('div', texto) |
            ('alt', cond) ('senao', cond) ('loop', cond) ('fim',)"""
    esp_x = 2.35
    esp_y = 0.42
    n_linhas = sum(2 if p[0] in ("s",) else (1.6 if p[0] in ("div", "alt", "loop", "senao") else 1) for p in passos)
    largura = esp_x * (len(participantes) - 1) + 2.4
    altura = n_linhas * esp_y + 2.6
    fig, ax = nova_figura(largura, altura)
    ax.text(largura / 2, altura - 0.25, titulo, ha="center", fontsize=11, weight="bold")

    pos = {}
    topo = altura - 0.75
    for i, (pid, rotulo, tipo) in enumerate(participantes):
        x = 1.2 + i * esp_x
        pos[pid] = x
        if tipo == "ator":
            boneco(ax, x, topo - 0.62, "", 0.9)
            ax.text(x, topo - 0.72, rotulo, ha="center", va="top", fontsize=FONTE, weight="bold")
        elif tipo == "banco":
            ax.add_patch(Rectangle((x - 0.45, topo - 0.75), 0.9, 0.55, facecolor=COR_CAB, edgecolor=COR_BORDA))
            ax.add_patch(Ellipse((x, topo - 0.2), 0.9, 0.22, facecolor=COR_CAB, edgecolor=COR_BORDA))
            ax.add_patch(Ellipse((x, topo - 0.75), 0.9, 0.22, facecolor=COR_CAB, edgecolor=COR_BORDA))
            ax.add_patch(Rectangle((x - 0.44, topo - 0.75), 0.88, 0.1, facecolor=COR_CAB, edgecolor="none"))
            ax.text(x, topo - 0.47, rotulo, ha="center", va="center", fontsize=FONTE, weight="bold")
        else:
            ax.add_patch(Rectangle((x - 0.95, topo - 0.75), 1.9, 0.6, facecolor=COR_CAB, edgecolor=COR_BORDA))
            ax.text(x, topo - 0.45, rotulo, ha="center", va="center", fontsize=FONTE, weight="bold")

    y = topo - 1.25

    num = 1
    pilha = []  # fragmentos abertos
    for p in passos:
        tipo = p[0]
        if tipo in ("m", "r"):
            x1, x2 = pos[p[1]], pos[p[2]]
            seta(ax, x1, y, x2, y, tracejada=(tipo == "r"), aberta=(tipo == "r"))
            ax.text((x1 + x2) / 2, y + 0.05, "%d. %s" % (num, p[3]), ha="center", va="bottom", fontsize=7.8)
            for f in pilha:
                f["xs"] += [x1, x2]
            num += 1
            y -= esp_y
        elif tipo == "s":
            x = pos[p[1]]
            ax.plot([x, x + 0.4, x + 0.4], [y, y, y - 0.3], color="black", lw=1)
            seta(ax, x + 0.4, y - 0.3, x, y - 0.3)
            ax.text(x + 0.48, y - 0.15, "%d. %s" % (num, p[2]), va="center", fontsize=7.8)
            for f in pilha:
                f["xs"] += [x, x + 1.8]
            num += 1
            y -= esp_y * 2
        elif tipo == "div":
            y -= 0.1
            ax.plot([0.1, largura - 0.1], [y, y], color="#555", lw=0.8)
            ax.plot([0.1, largura - 0.1], [y - 0.05, y - 0.05], color="#555", lw=0.8)
            ax.text(largura / 2, y - 0.025, "  " + p[1] + "  ", ha="center", va="center", fontsize=8.5,
                    weight="bold", bbox=dict(facecolor="#eeeeee", edgecolor="#555", lw=0.8))
            y -= esp_y * 1.1
        elif tipo in ("alt", "loop", "opt"):
            pilha.append({"tipo": tipo, "cond": p[1], "y0": y + 0.12, "xs": [], "senoes": []})
            y -= esp_y * 0.7
        elif tipo == "senao":
            pilha[-1]["senoes"].append((y + 0.1, p[1]))
            y -= esp_y * 0.7
        elif tipo == "fim":
            f = pilha.pop()
            nivel = len(pilha)
            x0 = min(f["xs"]) - 0.9 + nivel * 0.12
            x1 = min(max(f["xs"]) + 0.9, largura - 0.15) - nivel * 0.12
            y1 = y + 0.12
            ax.add_patch(Rectangle((x0, y1), x1 - x0, f["y0"] - y1, fill=False, edgecolor="#333", lw=0.9))
            ax.add_patch(Polygon([(x0, f["y0"]), (x0 + 0.55, f["y0"]), (x0 + 0.55, f["y0"] - 0.14),
                                  (x0 + 0.45, f["y0"] - 0.22), (x0, f["y0"] - 0.22)],
                                 facecolor="#eeeeee", edgecolor="#333", lw=0.8))
            ax.text(x0 + 0.05, f["y0"] - 0.11, f["tipo"], fontsize=8, weight="bold", va="center")
            ax.text(x0 + 0.62, f["y0"] - 0.11, "[" + f["cond"] + "]", fontsize=7.8, va="center")
            for (ys, cond) in f["senoes"]:
                ax.plot([x0, x1], [ys, ys], color="#333", lw=0.8, ls="--")
                ax.text(x0 + 0.1, ys - 0.12, "[" + cond + "]", fontsize=7.8, va="center")
            for g in pilha:
                g["xs"] += [x0 + 0.5, x1 - 0.5]
            y -= esp_y * 0.6
    for x in pos.values():
        ax.plot([x, x], [topo - 0.9, y - 0.2], color="#888", lw=0.9, ls="--", zorder=0)
    ax.set_ylim(y - 0.4, altura)
    fig.set_size_inches(largura, altura - (y - 0.4))
    salvar(fig, nome)


PART_PADRAO = [("U", "Estoquista", "ator"), ("N", "Navegador", "objeto"),
               ("A", "app.py (Flask)", "objeto"), ("M", "", "objeto"), ("DB", "SQLite", "banco")]




# ==================================================================
# DIAGRAMAS DO PETAGENDA
# ==================================================================
def caso_de_uso():
    fig, ax = nova_figura(10.5, 7)
    ax.add_patch(Rectangle((2.6, 0.3), 7.6, 6.3, fill=False, lw=1.3))
    ax.text(6.4, 6.4, "Sistema PetAgenda", ha="center", fontsize=11, weight="bold")
    boneco(ax, 1.0, 3.2, "Atendente", 1.3)

    casos = {
        "UC1": (4.6, 5.6, "UC01 - Manter\nClientes"),
        "UC2": (4.6, 4.45, "UC02 - Manter\nPets"),
        "UC3": (4.6, 3.3, "UC03 - Manter\nServiços"),
        "UC4": (4.6, 2.15, "UC04 - Agendar\nAtendimento"),
        "UC5": (4.6, 1.0, "UC05 - Consultar\nAgenda do Dia"),
        "V": (8.4, 2.15, "Verificar disponibilidade\nde horário"),
        "C": (8.4, 1.0, "Concluir / Cancelar\natendimento"),
    }
    for k, (x, y, txt) in casos.items():
        larg = 2.6 if k in ("V", "C") else 2.4
        ax.add_patch(Ellipse((x, y), larg, 0.8, facecolor=COR_CAIXA, edgecolor=COR_BORDA, lw=1.2))
        ax.text(x, y, txt, ha="center", va="center", fontsize=FONTE)

    for k in ("UC1", "UC2", "UC3", "UC4", "UC5"):
        x, y, _ = casos[k]
        ax.plot([1.3, x - 1.2], [4.0, y], color="black", lw=1)

    seta(ax, 5.8, 2.15, 7.1, 2.15, tracejada=True, aberta=True)
    ax.text(6.45, 2.23, "<<include>>", ha="center", va="bottom", fontsize=8)
    seta(ax, 7.1, 1.0, 5.8, 1.0, tracejada=True, aberta=True)
    ax.text(6.45, 1.08, "<<extend>>", ha="center", va="bottom", fontsize=8)
    # pet depende de cliente (o tutor)
    ax.plot([5.8, 6.5, 6.5], [4.45, 4.45, 5.45], color="black", lw=1, ls="--")
    seta(ax, 6.5, 5.45, 5.75, 5.45, tracejada=True, aberta=True)
    ax.text(6.6, 4.95, "<<include>>\n(selecionar tutor)", fontsize=7.5, va="center")
    salvar(fig, "caso_de_uso")


def der():
    fig, ax = nova_figura(11.5, 7)
    cli = tabela(ax, 0.3, 6.7, 2.7, "cliente",
                 ["PK  id : INTEGER", "nome : TEXT (NOT NULL)", "cpf : TEXT (UNIQUE)",
                  "telefone : TEXT (NOT NULL)", "email : TEXT", "endereco : TEXT"])
    pet = tabela(ax, 4.2, 6.7, 2.8, "pet",
                 ["PK  id : INTEGER", "nome : TEXT (NOT NULL)", "especie : TEXT (NOT NULL)", "raca : TEXT",
                  "porte : TEXT ('P','M','G')", "nascimento : TEXT", "FK  cliente_id : INTEGER"])
    ag = tabela(ax, 8.4, 5.7, 2.9, "agendamento",
                ["PK  id : INTEGER", "FK  pet_id : INTEGER", "FK  servico_id : INTEGER", "data : TEXT",
                 "hora : TEXT", "valor : REAL", "status : TEXT", "observacao : TEXT"])
    srv = tabela(ax, 4.2, 2.6, 2.8, "servico",
                 ["PK  id : INTEGER", "nome : TEXT (UNIQUE)", "descricao : TEXT", "preco : REAL",
                  "duracao_min : INTEGER"])

    ligacao(ax, cli[0] + cli[2], cli[1] + cli[3] - 0.9, pet[0], pet[1] + pet[3] - 0.9, "um", "zero_muitos", "possui")
    ligacao(ax, pet[0] + pet[2], pet[1] + pet[3] - 1.3, ag[0], ag[1] + ag[3] - 0.9, "um", "zero_muitos", "recebe")
    ligacao(ax, srv[0] + srv[2], srv[1] + srv[3] / 2, ag[0], ag[1] + 0.6, "um", "zero_muitos", "é usado em")
    ax.text(0.3, 0.25, "Notação pé de galinha  |  PK = chave primária  |  FK = chave estrangeira  |  "
            "status: AGENDADO, CONCLUIDO ou CANCELADO", fontsize=8, color="#555")
    salvar(fig, "der")


def classes():
    fig, ax = nova_figura(13, 9.5)
    c = classe(ax, 0.3, 9.2, 3.0, "Cliente",
               ["- id : int", "- nome : string", "- cpf : string", "- telefone : string", "- email : string",
                "- endereco : string"],
               ["+ $listar(busca) : Cliente[]", "+ $buscarPorId(id) : Cliente", "+ salvar() : Cliente",
                "+ $excluir(id) : string"])
    p = classe(ax, 4.9, 9.2, 3.0, "Pet",
               ["- id : int", "- nome : string", "- especie : string", "- raca : string", "- porte : string",
                "- nascimento : string", "- clienteId : int"],
               ["+ idade() : int", "+ $listar(clienteId) : Pet[]", "+ $buscarPorId(id) : Pet",
                "+ salvar() : Pet", "+ $excluir(id) : string"])
    s = classe(ax, 0.3, 4.0, 3.0, "Servico",
               ["- id : int", "- nome : string", "- descricao : string", "- preco : float", "- duracaoMin : int"],
               ["+ $listar() : Servico[]", "+ $buscarPorId(id) : Servico", "+ salvar() : Servico",
                "+ $excluir(id) : string"])
    a = classe(ax, 9.6, 7.4, 3.2, "Agendamento",
               ["- id : int", "- petId : int", "- servicoId : int", "- data : string", "- hora : string",
                "- valor : float", "- status : string", "- observacao : string"],
               ["+ validar() : string[]", "+ salvar() : Agendamento", "+ $listar(filtros) : Agendamento[]",
                "+ $buscarPorId(id) : Agendamento", "+ $alterarStatus(id, status) : string",
                "+ $excluir(id) : void", "+ $faturamentoDoMes(anoMes) : float"])

    def assoc(x1, y1, x2, y2, m1, m2, nome):
        xm = (x1 + x2) / 2
        ax.plot([x1, xm, xm, x2], [y1, y1, y2, y2], color="black", lw=1)
        ax.text(x1 + 0.08, y1 + 0.08, m1, fontsize=8)
        ax.text(x2 - 0.08, y2 + 0.08, m2, fontsize=8, ha="right")
        ax.text(xm + 0.08, (y1 + y2) / 2 + 0.1, nome, fontsize=8, style="italic")

    assoc(c[0] + c[2], c[1] + c[3] - 1.0, p[0], p[1] + p[3] - 1.0, "1", "0..*", "possui")
    assoc(p[0] + p[2], p[1] + p[3] - 1.4, a[0], a[1] + a[3] - 1.0, "1", "0..*", "recebe")
    assoc(s[0] + s[2], s[1] + s[3] / 2, a[0], a[1] + 0.8, "1", "0..*", "é usado em")
    ax.text(0.3, 0.2, "Métodos em itálico são estáticos (static no JavaScript).", fontsize=8, color="#555")
    salvar(fig, "classes")


def atividade():
    fig, ax = nova_figura(12, 13)
    ax.add_patch(Rectangle((0.2, 0.2), 3.6, 12.2, fill=False, lw=1.2))
    ax.add_patch(Rectangle((3.8, 0.2), 8.0, 12.2, fill=False, lw=1.2))
    ax.plot([0.2, 11.8], [12.0, 12.0], color="black", lw=1.2)
    ax.text(2.0, 12.2, "Atendente", ha="center", va="center", weight="bold", fontsize=10)
    ax.text(7.8, 12.2, "Sistema", ha="center", va="center", weight="bold", fontsize=10)
    ax.text(6.0, 12.75, "Diagrama de Atividade - Agendar Atendimento", ha="center", fontsize=11, weight="bold")

    def acao(x, y, txt, w=2.8):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.27), w, 0.54, boxstyle="round,pad=0.02,rounding_size=0.18",
                                    facecolor=COR_CAIXA, edgecolor=COR_BORDA, lw=1.2))
        ax.text(x, y, txt, ha="center", va="center", fontsize=8.5)

    def decisao(x, y, txt):
        ax.add_patch(Polygon([(x, y + 0.3), (x + 0.3, y), (x, y - 0.3), (x - 0.3, y)],
                             facecolor="white", edgecolor="black", lw=1.1))
        ax.text(x + 0.38, y + 0.2, txt, fontsize=8, va="bottom")

    def fim(x, y):
        ax.add_patch(Circle((x, y), 0.15, facecolor="white", edgecolor="black", lw=1.2))
        ax.add_patch(Circle((x, y), 0.09, facecolor="black"))

    def rot(x, y, t):
        ax.text(x, y, t, fontsize=8, color="#333")

    X = 6.2
    ax.add_patch(Circle((2.0, 11.6), 0.13, facecolor="black"))
    acao(2.0, 10.9, 'Acessar "Agendamentos"')
    acao(2.0, 10.1, 'Clicar em "Novo agendamento"')
    acao(X, 10.1, "Buscar pets e serviços")
    decisao(X, 9.2, "Existe pet cadastrado?")
    acao(9.4, 9.2, "Redirecionar para\ncadastro de pets", 2.4)
    fim(9.4, 8.45)
    acao(2.0, 8.3, "Selecionar pet, serviço,\ndata e hora")
    acao(2.0, 7.4, 'Clicar em "Salvar"')
    acao(X, 7.4, "Validar campos obrigatórios")
    acao(X, 6.6, "Verificar se data/hora é futura")
    acao(X, 5.8, "Verificar horário de\nfuncionamento (08h às 18h)")
    acao(X, 5.0, "Verificar conflito com outro\nagendamento no mesmo horário")
    decisao(X, 4.2, "Encontrou erro?")
    acao(9.4, 4.2, "Exibir erros no\nformulário", 2.4)
    acao(X, 3.3, "Buscar preço do serviço")
    acao(X, 2.5, "Gravar agendamento\n(status AGENDADO)")
    acao(2.0, 1.6, "Visualizar mensagem\nde sucesso")
    fim(2.0, 0.75)

    seta(ax, 2.0, 11.47, 2.0, 11.17)
    seta(ax, 2.0, 10.63, 2.0, 10.37)
    seta(ax, 3.4, 10.1, X - 1.4, 10.1)
    seta(ax, X, 9.83, X, 9.5)
    seta(ax, X + 0.3, 9.2, 8.2, 9.2); rot(X + 0.9, 9.27, "[não]")
    seta(ax, 9.4, 8.93, 9.4, 8.6)
    ax.plot([X, X, 2.0], [8.9, 8.8, 8.8], color="black", lw=1)
    seta(ax, 2.0, 8.8, 2.0, 8.57); rot(X + 0.08, 8.83, "[sim]")
    seta(ax, 2.0, 8.03, 2.0, 7.67)
    seta(ax, 3.4, 7.4, X - 1.4, 7.4)
    seta(ax, X, 7.13, X, 6.87)
    seta(ax, X, 6.33, X, 6.07)
    seta(ax, X, 5.53, X, 5.27)
    seta(ax, X, 4.73, X, 4.5)
    seta(ax, X + 0.3, 4.2, 8.2, 4.2); rot(X + 0.9, 4.27, "[sim]")
    ax.plot([10.6, 11.3, 11.3, 3.4], [4.2, 4.2, 8.15, 8.15], color="black", lw=1)
    seta(ax, 3.45, 8.15, 3.4, 8.15)
    rot(10.0, 8.22, "corrigir dados")
    seta(ax, X, 3.9, X, 3.57); rot(X + 0.08, 3.7, "[não]")
    seta(ax, X, 3.03, X, 2.77)
    ax.plot([X, X, 2.0], [2.23, 2.05, 2.05], color="black", lw=1)
    seta(ax, 2.0, 2.05, 2.0, 1.87)
    seta(ax, 2.0, 1.33, 2.0, 0.9)
    salvar(fig, "atividade")


PART_PADRAO = [("U", "Atendente", "ator"), ("N", "Navegador", "objeto"),
               ("R", "Rotas (Express)", "objeto"), ("M", "", "objeto"), ("DB", "SQLite", "banco")]


def part(classe_nome):
    return [x if x[0] != "M" else ("M", classe_nome, "objeto") for x in PART_PADRAO]


def seq_crud(nome, titulo, rota, classe_nome, validacao, passos_excluir):
    passos = [
        ("div", "Listar"),
        ("m", "U", "N", "acessa " + rota),
        ("m", "N", "R", "GET " + rota),
        ("m", "R", "M", "listar()"),
        ("m", "M", "DB", "SELECT"),
        ("r", "DB", "M", "registros"),
        ("r", "M", "R", "lista de objetos"),
        ("r", "R", "N", "página com a tabela"),
        ("div", "Cadastrar / Editar"),
        ("m", "U", "N", "preenche o formulário"),
        ("m", "N", "R", "POST " + rota + "/novo ou /:id/editar"),
        ("s", "R", validacao),
        ("alt", "dados inválidos"),
        ("r", "R", "N", "formulário com erros"),
        ("senao", "dados válidos"),
        ("m", "R", "M", "salvar()"),
        ("m", "M", "DB", "INSERT / UPDATE"),
        ("r", "DB", "M", "ok"),
        ("r", "R", "N", "redirect + \"salvo com sucesso\""),
        ("fim",),
        ("div", "Excluir"),
        ("m", "U", "N", "clica em Excluir e confirma"),
        ("m", "N", "R", "POST " + rota + "/:id/excluir"),
        ("m", "R", "M", "excluir(id)"),
    ] + passos_excluir + [("r", "R", "N", "redirect com mensagem")]
    sequencia(nome, titulo, part(classe_nome), passos)


def bloqueio(consulta, motivo):
    return [("m", "M", "DB", consulta),
            ("r", "DB", "M", "total"),
            ("alt", motivo),
            ("r", "M", "R", "mensagem de erro"),
            ("senao", "liberado"),
            ("m", "M", "DB", "DELETE"),
            ("r", "M", "R", "null"),
            ("fim",)]


def sequencias():
    seq_crud("seq_uc01_clientes", "Sequência UC01 - Manter Clientes", "/clientes", "Cliente",
             "valida nome, telefone e CPF", bloqueio("SELECT COUNT(*) FROM pet", "cliente tem pets"))
    seq_crud("seq_uc02_pets", "Sequência UC02 - Manter Pets", "/pets", "Pet",
             "valida nome, espécie, porte e tutor",
             [("m", "M", "DB", "SELECT agendamentos em aberto"),
              ("r", "DB", "M", "total"),
              ("alt", "tem agendamento em aberto"),
              ("r", "M", "R", "mensagem de erro"),
              ("senao", "liberado"),
              ("m", "M", "DB", "DELETE agendamentos do pet"),
              ("m", "M", "DB", "DELETE pet"),
              ("r", "M", "R", "null"),
              ("fim",)])
    seq_crud("seq_uc03_servicos", "Sequência UC03 - Manter Serviços", "/servicos", "Servico",
             "valida nome, preço e duração",
             bloqueio("SELECT COUNT(*) FROM agendamento", "serviço já usado"))

    sequencia("seq_uc04_agendar", "Sequência UC04 - Agendar Atendimento", part("Agendamento"), [
        ("m", "U", "N", "clica em \"Novo agendamento\""),
        ("m", "N", "R", "GET /agendamentos/novo"),
        ("m", "R", "DB", "busca pets e serviços"),
        ("r", "R", "N", "formulário"),
        ("m", "U", "N", "escolhe pet, serviço, data e hora"),
        ("m", "N", "R", "POST /agendamentos/novo"),
        ("m", "R", "M", "new Agendamento(dados)"),
        ("m", "R", "M", "validar()"),
        ("m", "M", "DB", "SELECT conflito de horário"),
        ("r", "DB", "M", "total"),
        ("r", "M", "R", "lista de erros"),
        ("alt", "há erros"),
        ("r", "R", "N", "formulário com os erros"),
        ("senao", "sem erros"),
        ("m", "R", "M", "salvar()"),
        ("m", "M", "DB", "SELECT preco FROM servico"),
        ("r", "DB", "M", "preço"),
        ("m", "M", "DB", "INSERT INTO agendamento"),
        ("r", "M", "R", "agendamento salvo"),
        ("r", "R", "N", "redirect + sucesso"),
        ("fim",),
    ])

    sequencia("seq_uc05_agenda", "Sequência UC05 - Consultar Agenda do Dia", part("Agendamento"), [
        ("m", "U", "N", "acessa a página inicial"),
        ("m", "N", "R", "GET /"),
        ("m", "R", "M", "listar({ data: hoje })"),
        ("m", "M", "DB", "SELECT com JOIN pet/cliente/servico"),
        ("r", "DB", "M", "registros"),
        ("r", "M", "R", "agenda do dia"),
        ("m", "R", "M", "faturamentoDoMes(mes)"),
        ("m", "M", "DB", "SELECT SUM(valor)"),
        ("r", "M", "R", "total"),
        ("r", "R", "N", "painel com indicadores e agenda"),
        ("r", "N", "U", "exibe a agenda"),
        ("opt", "atendente conclui um atendimento"),
        ("m", "U", "N", "clica em \"Concluir\""),
        ("m", "N", "R", "POST /agendamentos/:id/status"),
        ("m", "R", "M", "alterarStatus(id, CONCLUIDO)"),
        ("m", "M", "DB", "UPDATE agendamento"),
        ("r", "R", "N", "redirect para o painel"),
        ("fim",),
    ])


if __name__ == "__main__":
    caso_de_uso()
    der()
    classes()
    atividade()
    sequencias()
