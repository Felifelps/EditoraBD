"use strict";

const API_MATERIAS = "/materias/";

const STATUS = {
    EM_ANDAMENTO: 0,
    APROVADA: 1,
    REPROVADA: 2
};

const STATUS_LABELS = {
    0: "Em andamento",
    1: "Aprovada",
    2: "Reprovada"
};

const HTTP_STATUS = {
    BAD_REQUEST: 400,
    NOT_FOUND: 404,
    CONFLICT: 409,
    UNPROCESSABLE_ENTITY: 422,
    INTERNAL_SERVER_ERROR: 500
};

const CONFIG = {
    REQUEST_TIMEOUT: 15000,
    ALERT_TIMEOUT: 5000,
    CPF_LENGTH: 11
};

const elementos = {};

let materiaModal = null;
let detalhesMateriaModal = null;
let excluirModal = null;

let materiaParaExcluir = null;
let materiaDetalhesAtual = null;

let carregandoMaterias = false;
let carregandoDetalhes = false;
let salvandoMateria = false;
let excluindoMateria = false;
let alocandoJornalista = false;
let desalocandoJornalista = false;

document.addEventListener(
    "DOMContentLoaded",
    inicializarAplicacao
);

function inicializarAplicacao() {
    inicializarElementos();
    inicializarModais();
    registrarEventos();
    configurarEstadoInicial();
    carregarMaterias();
}

function inicializarElementos() {
    elementos.alertContainer =
        document.getElementById(
            "alertContainer"
        );

    elementos.loadingIndicator =
        document.getElementById(
            "loadingIndicator"
        );

    elementos.materiasTableBody =
        document.getElementById(
            "materiasTableBody"
        );

    elementos.filtroForm =
        document.getElementById(
            "filtroForm"
        );

    elementos.filtroSearch =
        document.getElementById(
            "filtroSearch"
        );

    elementos.filtroStatus =
        document.getElementById(
            "filtroStatus"
        );

    elementos.filtroSetor =
        document.getElementById(
            "filtroSetor"
        );

    elementos.btnNovaMateria =
        document.getElementById(
            "btnNovaMateria"
        );

    elementos.materiaForm =
        document.getElementById(
            "materiaForm"
        );

    elementos.materiaModal =
        document.getElementById(
            "materiaModal"
        );

    elementos.materiaModalLabel =
        document.getElementById(
            "materiaModalLabel"
        );

    elementos.btnSalvarMateria =
        document.getElementById(
            "btnSalvarMateria"
        );

    elementos.materiaId =
        document.getElementById(
            "materiaId"
        );

    elementos.titulo =
        document.getElementById(
            "titulo"
        );

    elementos.subtitulo =
        document.getElementById(
            "subtitulo"
        );

    elementos.resumo =
        document.getElementById(
            "resumo"
        );

    elementos.conteudo =
        document.getElementById(
            "conteudo"
        );

    elementos.data =
        document.getElementById(
            "data"
        );

    elementos.status =
        document.getElementById(
            "status"
        );

    elementos.idSetor =
        document.getElementById(
            "id_setor"
        );

    elementos.nomeJornal =
        document.getElementById(
            "nome_jornal"
        );

    elementos.numeroEdicao =
        document.getElementById(
            "numero_edicao"
        );

    elementos.cpfEditorChefe =
        document.getElementById(
            "cpf_editor_chefe"
        );

    elementos.detalhesMateriaModal =
        document.getElementById(
            "detalhesMateriaModal"
        );

    elementos.detalhesMateriaModalLabel =
        document.getElementById(
            "detalhesMateriaModalLabel"
        );

    elementos.detalhesLoading =
        document.getElementById(
            "detalhesLoading"
        );

    elementos.detalhesMateriaConteudo =
        document.getElementById(
            "detalhesMateriaConteudo"
        );

    elementos.detalhesTitulo =
        document.getElementById(
            "detalhesTitulo"
        );

    elementos.detalhesStatus =
        document.getElementById(
            "detalhesStatus"
        );

    elementos.detalhesMateriaSubtitulo =
        document.getElementById(
            "detalhesMateriaSubtitulo"
        );

    elementos.detalhesSubtitulo =
        document.getElementById(
            "detalhesSubtitulo"
        );

    elementos.detalhesResumo =
        document.getElementById(
            "detalhesResumo"
        );

    elementos.detalhesConteudo =
        document.getElementById(
            "detalhesConteudo"
        );

    elementos.detalhesData =
        document.getElementById(
            "detalhesData"
        );

    elementos.detalhesJornal =
        document.getElementById(
            "detalhesJornal"
        );

    elementos.detalhesEdicao =
        document.getElementById(
            "detalhesEdicao"
        );

    elementos.detalhesSetor =
        document.getElementById(
            "detalhesSetor"
        );

    elementos.alocarJornalistaForm =
        document.getElementById(
            "alocarJornalistaForm"
        );

    elementos.cpfJornalista =
        document.getElementById(
            "cpfJornalista"
        );

    elementos.btnAlocarJornalista =
        document.getElementById(
            "btnAlocarJornalista"
        );

    elementos.jornalistasTableBody =
        document.getElementById(
            "jornalistasTableBody"
        );

    elementos.excluirModal =
        document.getElementById(
            "excluirModal"
        );

    elementos.btnConfirmarExclusao =
        document.getElementById(
            "btnConfirmarExclusao"
        );
}

function inicializarModais() {
    if (
        elementos.materiaModal &&
        window.bootstrap
    ) {
        materiaModal =
            bootstrap.Modal.getOrCreateInstance(
                elementos.materiaModal
            );
    }

    if (
        elementos.detalhesMateriaModal &&
        window.bootstrap
    ) {
        detalhesMateriaModal =
            bootstrap.Modal.getOrCreateInstance(
                elementos.detalhesMateriaModal
            );
    }

    if (
        elementos.excluirModal &&
        window.bootstrap
    ) {
        excluirModal =
            bootstrap.Modal.getOrCreateInstance(
                elementos.excluirModal
            );
    }
}

