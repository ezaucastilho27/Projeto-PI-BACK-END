# Veritais — Backend API

API de verificação de fake news construída com **FastAPI + Google Gemini AI** (SDK moderno `google-genai`).

---

## 📂 Estrutura dos Arquivos

veritais-backend/
└── veritais-backend/        ← Pasta principal do código
├── main.py              ← Rotas da API e integração com Gemini
├── models.py            ← Banco de dados (SQLite + SQLAlchemy)
├── analyzer.py          ← Lógica de prompts e tratamento de respostas
├── factcheck.py         ← Integração com APIs externas (Google Fact Check)
├── requirements.txt     ← Dependências Python necessárias
└── .env.example         ← Modelo de variáveis de ambiente

---

## 🚀 Como Rodar o Projeto do Zero (Passo a Passo)

Certifique-se de ter o **Python 3.10 ou superior** instalado no seu computador antes de começar.

### 1. Instalação e Execução via Terminal (Linha Única)

Copie o comando abaixo, cole no seu terminal e aperte **Enter** para instalar todas as dependências e iniciar o servidor:

```powershell
cd veritais-backend ; cd veritais-backend ; py -m pip install fastapi uvicorn[standard] google-genai httpx python-multipart sqlalchemy pydantic python-dotenv ; py -m uvicorn main:app --reload
```

> **Nota:** Caso o comando `py` não esteja configurado no seu sistema, substitua-o por `python`.

O servidor estará ativo localmente em: **http://127.0.0.1:8000**

---

## 📖 Documentação Automática

O FastAPI gera automaticamente uma documentação visual para testar todas as rotas sem a necessidade de um front-end ativo.

Acesse pelo navegador: **http://127.0.0.1:8000/docs**

---

## 🔌 Endpoints Disponíveis

| Método   | Rota            | Parâmetros                          | Descrição                                                        |
|----------|-----------------|-------------------------------------|------------------------------------------------------------------|
| `POST`   | `/verify/text`  | `{ "text": "...", "title": "..." }` | Envia uma afirmação textual para a IA avaliar.                   |
| `POST`   | `/verify/url`   | `{ "url": "..." }`                  | Baixa o conteúdo de um link externo e valida o texto na IA.     |
| `POST`   | `/verify/image` | Arquivo (Multipart/Form-Data)       | Envia uma imagem (print, foto) para análise multimodal.         |
| `GET`    | `/history`      | Nenhum (query params opcionais)     | Retorna a lista completa de checagens salvas no banco de dados.  |
| `GET`    | `/history/{id}` | ID na URL                           | Traz a checagem detalhada e a justificativa completa da IA.      |
| `DELETE` | `/history/{id}` | ID na URL                           | Remove um registro específico do histórico.                      |

---

## 💾 Banco de Dados Local (SQLite)

O sistema utiliza **SQLite**, eliminando qualquer necessidade de configuração de servidores externos.

- O arquivo `veritais.db` é gerado **automaticamente** na raiz do projeto ao iniciar o servidor pela primeira vez.
- O histórico de análises, vereditos e notas de confiança retornados pelo Gemini ficam salvos e persistidos localmente.

---

## 🌐 Integração com Front-end (CORS Ativado)

A API possui o middleware CORS configurado para aceitar requisições de qualquer origem (`allow_origins=["*"]`). Você pode conectar seu front-end em React, Vue ou JavaScript nativo sem problemas de bloqueio no navegador.

**Exemplo prático com Axios:**

```javascript
const response = await axios.post("http://127.0.0.1:8000/verify/text", {
  text: "O chá de casca de laranja elimina vírus em 24 horas."
});

console.log(response.data.verdict); // Retorna "FALSO" ou "SUSPEITO"
```
