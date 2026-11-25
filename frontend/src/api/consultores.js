import { api } from "./cliente";

export function listarConsultores() {
  return api.buscar("/consultores");
}

export function criarConsultor(dados) {
  return api.criar("/consultores", dados);
}

export function atualizarConsultor(id, dados) {
  return api.atualizar(`/consultores/${id}`, dados);
}

export function removerConsultor(id) {
  return api.remover(`/consultores/${id}`);
}