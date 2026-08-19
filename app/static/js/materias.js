"use strict";

/*
 * ============================================================
 * CONFIGURAÇÃO
 * ============================================================
 */

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


/*
 * ============================================================
 * ESTADO
 * ============================================================
 */

let materiaModal = null;
let detalhesMateriaModal = null;
let excluirModal = null;

let materiaParaExcluir = null;
let materiaDetalhesAtual = null;


/*
 * ============================================================
 * ELEMENTOS DOM
 * ============================================================
 */

const elementos = {};


/*
 * ============================================================
 * INICIALIZAÇÃO
 * ============================================================
 */

document.addEventListener("DOMContentLoaded", () => {

    inicializarElementos();

    inicializarModais();

    registrarEventos();

    carregarMaterias();
});


function inicializarElementos() {

    elementos.alertContainer =
        document.getElementById("alertContainer");

    elementos.loadingIndicator =
        document.getElementById("loadingIndicator");

    elementos.materiasTableBody =
        document.getElementById("materiasTableBody");


    /*
     * ========================================================
     * FILTROS
     * ========================================================
     */

    elementos.filtroForm =
        document.getElementById("filtroForm");

    elementos.filtroSearch =
        document.getElementById("filtroSearch");

    elementos.filtroStatus =
        document.getElementById("filtroStatus");

    elementos.filtroSetor =
        document.getElementById("filtroSetor");


    /*
     * ========================================================
     * NOVA MATÉRIA
     * ========================================================
     */

    elementos.btnNovaMateria =
        document.getElementById("btnNovaMateria");


    /*
     * ========================================================
     * FORMULÁRIO
     * ========================================================
     */

    elementos.materiaForm =
        document.getElementById("materiaForm");

    elementos.materiaModal =
        document.getElementById("materiaModal");

    elementos.materiaModalLabel =
        document.getElementById("materiaModalLabel");

    elementos.btnSalvarMateria =
        document.getElementById("btnSalvarMateria");


    /*
     * ========================================================
     * CAMPOS
     * ========================================================
     */

    elementos.materiaId =
        document.getElementById("materiaId");

    elementos.titulo =
        document.getElementById("titulo");

    elementos.subtitulo =
        document.getElementById("subtitulo");

    elementos.resumo =
        document.getElementById("resumo");

    elementos.conteudo =
        document.getElementById("conteudo");

    elementos.data =
        document.getElementById("data");

    elementos.status =
        document.getElementById("status");

    elementos.idSetor =
        document.getElementById("id_setor");

    elementos.nomeJornal =
        document.getElementById("nome_jornal");

    elementos.numeroEdicao =
        document.getElementById("numero_edicao");

    elementos.cpfEditorChefe =
        document.getElementById("cpf_editor_chefe");


    /*
     * ========================================================
     * DETALHES
     * ========================================================
     */

    elementos.detalhesMateriaModal =
        document.getElementById(
            "detalhesMateriaModal"
        );

    elementos.detalhesMateriaModalLabel =
        document.getElementById(
            "detalhesMateriaModalLabel"
        );

    elementos.detalhesMateriaSubtitulo =
        document.getElementById(
            "detalhesMateriaSubtitulo"
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


    /*
     * ========================================================
     * JORNALISTAS
     * ========================================================
     */

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


    /*
     * ========================================================
     * EXCLUSÃO
     * ========================================================
     */

    elementos.excluirModal =
        document.getElementById(
            "excluirModal"
        );

    elementos.btnConfirmarExclusao =
        document.getElementById(
            "btnConfirmarExclusao"
        );
}


/*
 * ============================================================
 * MODAIS
 * ============================================================
 */

function inicializarModais() {

    if (
        elementos.materiaModal &&
        window.bootstrap
    ) {

        materiaModal =
            new bootstrap.Modal(
                elementos.materiaModal
            );
    }


    if (
        elementos.detalhesMateriaModal &&
        window.bootstrap
    ) {

        detalhesMateriaModal =
            new bootstrap.Modal(
                elementos.detalhesMateriaModal
            );
    }


    if (
        elementos.excluirModal &&
        window.bootstrap
    ) {

        excluirModal =
            new bootstrap.Modal(
                elementos.excluirModal
            );
    }
}


/*
 * ============================================================
 * EVENTOS
 * ============================================================
 */

function registrarEventos() {

    elementos.btnNovaMateria?.addEventListener(
        "click",
        abrirFormularioNovaMateria
    );


    elementos.filtroForm?.addEventListener(
        "submit",
        evento => {

            evento.preventDefault();

            carregarMaterias();
        }
    );


    elementos.materiaForm?.addEventListener(
        "submit",
        salvarMateria
    );


    elementos.btnConfirmarExclusao?.addEventListener(
        "click",
        excluirMateria
    );


    /*
     * Formulário de alocação.
     *
     * O tratamento completo de alocação
     * será implementado na próxima etapa.
     */

    elementos.alocarJornalistaForm?.addEventListener(
        "submit",
        evento => {

            evento.preventDefault();

            alocarJornalista();
        }
    );
}


/*
 * ============================================================
 * LISTAGEM
 * ============================================================
 */

async function carregarMaterias() {

    mostrarLoading(true);

    try {

        const parametros =
            construirParametrosFiltro();


        const url =
            construirUrlApi(
                API_MATERIAS,
                parametros
            );


        const resposta =
            await fetch(
                url,
                {
                    method: "GET",

                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );


        const dados =
            await processarResposta(
                resposta
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
            obterMensagemErro(erro),
            "danger"
        );


        renderizarMaterias([]);

    } finally {

        mostrarLoading(false);
    }
}


/*
 * ============================================================
 * FILTROS
 * ============================================================
 */

function construirParametrosFiltro() {

    const parametros =
        new URLSearchParams();


    const search =
        elementos.filtroSearch?.value.trim();


    const status =
        elementos.filtroStatus?.value;


    const setorId =
        elementos.filtroSetor?.value.trim();


    if (search) {

        parametros.append(
            "search",
            search
        );
    }


    if (
        status !== undefined &&
        status !== ""
    ) {

        parametros.append(
            "status",
            status
        );
    }


    if (setorId) {

        parametros.append(
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

    const queryString =
        parametros.toString();


    if (!queryString) {

        return endpoint;
    }


    return `${endpoint}?${queryString}`;
}


/*
 * ============================================================
 * RENDERIZAÇÃO
 * ============================================================
 */

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


    materias.forEach(
        materia => {

            const linha =
                criarLinhaMateria(
                    materia
                );


            elementos.materiasTableBody.appendChild(
                linha
            );
        }
    );
}


function criarLinhaMateria(
    materia
) {

    const linha =
        document.createElement("tr");


    const id =
        materia.id_materia ?? "";


    const titulo =
        materia.titulo ??
        "Sem título";


    const nomeJornal =
        materia.nome_jornal ??
        "-";


    const numeroEdicao =
        materia.numero_edicao ??
        "-";


    const data =
        formatarData(
            materia.data
        );


    const status =
        obterStatus(
            materia.status
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
                title="Visualizar detalhes da matéria"
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


    /*
     * ========================================================
     * BOTÃO DETALHES
     * ========================================================
     */

    const botaoDetalhes =
        linha.querySelector(
            '[data-action="detalhes"]'
        );


    botaoDetalhes?.addEventListener(
        "click",
        () => abrirDetalhesMateria(
            materia
        )
    );


    /*
     * ========================================================
     * BOTÃO EDITAR
     * ========================================================
     */

    const botaoEditar =
        linha.querySelector(
            '[data-action="editar"]'
        );


    botaoEditar?.addEventListener(
        "click",
        () => abrirFormularioEdicao(
            materia
        )
    );


    /*
     * ========================================================
     * BOTÃO EXCLUIR
     * ========================================================
     */

    const botaoExcluir =
        linha.querySelector(
            '[data-action="excluir"]'
        );


    botaoExcluir?.addEventListener(
        "click",
        () => abrirConfirmacaoExclusao(
            materia
        )
    );


    return linha;
}


/*
 * ============================================================
 * DETALHES DA MATÉRIA
 * ============================================================
 */

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


    materiaDetalhesAtual =
        materia;


    limparDetalhesMateria();


    detalhesMateriaModal?.show();


    mostrarLoadingDetalhes(true);


    try {

        const resposta =
            await fetch(
                `${API_MATERIAS}${encodeURIComponent(id)}`,
                {
                    method: "GET",

                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );


        const dados =
            await processarResposta(
                resposta
            );


        materiaDetalhesAtual =
            dados;


        preencherDetalhesMateria(
            dados
        );


        await carregarJornalistas(
            id
        );

    } catch (erro) {

        console.error(
            "Erro ao carregar detalhes da matéria:",
            erro
        );


        mostrarAlerta(
            obterMensagemErro(erro),
            "danger"
        );

    } finally {

        mostrarLoadingDetalhes(false);
    }
}


/*
 * ============================================================
 * PREENCHER DETALHES
 * ============================================================
 */

function preencherDetalhesMateria(
    materia
) {

    if (!materia) {
        return;
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

        const status =
            obterStatus(
                materia.status
            );


        elementos.detalhesStatus.innerHTML =
            criarBadgeStatus(
                status
            );
    }
}


/*
 * ============================================================
 * LIMPAR DETALHES
 * ============================================================
 */

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


    limparListaJornalistas();
}


/*
 * ============================================================
 * LOADING DOS DETALHES
 * ============================================================
 */

function mostrarLoadingDetalhes(
    mostrar
) {

    if (
        !elementos.detalhesLoading
    ) {
        return;
    }


    if (mostrar) {

        elementos.detalhesLoading.classList.remove(
            "d-none"
        );


        elementos.detalhesLoading.textContent =
            "Carregando detalhes...";

    } else {

        elementos.detalhesLoading.classList.add(
            "d-none"
        );


        elementos.detalhesLoading.textContent =
            "";
    }
}


/*
 * ============================================================
 * JORNALISTAS DA MATÉRIA
 * ============================================================
 */

async function carregarJornalistas(
    materiaId
) {

    if (
        !elementos.jornalistasTableBody
    ) {
        return;
    }


    limparListaJornalistas();


    try {

        const resposta =
            await fetch(
                `${API_MATERIAS}${encodeURIComponent(materiaId)}/jornalistas`,
                {
                    method: "GET",

                    headers: {
                        "Accept":
                            "application/json"
                    }
                }
            );


        const dados =
            await processarResposta(
                resposta
            );


        renderizarJornalistas(
            dados
        );

    } catch (erro) {

        console.error(
            "Erro ao carregar jornalistas:",
            erro
        );


        elementos.jornalistasTableBody.innerHTML = `
            <tr>

                <td
                    colspan="2"
                    class="text-center text-danger py-4"
                >
                    Não foi possível carregar os jornalistas.
                </td>

            </tr>
        `;
    }
}


/*
 * ============================================================
 * RENDERIZAÇÃO DOS JORNALISTAS
 * ============================================================
 */

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

        return;
    }


    jornalistas.forEach(
        jornalista => {

            const linha =
                criarLinhaJornalista(
                    jornalista
                );


            elementos.jornalistasTableBody.appendChild(
                linha
            );
        }
    );
}


function criarLinhaJornalista(
    jornalista
) {

    const linha =
        document.createElement("tr");


    const cpf =
        typeof jornalista === "string"
            ? jornalista
            : jornalista?.cpf_jornalista ?? "-";


    linha.innerHTML = `

        <td>
            ${escapeHtml(cpf)}
        </td>


        <td class="text-end">

            <button
                type="button"
                class="btn btn-sm btn-outline-danger"
                data-action="desalocar"
            >
                Desalocar
            </button>

        </td>
    `;


    /*
     * O fluxo efetivo de desalocação será
     * conectado na próxima etapa.
     */

    const botaoDesalocar =
        linha.querySelector(
            '[data-action="desalocar"]'
        );


    botaoDesalocar?.addEventListener(
        "click",
        () => desalocarJornalista(
            cpf
        )
    );


    return linha;
}


/*
 * ============================================================
 * LIMPAR LISTA DE JORNALISTAS
 * ============================================================
 */

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


/*
 * ============================================================
 * ALOCAÇÃO
 * ============================================================
 */

async function alocarJornalista() {

    /*
     * Implementação completa da chamada POST
     * será feita na próxima parte.
     */

    if (
        !materiaDetalhesAtual ||
        materiaDetalhesAtual.id_materia === undefined
    ) {

        mostrarAlerta(
            "Nenhuma matéria está aberta.",
            "warning"
        );

        return;
    }


    const cpf =
        elementos.cpfJornalista?.value.trim();


    if (!cpf) {

        mostrarAlerta(
            "Informe o CPF do jornalista.",
            "warning"
        );

        elementos.cpfJornalista?.focus();

        return;
    }


    mostrarAlerta(
        "O fluxo de alocação será conectado na próxima etapa.",
        "info"
    );
}


/*
 * ============================================================
 * DESALOCAÇÃO
 * ============================================================
 */

async function desalocarJornalista(
    cpf
) {

    /*
     * Implementação completa da chamada DELETE
     * será feita na próxima parte.
     */

    if (
        !materiaDetalhesAtual ||
        materiaDetalhesAtual.id_materia === undefined
    ) {

        mostrarAlerta(
            "Nenhuma matéria está aberta.",
            "warning"
        );

        return;
    }


    mostrarAlerta(
        `Desalocação do jornalista ${cpf} será conectada na próxima etapa.`,
        "info"
    );
}


/*
 * ============================================================
 * STATUS
 * ============================================================
 */

function obterStatus(status) {

    const valor =
        normalizarStatus(
            status
        );


    return {

        valor,

        label:
            STATUS_LABELS[valor] ??
            "Desconhecido"
    };
}


function criarBadgeStatus(
    status
) {

    const classe =
        obterClasseStatus(
            status
        );


    return `
        <span
            class="status-badge ${classe}"
        >
            ${escapeHtml(status.label)}
        </span>
    `;
}


function obterClasseStatus(
    status
) {

    switch (status.valor) {

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
        typeof status === "number"
    ) {

        return status;
    }


    const valor =
        String(status)
            .trim()
            .toLowerCase();


    if (valor === "0") {

        return STATUS.EM_ANDAMENTO;
    }


    if (valor === "1") {

        return STATUS.APROVADA;
    }


    if (valor === "2") {

        return STATUS.REPROVADA;
    }


    if (
        valor === "em andamento" ||
        valor === "em_andamento"
    ) {

        return STATUS.EM_ANDAMENTO;
    }


    if (
        valor === "aprovada"
    ) {

        return STATUS.APROVADA;
    }


    if (
        valor === "reprovada"
    ) {

        return STATUS.REPROVADA;
    }


    return -1;
}


/*
 * ============================================================
 * NOVA MATÉRIA
 * ============================================================
 */

function abrirFormularioNovaMateria() {

    limparFormulario();


    elementos.materiaModalLabel.textContent =
        "Nova matéria";


    elementos.btnSalvarMateria.textContent =
        "Salvar";


    materiaModal?.show();
}


/*
 * ============================================================
 * EDIÇÃO
 * ============================================================
 */

function abrirFormularioEdicao(
    materia
) {

    limparFormulario();


    elementos.materiaModalLabel.textContent =
        "Editar matéria";


    elementos.btnSalvarMateria.textContent =
        "Atualizar";


    elementos.materiaId.value =
        materia.id_materia ?? "";


    elementos.titulo.value =
        materia.titulo ?? "";


    elementos.subtitulo.value =
        materia.subtitulo ?? "";


    elementos.resumo.value =
        materia.resumo ?? "";


    elementos.conteudo.value =
        materia.conteudo ?? "";


    elementos.data.value =
        formatarDataParaInput(
            materia.data
        );


    elementos.status.value =
        String(
            normalizarStatus(
                materia.status
            )
        );


    elementos.idSetor.value =
        materia.id_setor ?? "";


    elementos.nomeJornal.value =
        materia.nome_jornal ?? "";


    elementos.numeroEdicao.value =
        materia.numero_edicao ?? "";


    elementos.cpfEditorChefe.value =
        materia.cpf_editor_chefe ?? "";


    materiaModal?.show();
}


/*
 * ============================================================
 * FORMULÁRIO
 * ============================================================
 */

function limparFormulario() {

    elementos.materiaForm?.reset();


    elementos.materiaId.value =
        "";


    elementos.status.value =
        String(
            STATUS.EM_ANDAMENTO
        );
}


function obterDadosFormulario() {

    const dados = {

        titulo:
            elementos.titulo.value.trim(),


        subtitulo:
            elementos.subtitulo.value.trim(),


        resumo:
            elementos.resumo.value.trim(),


        conteudo:
            elementos.conteudo.value.trim(),


        data:
            elementos.data.value,


        status:
            Number(
                elementos.status.value
            ),


        nome_jornal:
            elementos.nomeJornal.value.trim(),


        numero_edicao:
            converterNumeroOuNull(
                elementos.numeroEdicao.value
            ),


        id_setor:
            converterNumeroOuNull(
                elementos.idSetor.value
            ),


        cpf_editor_chefe:
            elementos.cpfEditorChefe?.value.trim() ||
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
        resultado.numero_edicao === null
    ) {

        delete resultado.numero_edicao;
    }


    if (
        resultado.id_setor === null
    ) {

        delete resultado.id_setor;
    }


    if (
        resultado.cpf_editor_chefe === null ||
        resultado.cpf_editor_chefe === ""
    ) {

        delete resultado.cpf_editor_chefe;
    }


    return resultado;
}


/*
 * ============================================================
 * VALIDAÇÃO
 * ============================================================
 */

function validarFormulario(
    dados
) {

    if (!dados.titulo) {

        mostrarAlerta(
            "O título da matéria é obrigatório.",
            "warning"
        );


        elementos.titulo.focus();

        return false;
    }


    if (!dados.conteudo) {

        mostrarAlerta(
            "O conteúdo da matéria é obrigatório.",
            "warning"
        );


        elementos.conteudo.focus();

        return false;
    }


    if (!dados.data) {

        mostrarAlerta(
            "A data da matéria é obrigatória.",
            "warning"
        );


        elementos.data.focus();

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


        elementos.status.focus();

        return false;
    }


    return true;
}


/*
 * ============================================================
 * POST / PUT
 * ============================================================
 */

async function salvarMateria(
    evento
) {

    evento.preventDefault();


    const id =
        elementos.materiaId.value.trim();


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

        alterarEstadoBotaoSalvar(
            false
        );
    }
}


