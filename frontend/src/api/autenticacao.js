import { api } from "./cliente";

export function entrar(email, senha) {
  return api.criar("/auth/login", { email, senha });
}

export function buscarUsuarioLogado() {
  return api.buscar("/auth/eu");
}