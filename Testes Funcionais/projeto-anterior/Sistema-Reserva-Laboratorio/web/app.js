"use strict";

const byTestId = (id) => document.querySelector(`[data-testid="${id}"]`);
const laboratorioFeedback = byTestId("laboratorio-feedback");
const reservaFeedback = byTestId("reserva-feedback");
const acaoFeedback = byTestId("reserva-acao-feedback");
const laboratorioResultado = byTestId("laboratorio-resultado");
const reservaDetalhes = byTestId("reserva-detalhes");
const reservaAcoes = byTestId("reserva-acoes");
const reservaAprovacao = byTestId("reserva-aprovacao");
const reservaCancelamento = byTestId("reserva-cancelamento");
let reservaAtual;

const laboratorioCampos = {
    id: "ID",
    nome: "Nome",
    capacidade: "Capacidade",
    status: "Status",
};
const reservaCampos = {
    id: "ID",
    laboratorio_id: "ID do laboratório",
    solicitante: "Solicitante",
    data: "Data",
    hora_inicio: "Hora inicial",
    hora_fim: "Hora final",
    status: "Status",
    data_cancelamento: "Data de cancelamento",
};

function mensagemErro(detail) {
    if (Array.isArray(detail)) {
        return detail.map(({ loc, msg }) => {
            const campo = loc?.slice(1).join(".");
            return campo ? `${campo}: ${msg}` : msg;
        }).join(" ");
    }
    return typeof detail === "string" ? detail : "A API não concluiu a operação.";
}

async function enviar(caminho, metodo, corpo) {
    const opcoes = { method: metodo };
    if (corpo !== undefined) {
        opcoes.headers = { "Content-Type": "application/json" };
        opcoes.body = JSON.stringify(corpo);
    }
    const resposta = await fetch(caminho, opcoes);
    const dados = await resposta.json().catch(() => null);
    return { resposta, dados };
}

function mostrarFeedback(elemento, estado, mensagem, status) {
    elemento.dataset.state = estado;
    elemento.dataset.httpStatus = status ?? "";
    elemento.textContent = status ? `HTTP ${status} — ${mensagem}` : mensagem;
}

function mostrarResultado(elemento, dados, campos) {
    const linhas = [];
    for (const [campo, rotulo] of Object.entries(campos)) {
        if (dados[campo] == null) continue;
        const linha = document.createElement("div");
        const titulo = document.createElement("dt");
        const valor = document.createElement("dd");
        titulo.textContent = rotulo;
        valor.textContent = dados[campo];
        valor.dataset.testid = `${elemento.dataset.testid}-${campo}`;
        linha.append(titulo, valor);
        linhas.push(linha);
    }
    elemento.replaceChildren(...linhas);
    elemento.hidden = false;
}

function mostrarReserva(dados) {
    reservaAtual = dados;
    mostrarResultado(byTestId("reserva-resultado"), dados, reservaCampos);
    reservaAprovacao.hidden = dados.status !== "pendente";
    reservaAcoes.hidden = dados.status !== "pendente" && dados.status !== "aprovada";
    reservaDetalhes.hidden = false;
    reservaCancelamento.reset();
}

function vincularFormulario(id, feedback, formulariosDoFluxo, preparar, mensagem, mostrar, limpar) {
    byTestId(id).addEventListener("submit", async (evento) => {
        evento.preventDefault();
        const campos = Object.fromEntries(new FormData(evento.currentTarget));
        const botoes = formulariosDoFluxo.querySelectorAll("button[type='submit']");
        for (const botao of botoes) botao.disabled = true;
        mostrarFeedback(feedback, "pending", "Aguarde…");
        try {
            limpar?.();
            const { resposta, dados } = await enviar(...preparar(campos));
            if (!resposta.ok || dados === null) {
                mostrarFeedback(feedback, "error", mensagemErro(dados?.detail), resposta.status);
                return;
            }
            mostrar(dados);
            mostrarFeedback(feedback, "success", mensagem, resposta.status);
        } catch {
            mostrarFeedback(feedback, "error", "Não foi possível concluir a comunicação com a API.");
        } finally {
            for (const botao of botoes) botao.disabled = false;
        }
    });
}

const laboratorios = document.querySelector("#laboratorios");
const reservas = document.querySelector("#reservas");
const mostrarLaboratorio = (dados) => mostrarResultado(laboratorioResultado, dados, laboratorioCampos);
const limparLaboratorio = () => { laboratorioResultado.hidden = true; };
const limparReserva = () => {
    reservaDetalhes.hidden = true;
    mostrarFeedback(acaoFeedback, "", "");
};
const urlReserva = (id) => `/reservas/${encodeURIComponent(id)}`;

vincularFormulario("laboratorio-cadastro", laboratorioFeedback, laboratorios,
    ({ nome, capacidade }) => ["/laboratorios/", "POST", { nome, capacidade: Number(capacidade) }],
    "Laboratório cadastrado.", mostrarLaboratorio, limparLaboratorio);
vincularFormulario("laboratorio-consulta", laboratorioFeedback, laboratorios,
    ({ id }) => [`/laboratorios/${encodeURIComponent(id)}`, "GET"],
    "Laboratório encontrado.", mostrarLaboratorio, limparLaboratorio);
vincularFormulario("reserva-solicitacao", reservaFeedback, reservas,
    (campos) => ["/reservas/", "POST", campos],
    "Reserva solicitada.", mostrarReserva, limparReserva);
vincularFormulario("reserva-consulta", reservaFeedback, reservas,
    ({ id }) => [urlReserva(id), "GET"],
    "Reserva encontrada.", mostrarReserva, limparReserva);
vincularFormulario("reserva-aprovacao", acaoFeedback, reservas,
    () => [`${urlReserva(reservaAtual.id)}/avaliar`, "PATCH", { acao: "aprovar" }],
    "Reserva aprovada.", mostrarReserva);
vincularFormulario("reserva-cancelamento", acaoFeedback, reservas,
    ({ solicitante }) => [`${urlReserva(reservaAtual.id)}/cancelar`, "PATCH", { solicitante }],
    "Reserva cancelada.", mostrarReserva);
