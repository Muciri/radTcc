# Catálogo de TCCs com API pública

Atividade de laboratório de Rapid Application Development (RAD), curso de Tecnólogo em Sistemas para Internet, IFPB.

Integrantes:

- Francisco Viana
- Murilo Maciel Rodrigues

O sistema é um catálogo de trabalhos de conclusão de curso com duas portas no mesmo projeto Django:

- **Porta aberta** (`/api/v1/publico/`): leitura, sem conta e sem senha, só de trabalhos publicados.
- **Porta fechada** (`/api/v1/gestao/`): escrita, para a coordenação, com token no cabeçalho.

O back-end é só API, não existe template nem formulário Django. A tela é um programa separado, na pasta `frontend/`.

## Estrutura

```
backend/    projeto Django (config/ e app catalogo/), db.sqlite3 com os dados de teste
frontend/   cliente React, servido por conta própria
```

## Como subir o back-end

Precisa de Python 3.12 ou mais novo.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

A API sobe em `http://localhost:8000`. O `db.sqlite3` já vem com os dados de teste. Se o banco for apagado, `python manage.py migrate` seguido de `python manage.py carregar_dados` recria tudo (o comando pode ser repetido sem duplicar nada).

Dados carregados: 4 cursos, 8 orientadores, 30 trabalhos em 6 anos (2021 a 2026), 15 palavras-chave, 6 trabalhos que não estão publicados e 3 trabalhos com dois autores.

## Como subir o front-end

Precisa de Node 20.19 ou mais novo, com o back-end já no ar.

```bash
cd frontend
npm install
npm run dev
```

A tela abre em `http://localhost:5173`. O endereço da API fica em `frontend/.env` (`VITE_API_URL` e `VITE_API_VERSION`). O CORS do back-end libera apenas essa origem.

Tecnologia do front-end: React 19 com TypeScript, Vite, Tailwind CSS, Axios e React Router.

## Contas da coordenação

| Usuário | Senha | Token |
|---|---|---|
| `coordenacao1` | `Coord@2026-1` | `db68077098eaf09482858509eba913e9277861cf` |
| `coordenacao2` | `Coord@2026-2` | `30b3872e65ade3787292a3c733b6851e316cc10a` |

As duas também entram no admin do Django em `/admin/`. O token vai no cabeçalho `Authorization: Token <token>`. Também dá para gerar um novo com usuário e senha:

```bash
curl -X POST http://localhost:8000/api/v1/gestao/token/ \
  -d username=coordenacao1 -d password='Coord@2026-1'
```

## Endpoints

Documentação navegável em `http://localhost:8000/api/docs/` e schema OpenAPI em `http://localhost:8000/api/schema/`.

### Porta aberta (sem token)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/v1/publico/trabalhos/` | Lista paginada de trabalhos publicados |
| GET | `/api/v1/publico/trabalhos/{id}/` | Detalhe com resumo e palavras-chave. 404 se não estiver publicado |
| GET | `/api/v1/publico/estatisticas/` | Trabalhos por ano, por curso e orientadores com mais trabalhos |

Parâmetros da lista, todos combináveis:

| Parâmetro | Efeito |
|---|---|
| `search` | busca no título, no resumo, no nome dos autores e no nome do orientador |
| `ano` | filtra pelo ano |
| `curso` | filtra pela sigla do curso, por exemplo `TSI` |
| `palavra_chave` | filtra pelo termo exato da palavra-chave |
| `ordering` | `ano`, `-ano`, `titulo` ou `-titulo` |
| `page`, `page_size` | página e tamanho (padrão 10, máximo 100) |

