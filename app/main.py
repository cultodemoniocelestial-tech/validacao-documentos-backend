from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api import document_router, course_router, validation_router, report_router

# Criar aplicação FastAPI
app = FastAPI(
    title="Sistema de Validação de Documentos",
    description="API para validação automática de documentos e experiência profissional para cursos técnicos",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(document_router.router)
app.include_router(course_router.router)
app.include_router(validation_router.router)
app.include_router(report_router.router)


@app.on_event("startup")
async def startup_event():
    """Evento de inicialização da aplicação"""
    # Inicializar banco de dados
    init_db()
    print("✅ Banco de dados inicializado")


@app.get("/")
async def root():
    """Rota raiz da API"""
    return {
        "message": "Sistema de Validação de Documentos - API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "service": "validacao-documentos-api"
    }
