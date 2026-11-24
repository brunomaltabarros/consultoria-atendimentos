import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useAutenticacao } from "../contexto/AutenticacaoContexto";

export default function Login() {
  const { token, entrar } = useAutenticacao();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState(null);
  const [enviando, setEnviando] = useState(false);

  if (token) {
    return <Navigate to="/" replace />;
  }

  async function aoEnviar(evento) {
    evento.preventDefault();
    setErro(null);
    setEnviando(true);
    try {
      await entrar(email, senha);
    } catch (e) {
      setErro(e.message);
    } finally {
      setEnviando(false);
    }
  }

  return (
    <main className="tela-login">
      <form className="cartao" onSubmit={aoEnviar}>
        <h1>Portal do Credenciamento</h1>
        <p className="subtitulo">Entre com seu e-mail e senha</p>

        <label>
          E-mail
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>

        <label>
          Senha
          <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} required />
        </label>

        {erro && <p className="erro">{erro}</p>}

        <button type="submit" disabled={enviando}>
          {enviando ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </main>
  );
}