### Porta fechada (com token)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/v1/gestao/token/` | Troca usuário e senha por token (não exige token) |
| GET, POST | `/api/v1/gestao/trabalhos/` | Lista (qualquer situação, com nota) e cadastro. Filtros `situacao`, `ano` e `curso` (id) |
| GET, PUT, PATCH, DELETE | `/api/v1/gestao/trabalhos/{id}/` | Consulta, alteração e exclusão. Publicar é um PATCH com `situacao: publicado` |
| GET, POST | `/api/v1/gestao/cursos/` e `/{id}/` | CRUD de cursos |
| GET, POST | `/api/v1/gestao/orientadores/` e `/{id}/` | CRUD de orientadores |
| GET, POST | `/api/v1/gestao/autores/` e `/{id}/` | CRUD de autores |
| GET, POST | `/api/v1/gestao/palavras-chave/` e `/{id}/` | CRUD de palavras-chave |

Sem token, qualquer rota da porta fechada responde 401. Excluir curso ou orientador que ainda estão em algum trabalho responde 409, assim como excluir o único autor de um trabalho.

### Validações

Valem no cadastro e na alteração de trabalhos, e o erro sai em JSON com status 400:

1. O ano não pode ser maior que o ano corrente.
2. Um trabalho só vai para `publicado` se tiver nota e data de defesa.
3. Todo trabalho tem no mínimo um e no máximo dois autores.
4. Não existem dois trabalhos com o mesmo título no mesmo curso e ano.

Exemplo, ao publicar sem nota:

```json
{"situacao": ["Um trabalho só pode ser publicado com nota e data de defesa."]}
```

O campo `cadastrado_por` é definido pelo token e é ignorado se vier no JSON. Também não é aceito o coorientador igual ao orientador.

## As três decisões sobre a API pública

### 1. O que a porta aberta expõe

**Quais registros:** só os que estão `publicado`. O recorte é feito no queryset da view, então um trabalho em andamento ou só defendido não aparece na lista e também não é alcançável pelo detalhe, mesmo que o id seja informado direto (responde 404, como se não existisse).

**Quais campos:**

| Na lista | No detalhe (a mais) |
|---|---|
| `id`, `titulo`, `ano`, `data_defesa`, `arquivo_pdf`, `curso`, `orientador`, `coorientador`, `autores` | `resumo`, `palavras_chave` |

Curso, orientador e autores saem por nome, não por id. Exemplo real:

```json
{
  "id": 7,
  "titulo": "Acessibilidade em portais de universidades federais",
  "ano": 2024,
  "data_defesa": "2024-03-11",
  "arquivo_pdf": "https://repositorio.ifpb.edu.br/tcc/2024-07.pdf",
  "curso": "TSI - Tecnologia em Sistemas para Internet",
  "orientador": "Mariana Cavalcanti Rocha",
  "coorientador": null,
  "autores": ["Mateus Martins Araújo"],
  "resumo": "Auditoria de conformidade com as diretrizes WCAG em portais institucionais...",
  "palavras_chave": ["acessibilidade", "desenvolvimento web"]
}
```

**Ficaram de fora:** a nota, o e-mail dos autores, o e-mail dos orientadores, a situação e quem cadastrou o trabalho.

**Por quê:** quem consulta o acervo quer saber se um tema já foi trabalhado e achar o trabalho, e para isso título, resumo, pessoas e palavras-chave bastam. A nota é dado acadêmico do aluno, os e-mails são dados pessoais (os autores nem têm conta no sistema, então nunca autorizaram aparecer) e a situação e o cadastrante são controle interno da coordenação. Como a porta é aberta e não sabemos quem consome, tudo que sai vira promessa: é mais seguro expor pouco e acrescentar depois do que retirar um campo de quem já depende dele.

Para isso existem serializers separados, `TrabalhoPublicoSerializer` e `TrabalhoPublicoDetalheSerializer` na porta aberta e `TrabalhoGestaoSerializer` na fechada. A nota e os e-mails simplesmente não existem nos serializers públicos, em vez de serem escondidos por um `if`.

### 2. Versão no endereço

**Sim, nas duas portas:** `/api/v1/publico/` e `/api/v1/gestao/`. Foi usado o `URLPathVersioning` do DRF com `v1` como única versão permitida, então um endereço com outra versão (por exemplo `/api/v2/...`) responde 404.

