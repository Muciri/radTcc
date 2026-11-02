import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { TrabalhoService } from "../services/TrabalhoService";
import type { Trabalho } from "../types/Trabalho";

export function TrabalhoDetalhes() {
    const { id } = useParams<{ id: string }>();

    const [trabalho, setTrabalho] = useState<Trabalho | null>(null);
    const [loading, setLoading] = useState(true);
    const [erro, setErro] = useState(false);

    useEffect(() => {
        async function carregar() {
            if (!id) {
                setErro(true);
                setLoading(false);
                return;
            }

            try {
                const dados = await TrabalhoService.getById(id);
                setTrabalho(dados);
            } catch {
                setErro(true);
            } finally {
                setLoading(false);
            }
        }

        void carregar();
    }, [id]);

    if (loading) {
        return (
            <main className="min-h-screen bg-gray-50 p-8 text-center text-gray-500">
                Carregando trabalho...
            </main>
        );
    }

    if (erro || !trabalho) {
        return (
            <main className="min-h-screen bg-gray-50 p-8 text-center">
                <p className="text-gray-700">
                    Não foi possível encontrar o trabalho.
                </p>
                <Link to="/" className="mt-3 inline-block text-green-700 hover:underline">
                    Voltar para a página inicial
                </Link>
            </main>
        );
    }

    return (
        <main className="min-h-screen bg-gray-50">
            <header className="border-b bg-white">
                <div className="mx-auto max-w-4xl px-6 py-5">
                    <Link to="/" className="text-sm text-green-700 hover:underline">
                        ← Voltar aos trabalhos
                    </Link>
                </div>
            </header>

            <div className="mx-auto max-w-4xl px-6 py-8">
                <article className="rounded-lg border bg-white p-6 shadow-sm">
                    <div className="flex flex-col gap-1">
                        <span className="text-sm font-semibold text-green-700">
                            curso: {trabalho.curso}
                        </span>

                        <span className="text-sm font-semibold text-green-700">
                            ano: {trabalho.ano}
                        </span>
                    </div>

                    <h1 className="mt-3 text-2xl font-bold text-gray-900">
                        {trabalho.titulo}
                    </h1>

                    <div className="mt-6 grid gap-5 sm:grid-cols-2">
                        <div>
                            <h2 className="text-sm font-semibold text-gray-500">
                                Autor(es)
                            </h2>
                            <p className="mt-1 text-gray-800">
                                {trabalho.autores?.join(", ") || "Não informado"}
                            </p>
                        </div>

                        <div>
                            <h2 className="text-sm font-semibold text-gray-500">
                                Orientador
                            </h2>
                            <p className="mt-1 text-gray-800">
                                {trabalho.orientador || "Não informado"}
                            </p>
                        </div>

                        <div>
                            <h2 className="text-sm font-semibold text-gray-500">
                                Coorientador
                            </h2>
                            <p className="mt-1 text-gray-800">
                                {trabalho.coorientador || "Não informado"}
                            </p>
                        </div>

                        <div>
                            <h2 className="text-sm font-semibold text-gray-500">
                                Data de defesa
                            </h2>
                            <p className="mt-1 text-gray-800">
                                {trabalho.data_defesa
                                    ? new Date(`${trabalho.data_defesa}T00:00:00`).toLocaleDateString("pt-BR")
                                    : "Não informada"}
                            </p>
                        </div>
                    </div>

                    <div className="mt-8 border-t pt-6">
                        <h2 className="font-semibold text-gray-900">
                            Resumo
                        </h2>
                        <p className="mt-2 whitespace-pre-line text-justify leading-relaxed text-gray-700">
                            {trabalho.resumo || "Resumo não disponível."}
                        </p>
                    </div>

                    <div className="mt-6">
                        <h2 className="font-semibold text-gray-900">
                            Palavras-chave
                        </h2>

                        <div className="mt-2 flex flex-wrap gap-2">
                            {trabalho.palavras_chave?.length ? (
                                trabalho.palavras_chave.map((palavra, index) => (
                                    <span
                                        key={index}
                                        className="rounded-full bg-green-50 px-3 py-1 text-sm text-green-800"
                                    >
                                        {palavra}
                                    </span>
                                ))
                            ) : (
                                <p className="text-sm text-gray-500">
                                    Nenhuma palavra-chave cadastrada.
                                </p>
                            )}
                        </div>
                    </div>
                </article>
            </div>
        </main>
    );
}