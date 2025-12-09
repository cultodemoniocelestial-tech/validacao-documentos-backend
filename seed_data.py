"""
Script para popular banco de dados com dados iniciais
"""
from app.core.database import SessionLocal, init_db
from app.models import Course

def seed_courses():
    """Criar cursos técnicos de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem cursos
        existing_courses = db.query(Course).count()
        if existing_courses > 0:
            print(f"✅ Banco já possui {existing_courses} curso(s)")
            return
        
        # Criar cursos de exemplo
        courses = [
            {
                "name": "Técnico em Informática",
                "code": "TEC-INFO",
                "description": "Curso técnico em informática para internet e desenvolvimento",
                "minimum_months": 12,
                "accepted_positions": [
                    "Técnico em Informática",
                    "Auxiliar de Informática",
                    "Assistente de TI",
                    "Suporte Técnico",
                    "Desenvolvedor",
                    "Programador",
                    "Analista de Suporte"
                ],
                "is_active": True
            },
            {
                "name": "Técnico em Administração",
                "code": "TEC-ADM",
                "description": "Curso técnico em administração empresarial",
                "minimum_months": 12,
                "accepted_positions": [
                    "Assistente Administrativo",
                    "Auxiliar Administrativo",
                    "Assistente de Departamento Pessoal",
                    "Auxiliar de Escritório",
                    "Secretário",
                    "Recepcionista"
                ],
                "is_active": True
            },
            {
                "name": "Técnico em Enfermagem",
                "code": "TEC-ENF",
                "description": "Curso técnico em enfermagem",
                "minimum_months": 18,
                "accepted_positions": [
                    "Auxiliar de Enfermagem",
                    "Técnico em Enfermagem",
                    "Cuidador",
                    "Atendente de Enfermagem"
                ],
                "is_active": True
            },
            {
                "name": "Técnico em Contabilidade",
                "code": "TEC-CONT",
                "description": "Curso técnico em contabilidade",
                "minimum_months": 12,
                "accepted_positions": [
                    "Auxiliar Contábil",
                    "Assistente Contábil",
                    "Auxiliar Fiscal",
                    "Assistente Fiscal",
                    "Auxiliar de Departamento Pessoal"
                ],
                "is_active": True
            },
            {
                "name": "Técnico em Logística",
                "code": "TEC-LOG",
                "description": "Curso técnico em logística",
                "minimum_months": 12,
                "accepted_positions": [
                    "Auxiliar de Logística",
                    "Assistente de Logística",
                    "Auxiliar de Almoxarifado",
                    "Conferente",
                    "Estoquista",
                    "Expedidor"
                ],
                "is_active": True
            }
        ]
        
        for course_data in courses:
            course = Course(**course_data)
            db.add(course)
        
        db.commit()
        print(f"✅ {len(courses)} cursos criados com sucesso!")
        
        # Listar cursos criados
        print("\n📚 Cursos cadastrados:")
        for course in courses:
            print(f"  - {course['code']}: {course['name']}")
        
    except Exception as e:
        print(f"❌ Erro ao criar cursos: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Inicializando banco de dados...")
    init_db()
    print("✅ Banco de dados inicializado\n")
    
    print("🌱 Populando banco com dados iniciais...")
    seed_courses()
    print("\n✅ Seed concluído!")