**Porta aberta:** é onde a versão é indispensável. Qualquer pessoa pode ter um script lendo a API sem nos avisar, e sem senha não temos como saber quem é. Se um campo mudar de nome ou de formato (por exemplo `resumo` virar `resumo_pt`), a versão nova sobe em `/v2/` e quem usa a `/v1/` continua funcionando.

**Porta fechada:** também versionada, por consistência. As duas portas compartilham o mesmo esquema de rotas e ficaria confuso uma ter versão e a outra não. Além disso a gestão pode ganhar outros clientes além do admin, como uma tela de cadastro, e esses clientes passam a depender do contrato do mesmo jeito. A diferença para a porta aberta é só de grau: na gestão é possível avisar os clientes, na pública não.

### 3. O que segura o uso

**Limite:** 30 requisições por minuto para cliente não autenticado, contadas por endereço de IP (`AnonRateThrottle` do DRF, taxa `30/min` em `settings.py`). Quem manda um token válido na porta fechada não entra nessa conta. O número foi escolhido para ser alto o bastante para uso normal de uma tela (uma busca, paginação e detalhes) e baixo o bastante para ser demonstrável na prática.

**O que o cliente recebe ao passar do limite:** status `429 Too Many Requests`, o cabeçalho `Retry-After` com os segundos de espera e um JSON com a mensagem:

```json
{"detail": "Limite de requisições excedido. Tente novamente em 60 segundos."}
```

Para ver acontecendo (a 31ª chamada responde 429):

```bash
for i in $(seq 1 31); do
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/api/v1/publico/trabalhos/
done
```

Os endereços `/api/docs/` e `/api/schema/` não entram no limite, para quem lê a documentação não gastar a cota da API. Ficou de fora do limite também o endpoint de token, que usa a view padrão do DRF sem limitação, o que permite tentar senhas à vontade. Como o enunciado pede limite na porta aberta, deixamos isso registrado como limitação conhecida.

## ViewSet, `@api_view` e APIView

| Recurso | Escolha | Por quê |
|---|---|---|
| Trabalhos na porta aberta | `ReadOnlyModelViewSet` com router | só lista e detalhe sobre um model, o router gera as duas rotas e a mesma classe cuida de filtro, busca, ordenação e paginação |
| Trabalhos, cursos, orientadores, autores e palavras-chave na porta fechada | `ModelViewSet` com router | CRUD completo sobre um model, uma classe por recurso e as cinco rotas padrão geradas pelo router |
| Estatísticas | `@api_view` | não é um model nem tem CRUD, é uma leitura que calcula agregações e devolve um dicionário. Uma função resolve, e um ViewSet com router não traria nada |
| Token | `APIView` (`ObtainAuthToken`) | uma única ação, POST, que não consulta nenhum model do catálogo |

As estatísticas são calculadas pelo banco, com `Count` e `values().annotate()`, sempre sobre os trabalhos publicados. Nenhum número é guardado em campo.

## Como a avaliação pode conferir

Pela página `http://localhost:8000/api/docs/`, com `curl` ou pelo front-end. Alguns exemplos:

```bash
# porta aberta, sem token
curl "http://localhost:8000/api/v1/publico/trabalhos/?search=dados&curso=ADM&ordering=-ano"

# porta fechada sem token: 401
curl -X POST http://localhost:8000/api/v1/gestao/trabalhos/ -H "Content-Type: application/json" -d '{}'

# porta fechada com token: lista tudo, inclusive não publicados e com nota
curl http://localhost:8000/api/v1/gestao/trabalhos/ \
  -H "Authorization: Token db68077098eaf09482858509eba913e9277861cf"
```

Para ver o front-end sem dados (critério 29), desligue o `runserver` e recarregue a tela: ela mostra a mensagem de erro com a opção de tentar de novo.