function registrarEventos() {
    elementos.btnNovaMateria?.addEventListener(
        "click",
        abrirFormularioNovaMateria
    );

    elementos.filtroForm?.addEventListener(
        "submit",
        tratarSubmitFiltro
    );

    elementos.materiaForm?.addEventListener(
        "submit",
        salvarMateria
    );

    elementos.btnConfirmarExclusao?.addEventListener(
        "click",
        excluirMateria
    );

    elementos.alocarJornalistaForm?.addEventListener(
        "submit",
        tratarSubmitAlocacao
    );

    elementos.btnAlocarJornalista?.addEventListener(
        "click",
        tratarCliqueAlocacao
    );

    elementos.cpfJornalista?.addEventListener(
        "input",
        tratarInputCpf
    );

    elementos.cpfJornalista?.addEventListener(
        "keydown",
        tratarTeclaCpf
    );

    elementos.detalhesMateriaModal?.addEventListener(
        "hidden.bs.modal",
        tratarFechamentoModalDetalhes
    );

    elementos.materiaModal?.addEventListener(
        "hidden.bs.modal",
        tratarFechamentoModalMateria
    );

    elementos.excluirModal?.addEventListener(
        "hidden.bs.modal",
        tratarFechamentoModalExclusao
    );

    document.addEventListener(
        "click",
        tratarCliqueDelegado
    );
}

function configurarEstadoInicial() {
    if (
        elementos.status &&
        elementos.status.value === ""
    ) {
        elementos.status.value =
            String(
                STATUS.EM_ANDAMENTO
            );
    }

    limparListaJornalistas();
}

function tratarSubmitFiltro(evento) {
    evento.preventDefault();
    carregarMaterias();
}

function tratarSubmitAlocacao(evento) {
    evento.preventDefault();
    evento.stopPropagation();

    alocarJornalista();
}

function tratarCliqueAlocacao(evento) {
    evento.preventDefault();
    evento.stopPropagation();

    if (
        alocandoJornalista
    ) {
        return;
    }

    alocarJornalista();
}

function tratarInputCpf(evento) {
    if (
        !evento?.target
    ) {
        return;
    }

    evento.target.value =
        normalizarCpf(
            evento.target.value
        );
}

function tratarTeclaCpf(evento) {
    if (
        evento.key !== "Enter"
    ) {
        return;
    }

    evento.preventDefault();
    evento.stopPropagation();

    alocarJornalista();
}

function tratarCliqueDelegado(evento) {
    const botao =
        evento.target.closest(
            '[data-action="desalocar"]'
        );

    if (!botao) {
        return;
    }

    const cpf =
        botao.dataset.cpf;

    if (!cpf) {
        return;
    }

    evento.preventDefault();
    evento.stopPropagation();

    desalocarJornalista(
        cpf,
        botao
    );
}

