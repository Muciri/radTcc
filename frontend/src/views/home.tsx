// import { useEffect, useState } from "react";
// import { Link } from "react-router-dom";
// import { TrabalhoService } from "../services/TrabalhoService";
// import type { Trabalho } from "../types/Trabalho";

// export default function Home() {
//     const [trabalhos, setTrabalhos] = useState<Trabalho[]>([]);
//     const [busca, setBusca] = useState("");
//     const [ano, setAno] = useState("");
//     const [pagina, setPagina] = useState(1);
//     const [total, setTotal] = useState(0);
//     const [temAnterior, setTemAnterior] = useState(false);
//     const [temProxima, setTemProxima] = useState(false);
//     const [loading, setLoading] = useState(true);
//     const [erro, setErro] = useState(false);

//     async function carregar(page = 1, search = busca, anoFiltro = ano) {
//         setLoading(true);
//         setErro(false);

//         try {
//             const response = await TrabalhoService.getAll({
//                 search: search || undefined,
//                 ano: anoFiltro ? Number(anoFiltro) : undefined,
//                 ordering: "-ano",
//                 page,
//                 page_size: 9,
//             });

//             setTrabalhos(response.results);
//             setTotal(response.count);
//             setTemAnterior(!!response.previous);
//             setTemProxima(!!response.next);
//             setPagina(page);
//         } catch {
//             setErro(true);
//             setTrabalhos([]);
//         } finally {
//             setLoading(false);
//         }
//     }

//     useEffect(() => {
//         void carregar();
//     }, []);

//     function pesquisar(e: React.FormEvent) {
//         e.preventDefault();
//         void carregar(1);
//     }

//     return (
//         <main className="min-h-screen bg-gray-50">
//             <header className="border-b bg-white">
//                 <div className="mx-auto max-w-6xl px-6 py-5">
//                     <h1 className="text-xl font-bold text-green-800">
//                         Repositório Acadêmico IFPB
//                     </h1>
//                     <p className="text-sm text-gray-500">
//                         Trabalhos de conclusão de curso
//                     </p>
//                 </div>
//             </header>

//             <div className="mx-auto max-w-6xl px-6 py-8">
//                 {/* Busca e filtro */}
//                 <form
//                     onSubmit={pesquisar}
//                     className="mb-8 flex flex-col gap-3 sm:flex-row"
//                 >
//                     <input
//                         value={busca}
//                         onChange={(e) => setBusca(e.target.value)}
//                         placeholder="Buscar trabalhos por título, autores, resumo, orientador..."
//                         className="flex-1 rounded-lg border bg-white px-4 py-3 text-sm outline-none focus:border-green-600"
//                     />

//                     <select
//                         value={ano}
//                         onChange={(e) => setAno(e.target.value)}
//                         className="rounded-lg border bg-white px-4 py-3 text-sm outline-none focus:border-green-600"
//                     >
//                         <option value="">Todos os anos</option>
//                         {Array.from(
//                             { length: 15 },
//                             (_, i) => new Date().getFullYear() - i
//                         ).map((a) => (
//                             <option key={a} value={a}>{a}</option>
//                         ))}
//                     </select>

//                     <button
//                         type="submit"
//                         className="rounded-lg bg-green-700 px-6 py-3 text-sm font-semibold text-white hover:bg-green-800"
//                     >
//                         Buscar
//                     </button>
//                 </form>

//                 {/* Resultados */}
//                 <div className="mb-5 flex items-center justify-between">
//                     <h2 className="text-lg font-semibold text-gray-800">
//                         Trabalhos publicados
//                     </h2>
//                     <span className="text-sm text-gray-500">
//                         {total} resultado(s)
//                     </span>
//                 </div>