/*
 * ============================================================
 * BOTÃO SALVAR
 * ============================================================
 */

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


    if (carregando) {

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
        elementos.materiaId.value.trim() !== "";


    elementos.btnSalvarMateria.textContent =
        editando
            ? "Atualizar"
            : "Salvar";
}


/*
 * ============================================================
 * EXCLUSÃO
 * ============================================================
 */

function abrirConfirmacaoExclusao(
    materia
) {

    materiaParaExcluir =
        materia;


    excluirModal?.show();
}


async function excluirMateria() {

    if (
        !materiaParaExcluir ||
        materiaParaExcluir.id_materia === undefined ||
        materiaParaExcluir.id_materia === null
    ) {

        mostrarAlerta(
            "Não foi possível identificar a matéria.",
            "danger"
        );

        return;
    }


    const id =
        materiaParaExcluir.id_materia;


    elementos.btnConfirmarExclusao.disabled =
        true;


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

        elementos.btnConfirmarExclusao.disabled =
            false;
    }
}


/*
 * ============================================================
 * RESPOSTA HTTP
 * ============================================================
 */

async function processarResposta(
    resposta
) {

    let dados = null;


    const contentType =
        resposta.headers.get(
            "content-type"
        );


    if (
        contentType &&
        contentType.includes(
            "application/json"
        )
    ) {

        dados =
            await resposta.json();

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


    if (!resposta.ok) {

        const erro =
            new Error(
                obterDetalheErro(
                    dados
                ) ??
                `Erro HTTP ${resposta.status}`
            );


        erro.status =
            resposta.status;


        erro.data =
            dados;


        throw erro;
    }


    return dados;
}


function obterDetalheErro(
    dados
) {

    if (!dados) {

        return null;
    }


    if (
        typeof dados === "string"
    ) {

        return dados;
    }


    if (dados.detail) {

        if (
            Array.isArray(
                dados.detail
            )
        ) {

            return dados.detail
                .map(
                    item => {

                        if (
                            typeof item === "string"
                        ) {

                            return item;
                        }


                        return (
                            item.msg ??
                            JSON.stringify(
                                item
                            )
                        );
                    }
                )
                .join("; ");
        }


        return String(
            dados.detail
        );
    }


    if (dados.message) {

        return String(
            dados.message
        );
    }


    if (dados.error) {

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
        erro &&
        erro.message
    ) {

        return erro.message;
    }


    return "Ocorreu um erro inesperado.";
}


/*
 * ============================================================
 * LISTA DA API
 * ============================================================
 */

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


    if (
        Array.isArray(
            dados.items
        )
    ) {

        return dados.items;
    }


    if (
        Array.isArray(
            dados.results
        )
    ) {

        return dados.results;
    }


    if (
        Array.isArray(
            dados.data
        )
    ) {

        return dados.data;
    }


    if (
        Array.isArray(
            dados.materias
        )
    ) {

        return dados.materias;
    }


    return [];
}


