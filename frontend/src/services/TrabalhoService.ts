import api from "./api";

import type { Trabalho } from "../types/Trabalho";
import type { Page } from "../types/Page";

interface TrabalhoFiltros {
    search?: string;
    ano?: number;
    curso?: string;
    palavra_chave?: string;
    ordering?: 'ano' | '-ano' | 'titulo' | '-titulo';
    page?: number;
    page_size?: number;
}

export const TrabalhoService = {
    getAll: async (filtros?: TrabalhoFiltros): Promise<Page> => {
        const params = new URLSearchParams();

        if (filtros) {
            Object.entries(filtros).forEach(([chave, valor]) => {
                if (valor !== undefined && valor !== null && valor !== '') {
                    params.append(chave, String(valor));
                }
            });
        }

        const response = await api.get<Page>(
            `/publico/trabalhos/?${params.toString()}`
        );

        return response.data;
    },
    
    getById: async(id:string): Promise<Trabalho> => {
        const response = await api.get<Trabalho>(`/publico/trabalhos/${id}`);
        return response.data;
    }
}