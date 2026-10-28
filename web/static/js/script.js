document.addEventListener("DOMContentLoaded", () => {
    const pdfInput = document.getElementById("pdf-input");
    const selectedFiles = document.getElementById("selected-files");
    const statusTitle = document.getElementById("status-title");
    const statusMessage = document.getElementById("status-message");
    const progressBar = document.getElementById("progress-bar");
    const progressLabel = document.getElementById("progress-label");
    const progressPercent = document.getElementById("progress-percent");
    const btnRevisar = document.getElementById("btn-revisar");
    const btnGerar = document.getElementById("btn-gerar");
    const btnSalvar = document.getElementById("btn-salvar-revisao");
    const tabela = document.getElementById("tabela-funcionarios");
    const reviewMessage = document.getElementById("review-message");
    const reviewCount = document.getElementById("review-count");

    let arquivosSelecionados = [];
    let loteAtual = null;
    let funcionariosAtuais = [];

    function atualizarStatus(titulo, mensagem) {
        statusTitle.textContent = titulo;
        statusMessage.textContent = mensagem;
    }
    function atualizarProgresso(valor, mensagem) {
        const progresso = Math.max(0, Math.min(100, valor));
        progressBar.style.width = `${progresso}%`;
        progressPercent.textContent = `${progresso}%`;
        progressLabel.textContent = mensagem;
    }
    function formatarTamanho(bytes) {
        return (bytes / (1024 * 1024)).toFixed(2);
    }
    async function respostaJson(resposta) {
        const dados = await resposta.json().catch(() => ({}));
        if (!resposta.ok || dados.sucesso === false) {
            throw new Error(dados.mensagem || "A operação não pôde ser concluída.");
        }
        return dados;
    }

    pdfInput.addEventListener("change", () => {
        arquivosSelecionados = Array.from(pdfInput.files);
        if (!arquivosSelecionados.length) {
            selectedFiles.textContent = "Nenhum arquivo selecionado.";
            return;
        }
        if (arquivosSelecionados.some(a => !a.name.toLowerCase().endsWith(".pdf"))) {
            selectedFiles.textContent = "Selecione apenas arquivos PDF.";
            pdfInput.value = "";
            arquivosSelecionados = [];
            return;
        }
        const tamanhoTotal = arquivosSelecionados.reduce((soma, a) => soma + a.size, 0);
        selectedFiles.textContent = `${arquivosSelecionados.length} arquivo(s) • ${formatarTamanho(tamanhoTotal)} MB`;
        atualizarStatus("Arquivos selecionados", "Os PDFs estão prontos para processamento.");
        atualizarProgresso(0, "Aguardando envio");
    });

    async function processarArquivos() {
        if (!arquivosSelecionados.length) {
            atualizarStatus("Nenhum arquivo selecionado", "Selecione pelo menos um PDF antes de continuar.");
            return;
        }
        const formulario = new FormData();
        arquivosSelecionados.forEach(a => formulario.append("arquivos", a));
        btnGerar.disabled = true;
        btnRevisar.disabled = true;
        btnSalvar.disabled = true;
        try {
            atualizarStatus("Enviando arquivos", "Enviando os PDFs para o servidor...");
            atualizarProgresso(10, "Enviando PDFs...");
            const upload = await respostaJson(await fetch("/api/upload", {method: "POST", body: formulario}));
            loteAtual = upload.lote;
            atualizarProgresso(35, "PDFs enviados");
            atualizarStatus("Processando documentos", `${upload.quantidade} PDF(s) recebidos. Executando OCR...`);
            atualizarProgresso(45, "Executando OCR...");
            const processamento = await respostaJson(await fetch("/api/processar", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({lote: loteAtual})
            }));
            atualizarProgresso(100, "Processamento concluído");
            atualizarStatus("Processamento concluído", "Agora clique em “Abrir revisão” para conferir os dados antes de gerar.");
            selectedFiles.textContent = `${upload.quantidade} PDF(s) processados.`;
            console.info("Resultado OCR:", processamento.detalhes);
            arquivosSelecionados = [];
            pdfInput.value = "";
            await carregarRevisao();
        } catch (erro) {
            console.error(erro);
            atualizarStatus("Erro no processamento", erro.message);
            atualizarProgresso(0, "Operação não concluída");
        } finally {
            btnGerar.disabled = false;
            btnRevisar.disabled = false;
        }
    }

    function criarInput(valor, campo, registro) {
        const input = document.createElement("input");
        input.type = "text";
        input.value = valor || "";
        input.dataset.campo = campo;
        input.setAttribute("aria-label", campo);
        input.addEventListener("input", () => { registro[campo] = input.value; });
        return input;
    }

    function renderizarTabela(registros) {
        tabela.replaceChildren();
        if (!registros.length) {
            const tr = document.createElement("tr");
            const td = document.createElement("td");
            td.colSpan = 6;
            td.className = "empty-row";
            td.textContent = "Nenhum funcionário encontrado neste lote.";
            tr.appendChild(td);
            tabela.appendChild(tr);
        } else {
            registros.forEach(registro => {
                const tr = document.createElement("tr");
                const origem = document.createElement("td");
                origem.className = "source-cell";
                origem.textContent = `${registro.arquivo_pdf} • pág. ${registro.pagina}`;
                tr.appendChild(origem);
                [
                    ["nome", registro.nome],
                    ["data_admissao", registro.data_admissao],
                    ["cargo", registro.cargo],
                    ["projeto", registro.projeto]
                ].forEach(([campo, valor]) => {
                    const td = document.createElement("td");
                    td.appendChild(criarInput(valor, campo, registro));
                    tr.appendChild(td);
                });
                const status = document.createElement("td");
                status.className = "status-cell";
                status.textContent = registro.status || "REVISAR";
                tr.appendChild(status);
                tabela.appendChild(tr);
            });
        }
        reviewCount.textContent = `${registros.length} registro(s)`;
        reviewMessage.textContent = registros.length
            ? "Edite os campos necessários e clique em “Salvar correções”."
            : "Não há dados para revisar neste lote.";
        btnSalvar.disabled = !registros.length;
    }

    async function carregarRevisao() {
        if (!loteAtual) {
            atualizarStatus("Nenhum lote disponível", "Processe os PDFs primeiro para abrir a revisão.");
            reviewMessage.textContent = "Processe um lote e clique em “Abrir revisão”.";
            return;
        }
        try {
            const dados = await respostaJson(await fetch(`/api/funcionarios?lote=${encodeURIComponent(loteAtual)}`));
            funcionariosAtuais = dados.funcionarios || [];
            renderizarTabela(funcionariosAtuais);
            document.getElementById("revisao").scrollIntoView({behavior: "smooth", block: "start"});
            atualizarStatus("Revisão carregada", `${funcionariosAtuais.length} registro(s) do lote atual carregados.`);
        } catch (erro) {
            atualizarStatus("Erro ao carregar revisão", erro.message);
            reviewMessage.textContent = erro.message;
        }
    }

    async function salvarRevisao() {
        if (!loteAtual || !funcionariosAtuais.length) return;
        btnSalvar.disabled = true;
        try {
            const dados = await respostaJson(await fetch("/api/funcionarios/salvar", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({lote: loteAtual, funcionarios: funcionariosAtuais})
            }));
            reviewMessage.textContent = dados.mensagem;
            atualizarStatus("Correções salvas", "Os dados revisados foram atualizados na planilha.");
            await carregarRevisao();
        } catch (erro) {
            reviewMessage.textContent = erro.message;
            atualizarStatus("Erro ao salvar", erro.message);
        } finally {
            btnSalvar.disabled = false;
        }
    }

    async function gerarDocumentos() {
        if (!loteAtual) {
            atualizarStatus("Nenhum lote disponível", "Selecione e processe os PDFs primeiro.");
            return;
        }
        btnGerar.disabled = true;
        try {
            atualizarStatus("Salvando e validando dados", "As correções serão salvas antes da geração.");
            if (funcionariosAtuais.length) {
                await respostaJson(await fetch("/api/funcionarios/salvar", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({lote: loteAtual, funcionarios: funcionariosAtuais})
                }));
            }
            atualizarProgresso(60, "Gerando documentos...");
            const resultado = await respostaJson(await fetch("/api/gerar", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({lote: loteAtual})
            }));
            atualizarProgresso(100, "Geração concluída");
            atualizarStatus("Documentos gerados", resultado.mensagem);
            reviewMessage.textContent = resultado.detalhes || resultado.mensagem;
            await carregarRevisao();
        } catch (erro) {
            atualizarStatus("Não foi possível gerar", erro.message);
            atualizarProgresso(0, "Geração não concluída");
            reviewMessage.textContent = erro.message;
        } finally {
            btnGerar.disabled = false;
        }
    }

    btnGerar.addEventListener("click", () => {
        if (arquivosSelecionados.length) processarArquivos();
        else gerarDocumentos();
    });
    btnRevisar.addEventListener("click", carregarRevisao);
    btnSalvar.addEventListener("click", salvarRevisao);

    document.querySelectorAll(".nav-item").forEach(item => {
        item.addEventListener("click", () => {
            document.querySelectorAll(".nav-item").forEach(link => link.classList.remove("active"));
            item.classList.add("active");
        });
    });
    atualizarProgresso(0, "Aguardando operação");
});
