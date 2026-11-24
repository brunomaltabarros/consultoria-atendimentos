import { useCallback, useEffect, useState } from "react";
import { buscarUsuarioLogado, entrar as entrarNaApi } from "../api/autenticacao";
import { AutenticacaoContexto } from "./AutenticacaoContexto";

export default function ProvedorAutenticacao({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [usuario, setUsuario] = useState(null);

  const sair = useCallback(() => {
    localStorage.removeItem("token");
    setToken(null);
    setUsuario(null);
  }, []);

  useEffect(() => {
    if (!token) {
      return;
    }
    buscarUsuarioLogado()
      .then(setUsuario)
      .catch(() => setUsuario(null));
  }, [token]);

  useEffect(() => {
    window.addEventListener("sessao-expirada", sair);
    return () => window.removeEventListener("sessao-expirada", sair);
  }, [sair]);

  async function entrar(email, senha) {
    const resposta = await entrarNaApi(email, senha);
    localStorage.setItem("token", resposta.access_token);
    setToken(resposta.access_token);
  }

  return (
    <AutenticacaoContexto.Provider value={{ token, usuario, entrar, sair }}>
      {children}
    </AutenticacaoContexto.Provider>
  );
}