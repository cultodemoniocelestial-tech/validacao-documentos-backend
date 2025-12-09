# Sistema de Validação de Documentos - Backend

API REST desenvolvida em FastAPI para validação automática de documentos e experiência profissional para cursos técnicos por competência.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **PostgreSQL** - Banco de dados relacional
- **PaddleOCR / Tesseract** - Extração de texto via OCR
- **Pydantic** - Validação de dados
- **Python 3.11+**

## 📁 Estrutura do Projeto

```
app/
├── api/                    # Rotas da API
│   ├── document_router.py  # Upload e extração de documentos
│   ├── course_router.py    # CRUD de cursos
│   ├── validation_router.py # Validação de experiências
│   └── report_router.py    # Geração de relatórios
├── services/               # Lógica de negócio
│   ├── ocr_service.py      # Serviço de OCR
│   ├── validation_service.py # Serviço de validação
│   └── report_service.py   # Serviço de relatórios
├── repositories/           # Acesso a dados
│   ├── document_repository.py
│   └── course_repository.py
├── models/                 # Modelos do banco de dados
│   ├── document.py
│   └── course.py
├── schemas/                # Schemas Pydantic
│   ├── document_schema.py
│   └── course_schema.py
├── core/                   # Configurações
│   ├── config.py
│   └── database.py
└── main.py                 # Aplicação principal
```

## 🔧 Instalação Local

### 1. Instalar dependências do sistema

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-por poppler-utils

# macOS
brew install tesseract tesseract-lang poppler
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Editar .env com suas configurações
```

### 5. Configurar PostgreSQL

```bash
# Criar banco de dados
createdb validacao_documentos

# Ou usar Docker
docker run --name postgres-validacao \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=validacao_documentos \
  -p 5432:5432 \
  -d postgres:15
```

### 6. Inicializar banco de dados

```bash
python seed_data.py
```

### 7. Executar aplicação

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## 📡 Endpoints Principais

### Documentos

- `POST /documents/upload` - Upload de documento
- `POST /documents/{id}/extract` - Extrair dados do documento
- `GET /documents/{id}` - Buscar documento
- `GET /documents/{id}/extractions` - Buscar extrações
- `DELETE /documents/{id}` - Deletar documento

### Cursos

- `POST /courses/` - Criar curso
- `GET /courses/` - Listar cursos
- `GET /courses/{id}` - Buscar curso
- `PUT /courses/{id}` - Atualizar curso
- `DELETE /courses/{id}` - Deletar curso

### Validações

- `POST /validations/` - Validar documento para curso
- `GET /validations/{id}` - Buscar validação
- `GET /validations/document/{id}` - Validações de um documento
- `GET /validations/{id}/summary` - Resumo da validação

### Relatórios

- `GET /reports/document/{id}` - Relatório completo do documento
- `GET /reports/course/{id}/statistics` - Estatísticas do curso

## 🔄 Fluxo de Uso

1. **Upload do documento** → `POST /documents/upload`
2. **Extrair dados via OCR** → `POST /documents/{id}/extract`
3. **Validar para curso** → `POST /validations/`
4. **Gerar relatório** → `GET /reports/document/{id}`

## 🧪 Exemplo de Uso

```bash
# 1. Upload de documento
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@carteira_trabalho.pdf"

# Resposta: { "id": 1, "filename": "carteira_trabalho.pdf", ... }

# 2. Extrair dados
curl -X POST "http://localhost:8000/documents/1/extract"

# Resposta: [{ "company_name": "Empresa X", "position": "Técnico", ... }]

# 3. Validar para curso
curl -X POST "http://localhost:8000/validations/" \
  -H "Content-Type: application/json" \
  -d '{"document_id": 1, "course_id": 1}'

# Resposta: { "status": "approved", ... }

# 4. Gerar relatório
curl "http://localhost:8000/reports/document/1"
```

## 🚀 Deploy

### Railway

1. Criar novo projeto no Railway
2. Adicionar PostgreSQL
3. Conectar repositório GitHub
4. Configurar variáveis de ambiente
5. Deploy automático

### Render

1. Criar Web Service
2. Conectar repositório
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Docker

```bash
# Build
docker build -t validacao-backend .

# Run
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  validacao-backend
```

## 📝 Variáveis de Ambiente

```env
DATABASE_URL=postgresql://user:password@localhost:5432/validacao_documentos
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=./uploads
OCR_ENGINE=paddleocr
```

## 🧪 Testes

```bash
pytest
```

## 📄 Licença

MIT