//                 {loading ? (
//                     <p className="py-12 text-center text-gray-500">
//                         Carregando trabalhos...
//                     </p>
//                 ) : erro ? (
//                     <div className="py-12 text-center">
//                         <p className="text-gray-700">
//                             Não foi possível carregar os trabalhos.
//                         </p>
//                         <button
//                             onClick={() => void carregar()}
//                             className="mt-3 text-sm font-semibold text-green-700 hover:underline"
//                         >
//                             Tentar novamente
//                         </button>
//                     </div>
//                 ) : trabalhos.length === 0 ? (
//                     <div className="py-12 text-center">
//                         <p className="font-medium text-gray-700">
//                             Nenhum trabalho encontrado.
//                         </p>
//                         <p className="mt-1 text-sm text-gray-500">
//                             Tente alterar os termos da busca ou os filtros.
//                         </p>
//                     </div>
//                 ) : (
//                     <>
//                         <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
//                             {trabalhos.map((trabalho) => (
//                                 <Link
//                                     key={trabalho.id}
//                                     to={`/trabalhos/${trabalho.id}`}
//                                     className="rounded-lg border bg-white p-5 transition hover:border-green-500 hover:shadow-sm"
//                                 >
//                                     <span className="text-xs font-semibold text-green-700">
//                                         {trabalho.curso} · {trabalho.ano}
//                                     </span>

//                                     <h3 className="mt-3 font-semibold text-gray-900">
//                                         {trabalho.titulo}
//                                     </h3>

//                                     <p className="mt-3 text-sm text-gray-500">
//                                         Orientador: {trabalho.orientador}
//                                     </p>

//                                     <p className="mt-1 text-sm text-gray-500">
//                                         Autor(es): {trabalho.autores.join(", ")}
//                                     </p>

//                                     <p className="mt-4 text-sm font-medium text-green-700">
//                                         Ver detalhes →
//                                     </p>
//                                 </Link>
//                             ))}
//                         </div>

//                         {/* Paginação */}
//                         <div className="mt-8 flex items-center justify-between">
//                             <button
//                                 disabled={!temAnterior}
//                                 onClick={() => void carregar(pagina - 1)}
//                                 className="rounded-lg border bg-white px-4 py-2 text-sm disabled:opacity-40"
//                             >
//                                 Anterior
//                             </button>

//                             <span className="text-sm text-gray-500">
//                                 Página {pagina}
//                             </span>

//                             <button
//                                 disabled={!temProxima}
//                                 onClick={() => void carregar(pagina + 1)}
//                                 className="rounded-lg border bg-white px-4 py-2 text-sm disabled:opacity-40"
//                             >
//                                 Próxima
//                             </button>
//                         </div>
//                     </>
//                 )}
//             </div>
//         </main>
//     );
// }




import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { TrabalhoService } from "../services/TrabalhoService";
import type { Trabalho } from "../types/Trabalho";

