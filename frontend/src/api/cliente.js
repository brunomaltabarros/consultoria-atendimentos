const URL_BASE = import.meta.env.VITE_API_URL;

export class ErroDaApi extends Error {
  constructor(mensagem, status) {
    super(mensagem);
    this.name = "ErroDaApi";
    this.status = status;
  }
}

function extrairMensagem(dados, status) {
  if (dados && typeof dados.erro === "string") {
    return dados.erro;
  }
  if (dados && Array.isArray(dados.detail)) {
    return dados.detail
      .map((item) => `${item.loc?.slice(1).join(".") ?? "campo"}: ${item.msg}`)
      .join("; ");
  }
  if (dados && typeof dados.detail === "string") {
    return dados.detail;
  }
  return `Erro ${status} na requisição.`;
}

async function requisitar(caminho, { metodo = "GET", corpo } = {}) {
  const cabecalhos = {};

  if (corpo !== undefined) {
    cabecalhos["Content-Type"] = "application/json";
  }

  const token = localStorage.getItem("token");
  if (token) {
    cabecalhos["Authorization"] = `Bearer ${token}`;
  }

  const resposta = await fetch(`${URL_BASE}${caminho}`, {
    method: metodo,
    headers: cabecalhos,
    body: corpo === undefined ? undefined : JSON.stringify(corpo),
  });

  if (resposta.status === 204) {
    return null;
  }

  const texto = await resposta.text();
  const dados = texto ? JSON.parse(texto) : null;

  if (!resposta.ok) {
    throw new ErroDaApi(extrairMensagem(dados, resposta.status), resposta.status);
  }

  return dados;
}

export const api = {
  buscar: (caminho) => requisitar(caminho),
  criar: (caminho, corpo) => requisitar(caminho, { metodo: "POST", corpo }),
  atualizar: (caminho, corpo) => requisitar(caminho, { metodo: "PUT", corpo }),
  remover: (caminho) => requisitar(caminho, { metodo: "DELETE" }),
};