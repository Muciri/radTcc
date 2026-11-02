
import { BrowserRouter, Routes, Route } from "react-router";

import Home from "./views/home";
import About from "./views/teste";
import TesteTrabalhos from "./views/TesteTrabalhos";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="teste" element={<TesteTrabalhos />} />
        <Route path="*" element={<h1>Página não encontrada</h1>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