export default function Home() {
    const [trabalhos, setTrabalhos] = useState<Trabalho[]>([]);
    const [busca, setBusca] = useState("");
    const [ano, setAno] = useState("");
    const [pagina, setPagina] = useState(1);
    const [total, setTotal] = useState(0);
    const [temAnterior, setTemAnterior] = useState(false);
    const [temProxima, setTemProxima] = useState(false);
    const [loading, setLoading] = useState(true);
    const [erro, setErro] = useState(false);
    const [curso, setCurso] = useState("");
    const [palavraChave, setPalavraChave] = useState("");

    async function carregar(
        page = 1,
        search = busca,
        anoFiltro = ano,
        cursoFiltro = curso,
        palavraFiltro = palavraChave
    ) {
        setLoading(true);
        setErro(false);

        try {
            const response = await TrabalhoService.getAll({
                search: search || undefined,
                ano: anoFiltro ? Number(anoFiltro) : undefined,
                curso: cursoFiltro || undefined,
                palavra_chave: palavraFiltro || undefined,
                ordering: "-ano",
                page,
                page_size: 9,
            });

            setTrabalhos(response.results);
            setTotal(response.count);
            setTemAnterior(!!response.previous);
            setTemProxima(!!response.next);
            setPagina(page);
        } catch {
            setErro(true);
            setTrabalhos([]);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        void carregar();
    }, []);

    function pesquisar(e: React.FormEvent) {
        e.preventDefault();
        void carregar(1);
    }

    return (
        <main className="min-h-screen bg-gray-50">
            <header className="border-b bg-white">
                <div className="mx-auto max-w-6xl px-6 py-5">
                    <h1 className="text-xl font-bold text-green-800">
                        Repositório Acadêmico IFPB
                    </h1>
                    <p className="text-sm text-gray-500">
                        Trabalhos de conclusão de curso
                    </p>
                </div>
            </header>

            <div className="mx-auto max-w-6xl px-6 py-8">
                {/* Busca e filtro */}
                <form
                    onSubmit={pesquisar}
                    className="mb-8 flex flex-col gap-3 sm:flex-row sm:flex-wrap"
                >
                    <input
                        value={busca}
                        onChange={(e) => setBusca(e.target.value)}
                        placeholder="Buscar trabalhos..."
                        className="min-w-48 flex-1 rounded-lg border bg-white px-4 py-3 text-sm outline-none focus:border-green-600"
                    />

                    <select
                        value={ano}
                        onChange={(e) => setAno(e.target.value)}
                        className="rounded-lg border bg-white px-4 py-3 text-sm outline-none focus:border-green-600"
                    >
                        <option value="">Todos os anos</option>
                        {Array.from(
                            { length: 15 },
                            (_, i) => new Date().getFullYear() - i
                        ).map((a) => (
                            <option key={a} value={a}>{a}</option>
                        ))}
                    </select>

                    <input
                        value={curso}
                        onChange={(e) => setCurso(e.target.value)}
                        placeholder="Curso"
                        className="rounded-lg border bg-white px-4 py-3 text-sm outline-none focus:border-green-600"
                    />

                    <input
                        value={palavraChave}
                        onChange={(e) => setPalavraChave(e.target.value)}
                        placeholder="Palavra-chave"
                        className="rounded-lg border bg-white px-4 py-3 text-sm outline-none focus:border-green-600"
                    />

                    <button
                        type="submit"
                        className="rounded-lg bg-green-700 px-6 py-3 text-sm font-semibold text-white hover:bg-green-800"
                    >
                        Buscar
                    </button>
                </form>

                {/* Resultados */}
                <div className="mb-5 flex items-center justify-between">
                    <h2 className="text-lg font-semibold text-gray-800">
                        Trabalhos publicados
                    </h2>
                    <span className="text-sm text-gray-500">
                        {total} resultado(s)
                    </span>
                </div>

                {loading ? (
                    <p className="py-12 text-center text-gray-500">
                        Carregando trabalhos...
                    </p>
                ) : erro ? (
                    <div className="py-12 text-center">
                        <p className="text-gray-700">
                            Não foi possível carregar os trabalhos.
                        </p>
                        <button
                            onClick={() => void carregar()}
                            className="mt-3 text-sm font-semibold text-green-700 hover:underline"
                        >
                            Tentar novamente
                        </button>
                    </div>
                ) : trabalhos.length === 0 ? (
                    <div className="py-12 text-center">
                        <p className="font-medium text-gray-700">
                            Nenhum trabalho encontrado.
                        </p>
                        <p className="mt-1 text-sm text-gray-500">
                            Tente alterar os termos da busca ou os filtros.
                        </p>
                    </div>
                ) : (
                    <>
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                            {trabalhos.map((trabalho) => (
                                <Link
                                    key={trabalho.id}
                                    to={`/trabalhos/${trabalho.id}`}
                                    className="rounded-lg border bg-white p-5 transition hover:border-green-500 hover:shadow-sm"
                                >
                                    <span className="text-xs font-semibold text-green-700">
                                        {trabalho.curso} · {trabalho.ano}
                                    </span>

                                    <h3 className="mt-3 font-semibold text-gray-900">
                                        {trabalho.titulo}
                                    </h3>

                                    <p className="mt-3 text-sm text-gray-500">
                                        Orientador: {trabalho.orientador}
                                    </p>

                                    <p className="mt-1 text-sm text-gray-500">
                                        Autor(es): {trabalho.autores.join(", ")}
                                    </p>

                                    <p className="mt-4 text-sm font-medium text-green-700">
                                        Ver detalhes →
                                    </p>
                                </Link>
                            ))}
                        </div>

                        {/* Paginação */}
                        <div className="mt-8 flex items-center justify-between">
                            <button
                                disabled={!temAnterior}
                                onClick={() => void carregar(pagina - 1)}
                                className="rounded-lg border bg-white px-4 py-2 text-sm disabled:opacity-40"
                            >
                                Anterior
                            </button>

                            <span className="text-sm text-gray-500">
                                Página {pagina}
                            </span>

                            <button
                                disabled={!temProxima}
                                onClick={() => void carregar(pagina + 1)}
                                className="rounded-lg border bg-white px-4 py-2 text-sm disabled:opacity-40"
                            >
                                Próxima
                            </button>
                        </div>
                    </>
                )}
            </div>
        </main>
    );
}