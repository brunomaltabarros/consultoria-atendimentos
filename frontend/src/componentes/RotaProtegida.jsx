import { Navigate } from "react-router-dom";
import { useAutenticacao } from "../contexto/AutenticacaoContexto";

export default function RotaProtegida({ children }) {
  const { token } = useAutenticacao();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}