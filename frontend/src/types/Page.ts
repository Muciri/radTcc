import type { Trabalho } from "./Trabalho";

export type Page = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Trabalho[];
};