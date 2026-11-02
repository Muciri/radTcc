import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./views/home";
import { TrabalhoDetalhes } from "./views/TrabalhoDetalhes";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/trabalhos/:id" element={<TrabalhoDetalhes />} />
        <Route path="*" element={<h1>Página não encontrada</h1>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
