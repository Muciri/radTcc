export type Trabalho = {
  id: number;
  titulo: string;
  ano: number;
  data_defesa: string;
  arquivo_pdf: string;
  curso: string;
  orientador: string;
  coorientador: string;
  autores: string[];
  resumo?: string;
  palavras_chave?: string[];
};