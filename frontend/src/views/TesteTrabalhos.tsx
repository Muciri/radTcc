import { useEffect, useState } from "react";
import { TrabalhoService } from "../services/TrabalhoService";
import type { Trabalho } from "../types/Trabalho";

type Filtros = NonNullable<
    Parameters<typeof TrabalhoService.getAll>[0]
>;

export default function TesteTrabalhos() {
    const [trabalhos, setTrabalhos] = useState<Trabalho[]>([]);
    const [detalhe, setDetalhe] = useState<Trabalho | null>(null);

    const [filtros, setFiltros] = useState<Filtros>({
        ordering: "-ano",
        page: 1,
        page_size: 10,
    });

    const [paginaAnterior, setPaginaAnterior] = useState<string | null>(null);
    const [proximaPagina, setProximaPagina] = useState<string | null>(null);
    const [count, setCount] = useState(0);

    const [id, setId] = useState("");
    const [loading, setLoading] = useState(false);
    const [erro, setErro] = useState("");

    async function buscar() {
        setLoading(true);
        setErro("");

        try {
            const response = await TrabalhoService.getAll(filtros);

            setTrabalhos(response.results);
            setCount(response.count);
            setPaginaAnterior(response.previous);
            setProximaPagina(response.next);
        } catch {
            setErro("Erro ao buscar trabalhos.");
            setTrabalhos([]);
        } finally {
            setLoading(false);
        }
    }

    async function buscarPorId() {
        if (!id) return;

        setLoading(true);
        setErro("");
        setDetalhe(null);

        try {
            const response = await TrabalhoService.getById(id);
            setDetalhe(response);
        } catch {
            setErro("Trabalho não encontrado.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        void buscar();
    }, []);

    function atualizarFiltro<K extends keyof Filtros>(
        campo: K,
        valor: Filtros[K]
    ) {
        setFiltros((atual) => ({
            ...atual,
            [campo]: valor,
            page: 1,
        }));
    }

    function mudarPagina(url: string | null) {
        if (!url) return;

        const params = new URL(url).searchParams;

        setFiltros((atual) => ({
            ...atual,
            page: Number(params.get("page") || 1),
        }));
    }

    return (
        <main className="mx-auto max-w-6xl space-y-6 p-6">
            <h1 className="text-2xl font-bold">
                Teste da API de Trabalhos
            </h1>

            {/* LISTAGEM E FILTROS */}
            <section className="space-y-4 rounded-xl border p-5">
                <h2 className="text-lg font-semibold">
                    1. Listar trabalhos (getAll)
                </h2>

                <div className="grid gap-3 md:grid-cols-2">
                    <input
                        className="rounded border p-2"
                        placeholder="Buscar título, autor, resumo..."
                        value={filtros.search || ""}
                        onChange={(e) => atualizarFiltro("search", e.target.value)}
                    />

                    <input
                        className="rounded border p-2"
                        placeholder="Ano"
                        type="number"
                        value={filtros.ano ?? ""}
                        onChange={(e) => atualizarFiltro(
                            "ano",
                            e.target.value ? Number(e.target.value) : undefined
                        )}
                    />

                    <input
                        className="rounded border p-2"
                        placeholder="Curso (ex: TSI)"
                        value={filtros.curso || ""}
                        onChange={(e) => atualizarFiltro("curso", e.target.value)}
                    />

                    <input
                        className="rounded border p-2"
                        placeholder="Palavra-chave"
                        value={filtros.palavra_chave || ""}
                        onChange={(e) => atualizarFiltro("palavra_chave", e.target.value)}
                    />

                    <select
                        className="rounded border p-2"
                        value={filtros.ordering}
                        onChange={(e) => atualizarFiltro(
                            "ordering",
                            e.target.value as Filtros["ordering"]
                        )}
                    >
                        <option value="-ano">Ano: mais recente</option>
                        <option value="ano">Ano: mais antigo</option>
                        <option value="titulo">Título: A-Z</option>
                        <option value="-titulo">Título: Z-A</option>
                    </select>

                    <select
                        className="rounded border p-2"
                        value={filtros.page_size}
                        onChange={(e) => atualizarFiltro(
                            "page_size",
                            Number(e.target.value)
                        )}
                    >
                        <option value={10}>10 por página</option>
                        <option value={20}>20 por página</option>
                        <option value={50}>50 por página</option>
                    </select>
                </div>

                <div className="flex gap-2">
                    <button
                        onClick={() => void buscar()}
                        disabled={loading}
                        className="rounded bg-blue-600 px-4 py-2 text-white"
                    >
                        Buscar
                    </button>

                    <button
                        onClick={() => {
                            setFiltros({
                                ordering: "-ano",
                                page: 1,
                                page_size: 10,
                            });
                            setTimeout(() => void buscar(), 0);
                        }}
                        className="rounded border px-4 py-2"
                    >
                        Limpar
                    </button>
                </div>

                <p className="text-sm text-gray-500">
                    {count} trabalho(s) encontrado(s)
                </p>

                {loading && <p>Carregando...</p>}
                {erro && <p className="text-red-600">{erro}</p>}

                <div className="divide-y">
                    {(trabalhos || []).map((trabalho) => (
                        <article key={trabalho.id} className="space-y-1 py-3">
                            <h3 className="font-semibold">{trabalho.titulo}</h3>
                            <p className="text-sm text-gray-500">
                                ID: {trabalho.id} | {trabalho.ano} | {trabalho.curso}
                            </p>
                            <p className="text-sm">
                                Orientador: {trabalho.orientador}
                            </p>
                            <button
                                onClick={() => {
                                    setId(String(trabalho.id));
                                    void TrabalhoService.getById(String(trabalho.id))
                                        .then(setDetalhe)
                                        .catch(() => setErro("Erro ao consultar trabalho."));
                                }}
                                className="text-sm text-blue-600"
                            >
                                Consultar detalhes
                            </button>
                        </article>
                    ))}
                </div>

                <div className="flex justify-between">
                    <button
                        disabled={!paginaAnterior || loading}
                        onClick={() => mudarPagina(paginaAnterior)}
                        className="rounded border px-3 py-2 disabled:opacity-40"
                    >
                        Anterior
                    </button>

                    <button
                        disabled={!proximaPagina || loading}
                        onClick={() => mudarPagina(proximaPagina)}
                        className="rounded border px-3 py-2 disabled:opacity-40"
                    >
                        Próxima
                    </button>
                </div>
            </section>

            {/* CONSULTA POR ID */}
            <section className="space-y-4 rounded-xl border p-5">
                <h2 className="text-lg font-semibold">
                    2. Consultar por ID (getById)
                </h2>

                <div className="flex gap-2">
                    <input
                        type="number"
                        min="1"
                        placeholder="ID do trabalho"
                        value={id}
                        onChange={(e) => setId(e.target.value)}
                        className="min-w-0 flex-1 rounded border p-2"
                    />

                    <button
                        onClick={() => void buscarPorId()}
                        disabled={loading}
                        className="rounded bg-blue-600 px-4 py-2 text-white"
                    >
                        Consultar
                    </button>
                </div>

                {detalhe && (
                    <pre className="overflow-x-auto rounded bg-gray-100 p-4 text-sm">
                        {JSON.stringify(detalhe, null, 2)}
                    </pre>
                )}
            </section>
        </main>
    );
}