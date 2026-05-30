Markdown# Veritais — Backend API

API de verificação de fake news construída com **FastAPI + Google Gemini AI (SDK moderno `google-genai`)**.

---

## 📂 Estrutura dos arquivos

veritais-backend/└── veritais-backend/     ← Pasta principal do código├── main.py           ← Rotas da API e integração com Gemini├── models.py         ← Banco de dados (SQLite + SQLAlchemy)├── analyzer.py       ← Lógica de prompts e tratamento de respostas├── factcheck.py      ← Integração com APIs externas (Google Fact Check)├── requirements.txt  ← Dependências Python necessárias└── .env.example      ← Modelo de variáveis de ambiente
---

## 🚀 Como rodar o projeto do zero (Passo a Passo)

Certifique-se de ter o **Python 3.10 ou superior** instalado no seu computador antes de começar.

### 1. Entrar na pasta correta do código
Abra o terminal e navegue até a subpasta interna onde estão os scripts e o arquivo `requirements.txt`:
```bash
cd veritais-backend/veritais-backend
2. Escolha como deseja rodar (Instalação das dependências)Se você utiliza Ambiente Virtual (Recomendado):Bash# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Ativar no Mac/Linux:
source venv/bin/activate

# Instalar as bibliotecas
pip install -r requirements.txt
pip install google-genai
Se você prefere instalar Globalmente no Sistema (Mais rápido e sem erros de caminho):Bashpy -m pip install fastapi uvicorn[standard] google-genai httpx python-multipart sqlalchemy pydantic python-dotenv
3. Configurar a Chave da IA (Gemini API)A chave padrão de demonstração já está embutida diretamente no código do arquivo main.py para facilitar a correção.Se preferir usar sua própria chave, crie um arquivo .env baseado no .env.example e configure a variável:Snippet de códigoGEMINI_API_KEY=sua_chave_do_gemini_aqui
4. Inicializar o ServidorCom as dependências instaladas, ligue o servidor executando:Bashpy -m uvicorn main:app --reload
Se o comando py não estiver mapeado no seu sistema, utilize o padrão:Bashuvicorn main:app --reload
O servidor estará ativo em: http://127.0.0.1:8000🎯 Interface Interativa e Testes (Swagger UI)O FastAPI gera automaticamente uma documentação visual perfeita para testar as rotas da IA sem precisar de um front-end configurado.Acesse pelo seu navegador: http://127.0.0.1:8000/docsEndpoints disponíveis para o Front-endMétodoRotaParâmetrosDescriçãoPOST/verify/text{ "text": "...", "title": "..." }Envia uma afirmação textual direta para a IA avaliar.POST/verify/url{ "url": "..." }Baixa o texto de um site e valida o conteúdo na IA.POST/verify/imageEnvio de arquivo (Multipart/Form-Data)Envia um arquivo de imagem (print, foto) para análise multimodal.GET/historyNenhum (Query params opcionais)Retorna a lista completa de checagens salvas no banco de dados.GET/history/{id}ID na URLTraz a checagem detalhada e a justificativa completa da IA.DELETE/history/{id}ID na URLRemove um registro específico do histórico.
