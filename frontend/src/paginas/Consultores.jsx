import { useEffect, useState } from "react";
import {
  atualizarConsultor,
  criarConsultor,
  listarConsultores,
  removerConsultor,
} from "../api/consultores";

const FORMULARIO_VAZIO = { nome: "", cpf: "", email: "", telefone: "", bio: "" };

export default function Consultores() {
  const [consultores, setConsultores] = useState([]);
  const [formulario, setFormulario] = useState(FORMULARIO_VAZIO);
  const [editandoId, setEditandoId] = useState(null);
  const [erro, setErro] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    listarConsultores()
      .then(setConsultores)
      .catch((e) => setErro(e.message))
      .finally(() => setCarregando(false));
  }, []);

  function alterarCampo(evento) {
    const { name, value } = evento.target;
    setFormulario({ ...formulario, [name]: value });
  }

  function iniciarEdicao(consultor) {
    setEditandoId(consultor.id);
    setFormulario({
      nome: consultor.nome,
      cpf: consultor.cpf,
      email: consultor.email,
      telefone: consultor.telefone,
      bio: consultor.bio ?? "",
    });
    setErro(null);
  }

  function cancelarEdicao() {
    setEditandoId(null);
    setFormulario(FORMULARIO_VAZIO);
    setErro(null);
  }

  async function salvar(evento) {
    evento.preventDefault();
    setErro(null);
    const dados = { ...formulario, bio: formulario.bio || null };
    try {
      if (editandoId) {
        const atualizado = await atualizarConsultor(editandoId, dados);
        setConsultores(consultores.map((c) => (c.id === atualizado.id ? atualizado : c)));
      } else {
        const novo = await criarConsultor(dados);
        setConsultores([...consultores, novo]);
      }
      cancelarEdicao();
    } catch (e) {
      setErro(e.message);
    }
  }

  async function excluir(consultor) {
    if (!window.confirm(`Excluir o consultor ${consultor.nome}?`)) {
      return;
    }
    setErro(null);
    try {
      await removerConsultor(consultor.id);
      setConsultores(consultores.filter((c) => c.id !== consultor.id));
      if (editandoId === consultor.id) {
        cancelarEdicao();
      }
    } catch (e) {
      setErro(e.message);
    }
  }

  return (
    <section>
      <h2>Consultores</h2>

      <form className="formulario" onSubmit={salvar}>
        <label>
          Nome
          <input name="nome" value={formulario.nome} onChange={alterarCampo} required />
        </label>
        <label>
          CPF
          <input name="cpf" value={formulario.cpf} onChange={alterarCampo} required />
        </label>
        <label>
          E-mail
          <input name="email" type="email" value={formulario.email} onChange={alterarCampo} required />
        </label>
        <label>
          Telefone
          <input name="telefone" value={formulario.telefone} onChange={alterarCampo} required />
        </label>
        <label className="largo">
          Bio
          <textarea name="bio" value={formulario.bio} onChange={alterarCampo} rows={2} />
        </label>
        <div className="acoes">
          <button type="submit">{editandoId ? "Salvar alterações" : "Cadastrar consultor"}</button>
          {editandoId && (
            <button type="button" className="secundario" onClick={cancelarEdicao}>
              Cancelar
            </button>
          )}
        </div>
      </form>

      {erro && <p className="erro">{erro}</p>}

      {carregando ? (
        <p>Carregando...</p>
      ) : consultores.length === 0 ? (
        <p>Nenhum consultor cadastrado.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Nome</th>
              <th>E-mail</th>
              <th>Telefone</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {consultores.map((consultor) => (
              <tr key={consultor.id}>
                <td>{consultor.nome}</td>
                <td>{consultor.email}</td>
                <td>{consultor.telefone}</td>
                <td>
                  <div className="botoes">
                    <button className="secundario" onClick={() => iniciarEdicao(consultor)}>
                      Editar
                    </button>
                    <button className="perigo" onClick={() => excluir(consultor)}>
                      Excluir
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}