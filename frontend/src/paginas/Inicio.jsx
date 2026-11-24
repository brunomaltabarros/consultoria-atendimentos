import { useAutenticacao } from "../contexto/AutenticacaoContexto";

export default function Inicio() {
  const { usuario, sair } = useAutenticacao();

  return (
    <main className="pagina">
      <header className="topo">
        <h1>Portal do Credenciamento</h1>
        <div className="usuario">
          <span>Olá, {usuario?.nome ?? "..."}</span>
          <button className="secundario" onClick={sair}>Sair</button>
        </div>
      </header>
      <p>Login funcionando. A tela de consultores entra aqui na próxima etapa.</p>
    </main>
  );
}