async function carregarMaterias() {
    if (
        carregandoMaterias
    ) {
        return;
    }

    carregandoMaterias = true;

    mostrarLoading(true);

    try {
        const parametros =
            construirParametrosFiltro();

        const url =
            construirUrlApi(
                API_MATERIAS,
                parametros
            );

        const dados =
            await requisicaoApi(
                url,
                {
                    method: "GET",
                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );

        const materias =
            extrairListaMaterias(
                dados
            );

        renderizarMaterias(
            materias
        );
    } catch (erro) {
        console.error(
            "Erro ao carregar matérias:",
            erro
        );

        mostrarAlerta(
            obterMensagemErro(
                erro
            ),
            "danger"
        );

        renderizarMaterias(
            []
        );
    } finally {
        carregandoMaterias = false;
        mostrarLoading(false);
    }
}

function construirParametrosFiltro() {
    const parametros =
        new URLSearchParams();

    const search =
        elementos.filtroSearch?.value
            ?.trim();

    const status =
        elementos.filtroStatus?.value;

    const setorId =
        elementos.filtroSetor?.value
            ?.trim();

    if (search) {
        parametros.set(
            "search",
            search
        );
    }

    if (
        status !== undefined &&
        status !== null &&
        status !== ""
    ) {
        parametros.set(
            "status",
            status
        );
    }

    if (setorId) {
        parametros.set(
            "setor_id",
            setorId
        );
    }

    return parametros;
}

function construirUrlApi(
    endpoint,
    parametros
) {
    if (
        !parametros
    ) {
        return endpoint;
    }

    const query =
        parametros.toString();

    if (!query) {
        return endpoint;
    }

    return `${endpoint}?${query}`;
}

function extrairListaMaterias(
    dados
) {
    if (
        Array.isArray(dados)
    ) {
        return dados;
    }

    if (
        !dados ||
        typeof dados !== "object"
    ) {
        return [];
    }

    const propriedades = [
        "items",
        "results",
        "data",
        "materias"
    ];

    for (
        const propriedade
        of propriedades
    ) {
        if (
            Array.isArray(
                dados[
                    propriedade
                ]
            )
        ) {
            return dados[
                propriedade
            ];
        }
    }

    return [];
}

function renderizarMaterias(
    materias
) {
    if (
        !elementos.materiasTableBody
    ) {
        return;
    }

    elementos.materiasTableBody.innerHTML =
        "";

    if (
        !Array.isArray(materias) ||
        materias.length === 0
    ) {
        elementos.materiasTableBody.innerHTML = `
            <tr id="emptyState">
                <td
                    colspan="7"
                    class="text-center text-muted py-5"
                >
                    Nenhuma matéria encontrada.
                </td>
            </tr>
        `;

        return;
    }

    const fragment =
        document.createDocumentFragment();

    materias.forEach(
        materia => {
            fragment.appendChild(
                criarLinhaMateria(
                    materia
                )
            );
        }
    );

    elementos.materiasTableBody.appendChild(
        fragment
    );
}

function criarLinhaMateria(
    materia
) {
    const linha =
        document.createElement(
            "tr"
        );

    const id =
        materia?.id_materia ??
        "";

    const titulo =
        materia?.titulo ??
        "Sem título";

    const nomeJornal =
        materia?.nome_jornal ??
        "-";

    const numeroEdicao =
        materia?.numero_edicao ??
        "-";

    const data =
        formatarData(
            materia?.data
        );

    const status =
        obterStatus(
            materia?.status
        );

    linha.dataset.materiaId =
        String(
            id
        );

    linha.innerHTML = `
        <td>
            ${escapeHtml(id)}
        </td>

        <td>
            <button
                type="button"
                class="btn btn-link p-0 text-start fw-semibold text-decoration-none"
                data-action="detalhes"
            >
                ${escapeHtml(titulo)}
            </button>
        </td>

        <td>
            ${escapeHtml(nomeJornal)}
        </td>

        <td>
            ${escapeHtml(numeroEdicao)}
        </td>

        <td>
            ${escapeHtml(data)}
        </td>

        <td>
            ${criarBadgeStatus(status)}
        </td>

        <td>
            <div class="acoes-materia">
                <button
                    type="button"
                    class="btn btn-sm btn-outline-primary"
                    data-action="editar"
                >
                    Editar
                </button>

                <button
                    type="button"
                    class="btn btn-sm btn-outline-danger"
                    data-action="excluir"
                >
                    Excluir
                </button>
            </div>
        </td>
    `;

    const detalhes =
        linha.querySelector(
            '[data-action="detalhes"]'
        );

    detalhes?.addEventListener(
        "click",
        evento => {
            evento.preventDefault();
            abrirDetalhesMateria(
                materia
            );
        }
    );

    const editar =
        linha.querySelector(
            '[data-action="editar"]'
        );

    editar?.addEventListener(
        "click",
        evento => {
            evento.preventDefault();
            abrirFormularioEdicao(
                materia
            );
        }
    );

    const excluir =
        linha.querySelector(
            '[data-action="excluir"]'
        );

    excluir?.addEventListener(
        "click",
        evento => {
            evento.preventDefault();
            abrirConfirmacaoExclusao(
                materia
            );
        }
    );

    return linha;
}

async function abrirDetalhesMateria(
    materia
) {
    const id =
        materia?.id_materia;

    if (
        id === undefined ||
        id === null
    ) {
        mostrarAlerta(
            "Não foi possível identificar a matéria.",
            "danger"
        );

        return;
    }

    materiaDetalhesAtual = {
        ...materia
    };

    limparDetalhesMateria();

    detalhesMateriaModal?.show();

    carregandoDetalhes = true;

    mostrarLoadingDetalhes(
        true
    );

    atualizarEstadoFormularioAlocacao();

    try {
        const dados =
            await requisicaoApi(
                `${API_MATERIAS}${encodeURIComponent(id)}`,
                {
                    method: "GET",
                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );

        if (
            dados &&
            typeof dados ===
                "object"
        ) {
            materiaDetalhesAtual = {
                ...materiaDetalhesAtual,
                ...dados
            };
        }

        preencherDetalhesMateria(
            materiaDetalhesAtual
        );

        await carregarJornalistas(
            id
        );
    } catch (erro) {
        console.error(
            "Erro ao carregar detalhes:",
            erro
        );

        mostrarAlerta(
            obterMensagemErro(
                erro
            ),
            "danger"
        );
    } finally {
        carregandoDetalhes = false;

        mostrarLoadingDetalhes(
            false
        );

        atualizarEstadoFormularioAlocacao();
    }
}

function preencherDetalhesMateria(
    materia
) {
    if (!materia) {
        return;
    }

    if (
        elementos.detalhesMateriaModalLabel
    ) {
        elementos.detalhesMateriaModalLabel.textContent =
            materia.titulo ??
            "Detalhes da matéria";
    }

    if (
        elementos.detalhesTitulo
    ) {
        elementos.detalhesTitulo.textContent =
            materia.titulo ??
            "-";
    }

    if (
        elementos.detalhesMateriaSubtitulo
    ) {
        elementos.detalhesMateriaSubtitulo.textContent =
            materia.subtitulo ??
            "";
    }

    if (
        elementos.detalhesSubtitulo
    ) {
        elementos.detalhesSubtitulo.textContent =
            materia.subtitulo ??
            "-";
    }

    if (
        elementos.detalhesResumo
    ) {
        elementos.detalhesResumo.textContent =
            materia.resumo ??
            "-";
    }

    if (
        elementos.detalhesConteudo
    ) {
        elementos.detalhesConteudo.textContent =
            materia.conteudo ??
            "-";
    }

    if (
        elementos.detalhesData
    ) {
        elementos.detalhesData.textContent =
            formatarData(
                materia.data
            );
    }

    if (
        elementos.detalhesJornal
    ) {
        elementos.detalhesJornal.textContent =
            materia.nome_jornal ??
            "-";
    }

    if (
        elementos.detalhesEdicao
    ) {
        elementos.detalhesEdicao.textContent =
            materia.numero_edicao ??
            "-";
    }

    if (
        elementos.detalhesSetor
    ) {
        elementos.detalhesSetor.textContent =
            materia.id_setor ??
            "-";
    }

    if (
        elementos.detalhesStatus
    ) {
        elementos.detalhesStatus.innerHTML =
            criarBadgeStatus(
                obterStatus(
                    materia.status
                )
            );
    }
}

function limparDetalhesMateria() {
    const campos = [
        elementos.detalhesTitulo,
        elementos.detalhesMateriaSubtitulo,
        elementos.detalhesSubtitulo,
        elementos.detalhesResumo,
        elementos.detalhesConteudo,
        elementos.detalhesData,
        elementos.detalhesJornal,
        elementos.detalhesEdicao,
        elementos.detalhesSetor
    ];

    campos.forEach(
        elemento => {
            if (elemento) {
                elemento.textContent =
                    "";
            }
        }
    );

    if (
        elementos.detalhesStatus
    ) {
        elementos.detalhesStatus.innerHTML =
            "";
    }

    if (
        elementos.detalhesMateriaModalLabel
    ) {
        elementos.detalhesMateriaModalLabel.textContent =
            "Detalhes da matéria";
    }

    limparListaJornalistas();
}

async function carregarJornalistas(
    materiaId
) {
    if (
        !elementos.jornalistasTableBody
    ) {
        return;
    }

    if (
        materiaId === undefined ||
        materiaId === null
    ) {
        limparListaJornalistas();
        return;
    }

    renderizarCarregandoJornalistas();

    try {
        const endpoint =
            `${API_MATERIAS}` +
            `${encodeURIComponent(
                materiaId
            )}` +
            `/jornalistas`;

        const dados =
            await requisicaoApi(
                endpoint,
                {
                    method: "GET",
                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );

        const jornalistas =
            extrairListaJornalistas(
                dados
            );

        renderizarJornalistas(
            jornalistas
        );
    } catch (erro) {
        console.error(
            "Erro ao carregar jornalistas:",
            erro
        );

        renderizarErroJornalistas(
            obterMensagemErro(
                erro
            )
        );
    }
}

function extrairListaJornalistas(
    dados
) {
    if (
        Array.isArray(dados)
    ) {
        return dados;
    }

    if (
        !dados ||
        typeof dados !==
            "object"
    ) {
        return [];
    }

    const propriedades = [
        "items",
        "results",
        "data",
        "jornalistas"
    ];

    for (
        const propriedade
        of propriedades
    ) {
        if (
            Array.isArray(
                dados[
                    propriedade
                ]
            )
        ) {
            return dados[
                propriedade
            ];
        }
    }

    return [];
}

function extrairCpfJornalista(
    jornalista
) {
    if (
        typeof jornalista ===
        "string"
    ) {
        return jornalista;
    }

    if (
        !jornalista ||
        typeof jornalista !==
            "object"
    ) {
        return "";
    }

    return (
        jornalista.cpf_jornalista ??
        jornalista.cpf ??
        jornalista.CPF ??
        ""
    );
}

function renderizarCarregandoJornalistas() {
    if (
        !elementos.jornalistasTableBody
    ) {
        return;
    }

    elementos.jornalistasTableBody.innerHTML = `
        <tr>
            <td
                colspan="2"
                class="text-center text-muted py-4"
            >
                <span
                    class="spinner-border spinner-border-sm me-2"
                    role="status"
                    aria-hidden="true"
                ></span>
                Carregando jornalistas...
            </td>
        </tr>
    `;
}

function renderizarErroJornalistas(
    mensagem
) {
    if (
        !elementos.jornalistasTableBody
    ) {
        return;
    }

    elementos.jornalistasTableBody.innerHTML = `
        <tr>
            <td
                colspan="2"
                class="text-center text-danger py-4"
            >
                ${escapeHtml(
                    mensagem ||
                    "Não foi possível carregar os jornalistas."
                )}
            </td>
        </tr>
    `;
}

function renderizarJornalistas(
    jornalistas
) {
    if (
        !elementos.jornalistasTableBody
    ) {
        return;
    }

    elementos.jornalistasTableBody.innerHTML =
        "";

    if (
        !Array.isArray(jornalistas) ||
        jornalistas.length === 0
    ) {
        limparListaJornalistas();
        return;
    }

    const fragment =
        document.createDocumentFragment();

    const cpfs =
        new Set();

    jornalistas.forEach(
        jornalista => {
            const cpf =
                normalizarCpf(
                    extrairCpfJornalista(
                        jornalista
                    )
                );

            if (!cpf) {
                return;
            }

            if (
                cpfs.has(cpf)
            ) {
                return;
            }

            cpfs.add(cpf);

            fragment.appendChild(
                criarLinhaJornalista(
                    cpf
                )
            );
        }
    );

    if (
        fragment.childNodes.length ===
        0
    ) {
        limparListaJornalistas();
        return;
    }

    elementos.jornalistasTableBody.appendChild(
        fragment
    );
}

function criarLinhaJornalista(
    cpf
) {
    const linha =
        document.createElement(
            "tr"
        );

    linha.dataset.cpf =
        cpf;

    linha.innerHTML = `
        <td>
            ${escapeHtml(cpf)}
        </td>

        <td class="text-end">
            <button
                type="button"
                class="btn btn-sm btn-outline-danger"
                data-action="desalocar"
                data-cpf="${escapeHtml(cpf)}"
            >
                Desalocar
            </button>
        </td>
    `;

    return linha;
}

function limparListaJornalistas() {
    if (
        !elementos.jornalistasTableBody
    ) {
        return;
    }

    elementos.jornalistasTableBody.innerHTML = `
        <tr id="jornalistasEmptyState">
            <td
                colspan="2"
                class="text-center text-muted py-4"
            >
                Nenhum jornalista alocado.
            </td>
        </tr>
    `;
}

async function alocarJornalista() {
    if (
        alocandoJornalista
    ) {
        return;
    }

    if (
        !materiaDetalhesAtual ||
        materiaDetalhesAtual.id_materia ===
            undefined ||
        materiaDetalhesAtual.id_materia ===
            null
    ) {
        mostrarAlerta(
            "Nenhuma matéria está aberta.",
            "warning"
        );

        return;
    }

    if (
        !elementos.cpfJornalista
    ) {
        mostrarAlerta(
            "Campo de CPF do jornalista não encontrado.",
            "danger"
        );

        return;
    }

    const materiaId =
        materiaDetalhesAtual.id_materia;

    const cpf =
        normalizarCpf(
            elementos.cpfJornalista.value
        );

    if (!cpf) {
        mostrarAlerta(
            "Informe o CPF do jornalista.",
            "warning"
        );

        elementos.cpfJornalista.focus();

        return;
    }

    if (
        cpf.length !==
        CONFIG.CPF_LENGTH
    ) {
        mostrarAlerta(
            "O CPF deve conter 11 dígitos.",
            "warning"
        );

        elementos.cpfJornalista.focus();

        return;
    }

    alocandoJornalista = true;

    atualizarEstadoBotaoAlocacao(
        true
    );

    try {
        const parametros =
            new URLSearchParams();

        parametros.set(
            "cpf_jornalista",
            cpf
        );

        const endpoint =
            `${API_MATERIAS}` +
            `${encodeURIComponent(
                materiaId
            )}` +
            `/jornalistas?` +
            parametros.toString();

        const dados =
            await requisicaoApi(
                endpoint,
                {
                    method: "POST",
                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );

        elementos.cpfJornalista.value =
            "";

        mostrarAlerta(
            obterMensagemSucesso(
                dados,
                "Jornalista alocado com sucesso."
            ),
            "success"
        );

        await carregarJornalistas(
            materiaId
        );
    } catch (erro) {
        console.error(
            "Erro ao alocar jornalista:",
            erro
        );

        mostrarAlerta(
            obterMensagemErro(
                erro
            ),
            "danger"
        );
    } finally {
        alocandoJornalista = false;

        atualizarEstadoBotaoAlocacao(
            false
        );
    }
}

function atualizarEstadoBotaoAlocacao(
    carregando
) {
    const botao =
        elementos.btnAlocarJornalista;

    if (!botao) {
        return;
    }

    botao.disabled =
        carregando;

    if (
        carregando
    ) {
        botao.innerHTML = `
            <span
                class="spinner-border spinner-border-sm me-1"
                role="status"
                aria-hidden="true"
            ></span>
            Alocando...
        `;
    } else {
        botao.textContent =
            "Alocar";
    }

    if (
        elementos.cpfJornalista
    ) {
        elementos.cpfJornalista.disabled =
            carregando;
    }
}

async function desalocarJornalista(
    cpf,
    botao = null
) {
    if (
        desalocandoJornalista
    ) {
        return;
    }

    if (
        !materiaDetalhesAtual ||
        materiaDetalhesAtual.id_materia ===
            undefined ||
        materiaDetalhesAtual.id_materia ===
            null
    ) {
        mostrarAlerta(
            "Nenhuma matéria está aberta.",
            "warning"
        );

        return;
    }

    const materiaId =
        materiaDetalhesAtual.id_materia;

    const cpfNormalizado =
        normalizarCpf(
            cpf
        );

    if (
        cpfNormalizado.length !==
        CONFIG.CPF_LENGTH
    ) {
        mostrarAlerta(
            "CPF do jornalista inválido.",
            "warning"
        );

        return;
    }

    const confirmar =
        window.confirm(
            `Deseja desalocar o jornalista ${cpfNormalizado}?`
        );

    if (!confirmar) {
        return;
    }

    desalocandoJornalista = true;

    atualizarEstadoBotaoDesalocacao(
        botao,
        true
    );

    try {
        const endpoint =
            `${API_MATERIAS}` +
            `${encodeURIComponent(
                materiaId
            )}` +
            `/jornalistas/` +
            `${encodeURIComponent(
                cpfNormalizado
            )}`;

        const dados =
            await requisicaoApi(
                endpoint,
                {
                    method: "DELETE",
                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );

        mostrarAlerta(
            obterMensagemSucesso(
                dados,
                "Jornalista desalocado com sucesso."
            ),
            "success"
        );

        await carregarJornalistas(
            materiaId
        );
    } catch (erro) {
        console.error(
            "Erro ao desalocar jornalista:",
            erro
        );

        mostrarAlerta(
            obterMensagemErro(
                erro
            ),
            "danger"
        );

        atualizarEstadoBotaoDesalocacao(
            botao,
            false
        );
    } finally {
        desalocandoJornalista = false;
    }
}

function atualizarEstadoBotaoDesalocacao(
    botao,
    carregando
) {
    if (!botao) {
        return;
    }

    botao.disabled =
        carregando;

    if (
        carregando
    ) {
        botao.innerHTML = `
            <span
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
            ></span>
            Removendo...
        `;
    } else {
        botao.textContent =
            "Desalocar";
    }
}

function obterMensagemSucesso(
    dados,
    padrao
) {
    if (
        dados &&
        typeof dados ===
            "object"
    ) {
        if (
            dados.message
        ) {
            return String(
                dados.message
            );
        }

        if (
            dados.mensagem
        ) {
            return String(
                dados.mensagem
            );
        }

        if (
            typeof dados.detail ===
            "string"
        ) {
            return dados.detail;
        }
    }

    return padrao;
}

function abrirFormularioNovaMateria() {
    limparFormulario();

    if (
        elementos.materiaModalLabel
    ) {
        elementos.materiaModalLabel.textContent =
            "Nova matéria";
    }

    if (
        elementos.btnSalvarMateria
    ) {
        elementos.btnSalvarMateria.textContent =
            "Salvar";
    }

    materiaModal?.show();
}

function abrirFormularioEdicao(
    materia
) {
    limparFormulario();

    if (
        elementos.materiaModalLabel
    ) {
        elementos.materiaModalLabel.textContent =
            "Editar matéria";
    }

    if (
        elementos.btnSalvarMateria
    ) {
        elementos.btnSalvarMateria.textContent =
            "Atualizar";
    }

    if (
        elementos.materiaId
    ) {
        elementos.materiaId.value =
            materia.id_materia ??
            "";
    }

    if (
        elementos.titulo
    ) {
        elementos.titulo.value =
            materia.titulo ??
            "";
    }

    if (
        elementos.subtitulo
    ) {
        elementos.subtitulo.value =
            materia.subtitulo ??
            "";
    }

    if (
        elementos.resumo
    ) {
        elementos.resumo.value =
            materia.resumo ??
            "";
    }

    if (
        elementos.conteudo
    ) {
        elementos.conteudo.value =
            materia.conteudo ??
            "";
    }

    if (
        elementos.data
    ) {
        elementos.data.value =
            formatarDataParaInput(
                materia.data
            );
    }

    if (
        elementos.status
    ) {
        elementos.status.value =
            String(
                normalizarStatus(
                    materia.status
                )
            );
    }

    if (
        elementos.idSetor
    ) {
        elementos.idSetor.value =
            materia.id_setor ??
            "";
    }

    if (
        elementos.nomeJornal
    ) {
        elementos.nomeJornal.value =
            materia.nome_jornal ??
            "";
    }

    if (
        elementos.numeroEdicao
    ) {
        elementos.numeroEdicao.value =
            materia.numero_edicao ??
            "";
    }

    if (
        elementos.cpfEditorChefe
    ) {
        elementos.cpfEditorChefe.value =
            materia.cpf_editor_chefe ??
            "";
    }

    materiaModal?.show();
}

function limparFormulario() {
    elementos.materiaForm?.reset();

    if (
        elementos.materiaId
    ) {
        elementos.materiaId.value =
            "";
    }

    if (
        elementos.status
    ) {
        elementos.status.value =
            String(
                STATUS.EM_ANDAMENTO
            );
    }
}

function obterDadosFormulario() {
    const dados = {
        titulo:
            elementos.titulo?.value
                ?.trim() ??
            "",

        subtitulo:
            elementos.subtitulo?.value
                ?.trim() ??
            "",

        resumo:
            elementos.resumo?.value
                ?.trim() ??
            "",

        conteudo:
            elementos.conteudo?.value
                ?.trim() ??
            "",

        data:
            elementos.data?.value ??
            "",

        status:
            Number(
                elementos.status?.value
            ),

        nome_jornal:
            elementos.nomeJornal?.value
                ?.trim() ??
            "",

        numero_edicao:
            converterNumeroOuNull(
                elementos.numeroEdicao?.value
            ),

        id_setor:
            converterNumeroOuNull(
                elementos.idSetor?.value
            ),

        cpf_editor_chefe:
            elementos.cpfEditorChefe?.value
                ?.trim() ||
            null
    };

    return removerCamposOpcionaisVazios(
        dados
    );
}

function removerCamposOpcionaisVazios(
    dados
) {
    const resultado = {
        ...dados
    };

    if (
        resultado.subtitulo === ""
    ) {
        delete resultado.subtitulo;
    }

    if (
        resultado.resumo === ""
    ) {
        delete resultado.resumo;
    }

    if (
        resultado.nome_jornal === ""
    ) {
        delete resultado.nome_jornal;
    }

    if (
        resultado.numero_edicao ===
        null
    ) {
        delete resultado.numero_edicao;
    }

    if (
        resultado.id_setor ===
        null
    ) {
        delete resultado.id_setor;
    }

    if (
        !resultado.cpf_editor_chefe
    ) {
        delete resultado.cpf_editor_chefe;
    }

    return resultado;
}

function validarFormulario(
    dados
) {
    if (!dados.titulo) {
        mostrarAlerta(
            "O título da matéria é obrigatório.",
            "warning"
        );

        elementos.titulo?.focus();

        return false;
    }

    if (
        dados.titulo.length >
        255
    ) {
        mostrarAlerta(
            "O título da matéria deve possuir no máximo 255 caracteres.",
            "warning"
        );

        elementos.titulo?.focus();

        return false;
    }

    if (!dados.conteudo) {
        mostrarAlerta(
            "O conteúdo da matéria é obrigatório.",
            "warning"
        );

        elementos.conteudo?.focus();

        return false;
    }

    if (!dados.data) {
        mostrarAlerta(
            "A data da matéria é obrigatória.",
            "warning"
        );

        elementos.data?.focus();

        return false;
    }

    if (
        !Number.isInteger(
            dados.status
        ) ||
        ![
            STATUS.EM_ANDAMENTO,
            STATUS.APROVADA,
            STATUS.REPROVADA
        ].includes(
            dados.status
        )
    ) {
        mostrarAlerta(
            "O status informado é inválido.",
            "warning"
        );

        elementos.status?.focus();

        return false;
    }

    if (
        dados.id_setor !==
            null &&
        (
            !Number.isInteger(
                dados.id_setor
            ) ||
            dados.id_setor <= 0
        )
    ) {
        mostrarAlerta(
            "O setor informado é inválido.",
            "warning"
        );

        elementos.idSetor?.focus();

        return false;
    }

    if (
        dados.numero_edicao !==
            null &&
        (
            !Number.isInteger(
                dados.numero_edicao
            ) ||
            dados.numero_edicao <= 0
        )
    ) {
        mostrarAlerta(
            "O número da edição informado é inválido.",
            "warning"
        );

        elementos.numeroEdicao?.focus();

        return false;
    }

    if (
        dados.cpf_editor_chefe &&
        normalizarCpf(
            dados.cpf_editor_chefe
        ).length !==
            CONFIG.CPF_LENGTH
    ) {
        mostrarAlerta(
            "O CPF do editor-chefe deve conter 11 dígitos.",
            "warning"
        );

        elementos.cpfEditorChefe?.focus();

        return false;
    }

    return true;
}

async function salvarMateria(
    evento
) {
    evento.preventDefault();

    if (
        salvandoMateria
    ) {
        return;
    }

    const id =
        elementos.materiaId?.value
            ?.trim() ??
        "";

    const dados =
        obterDadosFormulario();

    if (
        !validarFormulario(
            dados
        )
    ) {
        return;
    }

    const editando =
        id !== "";

    const endpoint =
        editando
            ? `${API_MATERIAS}${encodeURIComponent(id)}`
            : API_MATERIAS;

    const metodo =
        editando
            ? "PUT"
            : "POST";

    salvandoMateria = true;

    alterarEstadoBotaoSalvar(
        true
    );

    try {
        const resposta =
            await fetch(
                endpoint,
                {
                    method: metodo,
                    headers: {
                        "Content-Type":
                            "application/json",
                        "Accept":
                            "application/json"
                    },
                    body:
                        JSON.stringify(
                            dados
                        )
                }
            );

        await processarResposta(
            resposta
        );

        materiaModal?.hide();

        mostrarAlerta(
            editando
                ? "Matéria atualizada com sucesso."
                : "Matéria cadastrada com sucesso.",
            "success"
        );

        await carregarMaterias();
    } catch (erro) {
        console.error(
            "Erro ao salvar matéria:",
            erro
        );

        mostrarAlerta(
            obterMensagemErro(
                erro
            ),
            "danger"
        );
    } finally {
        salvandoMateria = false;

        alterarEstadoBotaoSalvar(
            false
        );
    }
}

function alterarEstadoBotaoSalvar(
    carregando
) {
    if (
        !elementos.btnSalvarMateria
    ) {
        return;
    }

    elementos.btnSalvarMateria.disabled =
        carregando;

    if (
        carregando
    ) {
        elementos.btnSalvarMateria.innerHTML = `
            <span
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
            ></span>
            Salvando...
        `;

        return;
    }

    const editando =
        (
            elementos.materiaId?.value
                ?.trim() ??
            ""
        ) !== "";

    elementos.btnSalvarMateria.textContent =
        editando
            ? "Atualizar"
            : "Salvar";
}

function abrirConfirmacaoExclusao(
    materia
) {
    if (
        !materia ||
        materia.id_materia ===
            undefined ||
        materia.id_materia ===
            null
    ) {
        mostrarAlerta(
            "Não foi possível identificar a matéria.",
            "danger"
        );

        return;
    }

    materiaParaExcluir =
        materia;

    excluirModal?.show();
}

async function excluirMateria() {
    if (
        excluindoMateria
    ) {
        return;
    }

    if (
        !materiaParaExcluir ||
        materiaParaExcluir.id_materia ===
            undefined ||
        materiaParaExcluir.id_materia ===
            null
    ) {
        mostrarAlerta(
            "Não foi possível identificar a matéria.",
            "danger"
        );

        return;
    }

    const id =
        materiaParaExcluir.id_materia;

    excluindoMateria = true;

    if (
        elementos.btnConfirmarExclusao
    ) {
        elementos.btnConfirmarExclusao.disabled =
            true;
    }

    try {
        const resposta =
            await fetch(
                `${API_MATERIAS}${encodeURIComponent(id)}`,
                {
                    method: "DELETE",
                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );

        await processarResposta(
            resposta
        );

        excluirModal?.hide();

        mostrarAlerta(
            "Matéria excluída com sucesso.",
            "success"
        );

        if (
            materiaDetalhesAtual?.id_materia ===
            id
        ) {
            materiaDetalhesAtual =
                null;

            detalhesMateriaModal?.hide();
        }

        materiaParaExcluir =
            null;

        await carregarMaterias();
    } catch (erro) {
        console.error(
            "Erro ao excluir matéria:",
            erro
        );

        mostrarAlerta(
            obterMensagemErro(
                erro
            ),
            "danger"
        );
    } finally {
        excluindoMateria = false;

        if (
            elementos.btnConfirmarExclusao
        ) {
            elementos.btnConfirmarExclusao.disabled =
                false;
        }
    }
}

function tratarFechamentoModalDetalhes() {
    carregandoDetalhes = false;

    materiaDetalhesAtual =
        null;

    if (
        elementos.cpfJornalista
    ) {
        elementos.cpfJornalista.value =
            "";
        elementos.cpfJornalista.disabled =
            false;
    }

    if (
        elementos.btnAlocarJornalista
    ) {
        elementos.btnAlocarJornalista.disabled =
            false;
        elementos.btnAlocarJornalista.textContent =
            "Alocar";
    }

    limparListaJornalistas();
}

function tratarFechamentoModalMateria() {
    if (
        !salvandoMateria
    ) {
        limparFormulario();
    }
}

function tratarFechamentoModalExclusao() {
    if (
        !excluindoMateria
    ) {
        materiaParaExcluir =
            null;
    }
}

async function requisicaoApi(
    url,
    opcoes = {}
) {
    const controller =
        new AbortController();

    const timeout =
        window.setTimeout(
            () => {
                controller.abort();
            },
            CONFIG.REQUEST_TIMEOUT
        );

    try {
        const resposta =
            await fetch(
                url,
                {
                    ...opcoes,
                    signal:
                        controller.signal
                }
            );

        return await processarResposta(
            resposta
        );
    } catch (erro) {
        if (
            erro?.name ===
            "AbortError"
        ) {
            const timeoutErro =
                new Error(
                    "A requisição demorou demais para responder."
                );

            timeoutErro.code =
                "REQUEST_TIMEOUT";

            throw timeoutErro;
        }

        throw erro;
    } finally {
        window.clearTimeout(
            timeout
        );
    }
}

async function processarResposta(
    resposta
) {
    const contentType =
        resposta.headers.get(
            "content-type"
        ) || "";

    let dados = null;

    if (
        contentType.includes(
            "application/json"
        )
    ) {
        try {
            dados =
                await resposta.json();
        } catch {
            dados = null;
        }
    } else {
        const texto =
            await resposta.text();

        dados =
            texto
                ? {
                    detail: texto
                }
                : null;
    }

    if (
        !resposta.ok
    ) {
        const erro =
            new Error(
                obterDetalheErro(
                    dados
                ) ||
                obterMensagemHttp(
                    resposta.status
                )
            );

        erro.status =
            resposta.status;

        erro.data =
            dados;

        throw erro;
    }

    return dados;
}

function obterMensagemHttp(
    status
) {
    switch (
        status
    ) {
        case HTTP_STATUS.BAD_REQUEST:
            return "Dados inválidos.";

        case HTTP_STATUS.NOT_FOUND:
            return "Registro não encontrado.";

        case HTTP_STATUS.CONFLICT:
            return "A operação entrou em conflito com os dados existentes.";

        case HTTP_STATUS.UNPROCESSABLE_ENTITY:
            return "Os dados enviados são inválidos.";

        case HTTP_STATUS.INTERNAL_SERVER_ERROR:
            return "Erro interno do servidor.";

        default:
            return `Erro HTTP ${status}.`;
    }
}

function obterDetalheErro(
    dados
) {
    if (!dados) {
        return null;
    }

    if (
        typeof dados ===
        "string"
    ) {
        return dados;
    }

    if (
        dados.detail !==
        undefined
    ) {
        if (
            Array.isArray(
                dados.detail
            )
        ) {
            return dados.detail
                .map(
                    item => {

                        if (
                            typeof item ===
                            "string"
                        ) {
                            return item;
                        }

                        return (
                            item?.msg ??
                            item?.message ??
                            JSON.stringify(
                                item
                            )
                        );
                    }
                )
                .join(
                    "; "
                );
        }

        if (
            typeof dados.detail ===
            "object"
        ) {
            return (
                dados.detail.message ??
                JSON.stringify(
                    dados.detail
                )
            );
        }

        return String(
            dados.detail
        );
    }

    if (
        dados.message
    ) {
        return String(
            dados.message
        );
    }

    if (
        dados.mensagem
    ) {
        return String(
            dados.mensagem
        );
    }

    if (
        dados.error
    ) {
        return String(
            dados.error
        );
    }

    return null;
}

function obterMensagemErro(
    erro
) {
    if (
        erro?.code ===
        "REQUEST_TIMEOUT"
    ) {
        return erro.message;
    }

    if (
        erro?.message
    ) {
        return erro.message;
    }

    return "Ocorreu um erro inesperado.";
}

function mostrarAlerta(
    mensagem,
    tipo = "info"
) {
    if (
        !elementos.alertContainer
    ) {
        console.warn(
            mensagem
        );

        return;
    }

    const tiposPermitidos = [
        "success",
        "danger",
        "warning",
        "info"
    ];

    const tipoSeguro =
        tiposPermitidos.includes(
            tipo
        )
            ? tipo
            : "info";

    const alerta =
        document.createElement(
            "div"
        );

    alerta.className =
        `alert alert-${tipoSeguro} alert-dismissible fade show`;

    alerta.setAttribute(
        "role",
        "alert"
    );

    const texto =
        document.createElement(
            "span"
        );

    texto.textContent =
        mensagem ??
        "";

    alerta.appendChild(
        texto
    );

    const botao =
        document.createElement(
            "button"
        );

    botao.type =
        "button";

    botao.className =
        "btn-close";

    botao.setAttribute(
        "data-bs-dismiss",
        "alert"
    );

    botao.setAttribute(
        "aria-label",
        "Fechar"
    );

    alerta.appendChild(
        botao
    );

    elementos.alertContainer.appendChild(
        alerta
    );

    window.setTimeout(
        () => {
            if (
                alerta &&
                alerta.parentNode
            ) {
                alerta.remove();
            }
        },
        CONFIG.ALERT_TIMEOUT
    );
}

function mostrarLoading(
    mostrar
) {
    if (
        !elementos.loadingIndicator
    ) {
        return;
    }

    elementos.loadingIndicator.classList.toggle(
        "d-none",
        !mostrar
    );

    if (
        mostrar
    ) {
        elementos.loadingIndicator.innerHTML = `
            <span
                class="loading-spinner"
                aria-hidden="true"
            ></span>
            Carregando...
        `;
    } else {
        elementos.loadingIndicator.innerHTML =
            "";
    }
}

function mostrarLoadingDetalhes(
    mostrar
) {
    if (
        !elementos.detalhesLoading
    ) {
        return;
    }

    elementos.detalhesLoading.classList.toggle(
        "d-none",
        !mostrar
    );

    elementos.detalhesLoading.textContent =
        mostrar
            ? "Carregando detalhes..."
            : "";
}

function atualizarEstadoFormularioAlocacao() {
    const materiaDisponivel =
        materiaDetalhesAtual?.id_materia !==
            undefined &&
        materiaDetalhesAtual?.id_materia !==
            null;

    const habilitado =
        materiaDisponivel &&
        !carregandoDetalhes &&
        !alocandoJornalista;

    if (
        elementos.cpfJornalista
    ) {
        elementos.cpfJornalista.disabled =
            !habilitado;
    }

    if (
        elementos.btnAlocarJornalista
    ) {
        elementos.btnAlocarJornalista.disabled =
            !habilitado;
    }
}

function formatarData(
    data
) {
    if (!data) {
        return "-";
    }

    const valor =
        String(
            data
        );

    const correspondencia =
        valor.match(
            /^(\d{4})-(\d{2})-(\d{2})$/
        );

    if (
        correspondencia
    ) {
        return (
            `${correspondencia[3]}/` +
            `${correspondencia[2]}/` +
            `${correspondencia[1]}`
        );
    }

    const objeto =
        new Date(
            data
        );

    if (
        Number.isNaN(
            objeto.getTime()
        )
    ) {
        return valor;
    }

    return new Intl.DateTimeFormat(
        "pt-BR"
    ).format(
        objeto
    );
}

function formatarDataParaInput(
    data
) {
    if (!data) {
        return "";
    }

    const valor =
        String(
            data
        );

    const correspondencia =
        valor.match(
            /^(\d{4})-(\d{2})-(\d{2})/
        );

    if (
        correspondencia
    ) {
        return (
            `${correspondencia[1]}-` +
            `${correspondencia[2]}-` +
            `${correspondencia[3]}`
        );
    }

    return "";
}

function normalizarCpf(
    cpf
) {
    if (
        cpf === null ||
        cpf === undefined
    ) {
        return "";
    }

    return String(
        cpf
    )
        .replace(
            /\D/g,
            ""
        )
        .slice(
            0,
            CONFIG.CPF_LENGTH
        );
}

function converterNumeroOuNull(
    valor
) {
    if (
        valor === null ||
        valor === undefined ||
        String(
            valor
        ).trim() === ""
    ) {
        return null;
    }

    const numero =
        Number(
            valor
        );

    return Number.isFinite(
        numero
    )
        ? numero
        : null;
}

function obterStatus(
    status
) {
    const valor =
        normalizarStatus(
            status
        );

    return {
        valor,
        label:
            STATUS_LABELS[
                valor
            ] ??
            "Desconhecido"
    };
}

function normalizarStatus(
    status
) {
    if (
        status === null ||
        status === undefined
    ) {
        return -1;
    }

    if (
        typeof status ===
        "number"
    ) {
        return status;
    }

    const valor =
        String(
            status
        )
            .trim()
            .toLowerCase();

    if (
        valor === "0" ||
        valor === "em andamento" ||
        valor === "em_andamento"
    ) {
        return STATUS.EM_ANDAMENTO;
    }

    if (
        valor === "1" ||
        valor === "aprovada"
    ) {
        return STATUS.APROVADA;
    }

    if (
        valor === "2" ||
        valor === "reprovada"
    ) {
        return STATUS.REPROVADA;
    }

    return -1;
}

function criarBadgeStatus(
    status
) {
    return `
        <span
            class="status-badge ${obterClasseStatus(status)}"
        >
            ${escapeHtml(
                status.label
            )}
        </span>
    `;
}

function obterClasseStatus(
    status
) {
    switch (
        status.valor
    ) {
        case STATUS.EM_ANDAMENTO:
            return "status-em-andamento";

        case STATUS.APROVADA:
            return "status-aprovada";

        case STATUS.REPROVADA:
            return "status-reprovada";

        default:
            return "status-desconhecido";
    }
}

function escapeHtml(
    valor
) {
    if (
        valor === null ||
        valor === undefined
    ) {
        return "";
    }

    return String(
        valor
    )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}