# Veritais — Backend API

API de verificação de fake news construída com **FastAPI + Claude AI**.

---

## Estrutura dos arquivos

```
veritais-backend/
├── main.py           ← Rotas da API (endpoints)
├── models.py         ← Banco de dados (SQLite + SQLAlchemy)
├── analyzer.py       ← Lógica de análise e prompt do Claude
├── factcheck.py      ← Integração APIs externas (Google, NewsAPI)
├── requirements.txt  ← Dependências Python
└── .env.example      ← Modelo de variáveis de ambiente
```

---

## Como rodar (passo a passo)

### 1. Clone / baixe a pasta `veritais-backend`

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env e coloque sua chave da Anthropic
```

A única chave **obrigatória** é a `ANTHROPIC_API_KEY`.  
As demais são opcionais — o sistema funciona sem elas.

### 5. Rode o servidor

```bash
uvicorn main:app --reload
```

A API estará disponível em: **http://localhost:8000**

---

## Endpoints disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Status da API |
| POST | `/verify/url` | Verifica uma URL |
| POST | `/verify/text` | Verifica um texto/afirmação |
| POST | `/verify/image` | Verifica uma imagem |
| GET | `/history` | Lista histórico de verificações |
| GET | `/history/{id}` | Detalhe de uma verificação |
| DELETE | `/history/{id}` | Remove uma verificação |

Documentação interativa: **http://localhost:8000/docs**

---

## Exemplos de uso

### Verificar URL
```bash
curl -X POST http://localhost:8000/verify/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com/noticia"}'
```

### Verificar texto
```bash
curl -X POST http://localhost:8000/verify/text \
  -H "Content-Type: application/json" \
  -d '{"text": "O governo anunciou que vacinas causam autismo"}'
```

### Verificar imagem
```bash
curl -X POST http://localhost:8000/verify/image \
  -F "file=@foto_suspeita.jpg"
```

---

## Resposta padrão (todos os endpoints)

```json
{
  "id": 1,
  "verdict": "FALSO",
  "confidence": 92,
  "summary": "A afirmação é falsa e contradiz evidências científicas consolidadas.",
  "analysis": "1. O que afirma...\n2. Evidências contra...\n3. Fontes confiáveis...",
  "sources_found": [],
  "checked_at": "2025-01-15T14:30:00"
}
```

**Vereditos possíveis:** `VERDADEIRO` | `FALSO` | `SUSPEITO` | `INCONCLUSIVO`

---

## Deploy gratuito (Railway)

1. Crie conta em https://railway.app
2. New Project → Deploy from GitHub repo
3. Adicione as variáveis de ambiente no painel do Railway
4. Deploy automático ✓

---

## Conectar ao front-end React

No seu `App.jsx`, use:
```js
const API_URL = "http://localhost:8000";  // local
// const API_URL = "https://seu-projeto.railway.app";  // produção

const res = await axios.post(`${API_URL}/verify/url`, { url });
```
