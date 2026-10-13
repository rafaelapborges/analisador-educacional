
async function carregarMensagem() {
    const mensagem = document.getElementById("mensagem");
    const status = document.getElementById("status");

    try {
        const resposta = await fetch("/api/hello");

        if (!resposta.ok) {
            throw new Error("Erro ao conectar");
        }

        const dados = await resposta.json();

        mensagem.textContent = dados.message;
        status.textContent = "Backend conectado com sucesso!";
        status.style.color = "green";

    } catch (erro) {
        mensagem.textContent = "Erro de conexão";
        status.textContent = "Não foi possível conectar ao backend.";
        status.style.color = "red";
    }
}

carregarMensagem();
