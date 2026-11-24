import { createContext, useContext } from "react";

export const AutenticacaoContexto = createContext(null);

export function useAutenticacao() {
  return useContext(AutenticacaoContexto);
}