/*
 * ============================================================
 * ALERTAS
 * ============================================================
 */

function mostrarAlerta(
    mensagem,
    tipo = "info"
) {

    if (
        !elementos.alertContainer
    ) {

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


    alerta.innerHTML = `
        ${escapeHtml(mensagem)}

        <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Fechar"
        ></button>
    `;


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
        5000
    );
}


/*
 * ============================================================
 * LOADING
 * ============================================================
 */

function mostrarLoading(
    mostrar
) {

    if (
        !elementos.loadingIndicator
    ) {

        return;
    }


    if (mostrar) {

        elementos.loadingIndicator.classList.remove(
            "d-none"
        );


        elementos.loadingIndicator.innerHTML = `
            <span
                class="loading-spinner"
                aria-hidden="true"
            ></span>

            Carregando...
        `;

    } else {

        elementos.loadingIndicator.classList.add(
            "d-none"
        );


        elementos.loadingIndicator.innerHTML =
            "";
    }
}


/*
 * ============================================================
 * DATAS
 * ============================================================
 */

function formatarData(
    data
) {

    if (!data) {

        return "-";
    }


    const valor =
        String(data);


    const correspondencia =
        valor.match(
            /^(\d{4})-(\d{2})-(\d{2})$/
        );


    if (correspondencia) {

        return (
            `${correspondencia[3]}/` +
            `${correspondencia[2]}/` +
            `${correspondencia[1]}`
        );
    }


    const dataObjeto =
        new Date(data);


    if (
        Number.isNaN(
            dataObjeto.getTime()
        )
    ) {

        return valor;
    }


    return new Intl.DateTimeFormat(
        "pt-BR"
    ).format(
        dataObjeto
    );
}


function formatarDataParaInput(
    data
) {

    if (!data) {

        return "";
    }


    const valor =
        String(data);


    const correspondencia =
        valor.match(
            /^(\d{4})-(\d{2})-(\d{2})/
        );


    if (correspondencia) {

        return (
            `${correspondencia[1]}-` +
            `${correspondencia[2]}-` +
            `${correspondencia[3]}`
        );
    }


    return "";
}


/*
 * ============================================================
 * UTILITÁRIOS
 * ============================================================
 */

function converterNumeroOuNull(
    valor
) {

    if (
        valor === null ||
        valor === undefined ||
        String(valor).trim() === ""
    ) {

        return null;
    }


    const numero =
        Number(valor);


    return Number.isFinite(
        numero
    )
        ? numero
        : null;
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


    return String(valor)

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