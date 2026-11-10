import { useEffect, useState } from "react";
import { api } from "./api/cliente";

function App() {
  const [consultores, setConsultores] = useState([]);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    api
      .buscar("/consultores")
      .then(setConsultores)
      .catch((e) => setErro(e.message));
  }, []);

  return (
    <div>
      <h1>Teste de conexão com a API</h1>
      {erro && <p style={{ color: "crimson" }}>Erro: {erro}</p>}
      <p>{consultores.length} consultor(es) recebidos</p>
      <ul>
        {consultores.map((c) => (
          <li key={c.id}>
            {c.nome} — {c.email}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;