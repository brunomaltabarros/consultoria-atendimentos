import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import RotaProtegida from "./componentes/RotaProtegida";
import ProvedorAutenticacao from "./contexto/ProvedorAutenticacao";
import Inicio from "./paginas/Inicio";
import Login from "./paginas/Login";

function App() {
  return (
    <ProvedorAutenticacao>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <RotaProtegida>
                <Inicio />
              </RotaProtegida>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ProvedorAutenticacao>
  );
}

export default App;