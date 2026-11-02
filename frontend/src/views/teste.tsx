
import { Link } from "react-router";

function About() {
  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-6">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-xl">

        <span className="text-sm font-semibold text-blue-400">
          Página de teste
        </span>

        <h1 className="mt-3 text-3xl font-bold text-white">
          Olá, Tailwind! 👋
        </h1>

        <p className="mt-4 text-slate-400 leading-relaxed">
          Se você está vendo essa página estilizada, significa que o
          Tailwind CSS está funcionando corretamente no seu projeto.
        </p>

        <Link
          to="/"
          className="mt-8 inline-flex items-center justify-center rounded-lg bg-blue-600 px-5 py-3 font-medium text-white transition hover:bg-blue-700"
        >
          Voltar para Home
        </Link>

      </div>
    </main>
  );
}

export default About;
