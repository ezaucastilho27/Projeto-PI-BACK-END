# Veritais — Backend API

API de verificação de fake news construída com **FastAPI + Google Gemini AI (SDK moderno `google-genai`)**.

---

## 📂 Estrutura dos arquivos

veritais-backend/
└── veritais-backend/     ← Pasta principal do código
├── main.py           ← Rotas da API e integração com Gemini
├── models.py         ← Banco de dados (SQLite + SQLAlchemy)
├── analyzer.py       ← Lógica de prompts e tratamento de respostas
├── factcheck.py      ← Integração com APIs externas (Google Fact Check)
├── requirements.txt  ← Dependências Python necessárias
└── .env.example      ← Modelo de variáveis de ambiente
---

## 🚀 Como rodar o projeto do zero (Passo a Passo)

Certifique-se de ter o **Python 3.10 ou superior** instalado no seu computador antes de começar.

### 1. Instalação e Execução Direta via Terminal (Linha Única)
Copie o comando contínuo abaixo, cole no seu terminal e aperte **Enter** para acessar automaticamente as pastas corretas, instalar todas as dependências globais e iniciar o servidor de primeira:

```powershell
cd veritais-backend ; cd veritais-backend ; py -m pip install fastapi uvicorn[standard] google-genai httpx python-multipart sqlalchemy pydantic python-dotenv ; py -m uvicorn main:app --reload
(Caso o comando py não esteja configurado no seu sistema, substitua-o por python).

O servidor estará ativo localmente em: http://127.0.0.1:8000

O FastAPI gera automaticamente uma documentação visual perfeita para testar todas as rotas da inteligência artificial sem a necessidade de um front-end ativo.Acesse pelo seu navegador: http://127.0.0.1:8000/docsEndpoints disponíveis para o Front-endMétodoRotaParâmetrosDescriçãoPOST/verify/text{ "text": "...", "title": "..." }Envia uma afirmação textual direta para a IA avaliar.POST/verify/url{ "url": "..." }Baixa o conteúdo de um link externo e valida o texto na IA.POST/verify/imageEnvio de arquivo (Multipart/Form-Data)Envia um arquivo de imagem (print, foto) para análise multimodal.GET/historyNenhum (Query params opcionais)Retorna a lista completa de checagens salvas no banco de dados.GET/history/{id}ID na URLTraz a checagem detalhada e a justificativa completa da IA.DELETE/history/{id}ID na URLRemove um registro específico do histórico.

💾 Banco de Dados Local (SQLite)
O sistema utiliza o banco de dados SQLite, eliminando qualquer complexidade ou configuração de servidores de banco de dados externos.

O arquivo veritais.db é gerado de forma 100% automática na raiz do projeto assim que o servidor é iniciado pela primeira vez.

O histórico de análises, vereditos e notas de confiança retornados pelo Gemini permanecem salvos e persistidos localmente nele.

🌐 Integração com Front-end (CORS Ativado)
Esta API já possui o middleware CORS configurado para aceitar requisições de qualquer origem (allow_origins=["*"]). Você pode conectar seu front-end em React, Vue ou Javascript nativo chamando o servidor local diretamente através do Axios ou Fetch API sem problemas de segurança no navegador.

JavaScript
// Exemplo prático de chamada no Front-end usando Axios
const response = await axios.post("[http://127.0.0.1:8000/verify/text](http://127.0.0.1:8000/verify/text)", {
  text: "O chá de casca de laranja elimina vírus em 24 horas."
});
console.log(response.data.verdict); // Retorna "FALSO" ou "SUSPEITO"

---

### 📥 Link de Download Direto do Arquivo

Clique no link abaixo para baixar o arquivo físico e direto no seu computador, evitando que qualquer erro de formatação misture as linhas de código com o texto comum:

👉 **[Baixar o arquivo README.md para o seu VS Code](sandbox:/README.md)**
