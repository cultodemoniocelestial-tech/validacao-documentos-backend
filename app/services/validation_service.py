from typing import Dict, Any, List, Optional
from difflib import SequenceMatcher
from app.models import Course, DocumentExtraction


class ValidationService:
    """Serviço para validação de experiência profissional"""
    
    def __init__(self):
        self.similarity_threshold = 0.7  # 70% de similaridade
    
    def validate_experience(
        self,
        extraction: DocumentExtraction,
        course: Course
    ) -> Dict[str, Any]:
        """
        Validar se a experiência extraída atende aos requisitos do curso
        
        Returns:
            Dict com status (approved, rejected, manual_review) e detalhes
        """
        validation_result = {
            "status": "manual_review",
            "required_months": course.minimum_months,
            "found_months": extraction.months_worked or 0,
            "position_match": None,
            "details": {
                "position_found": extraction.position,
                "accepted_positions": course.accepted_positions,
                "company": extraction.company_name,
                "dates": {
                    "start": extraction.start_date,
                    "end": extraction.end_date
                }
            }
        }
        
        # Verificar se há meses trabalhados
        if not extraction.months_worked or extraction.months_worked <= 0:
            validation_result["status"] = "manual_review"
            validation_result["details"]["reason"] = "Não foi possível calcular o tempo de experiência"
            return validation_result
        
        # Verificar tempo mínimo
        meets_time_requirement = extraction.months_worked >= course.minimum_months
        
        # Verificar cargo
        position_match = self._check_position_match(
            extraction.position,
            course.accepted_positions
        )
        
        if position_match:
            validation_result["position_match"] = position_match["matched_position"]
            validation_result["details"]["similarity_score"] = position_match["similarity"]
        
        # Determinar status final
        if meets_time_requirement and position_match and position_match["similarity"] >= self.similarity_threshold:
            validation_result["status"] = "approved"
            validation_result["details"]["reason"] = "Atende a todos os requisitos"
        elif not meets_time_requirement:
            validation_result["status"] = "rejected"
            validation_result["details"]["reason"] = f"Tempo de experiência insuficiente. Requerido: {course.minimum_months} meses, Encontrado: {extraction.months_worked} meses"
        elif not position_match or position_match["similarity"] < self.similarity_threshold:
            validation_result["status"] = "manual_review"
            validation_result["details"]["reason"] = "Cargo não corresponde exatamente aos aceitos. Requer análise manual."
        else:
            validation_result["status"] = "manual_review"
            validation_result["details"]["reason"] = "Requer análise manual para confirmação"
        
        return validation_result
    
    def _check_position_match(
        self,
        position: Optional[str],
        accepted_positions: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Verificar se o cargo corresponde a algum dos aceitos
        Usa similaridade de strings para match flexível
        """
        if not position or not accepted_positions:
            return None
        
        position_lower = position.lower().strip()
        best_match = None
        best_similarity = 0.0
        
        for accepted in accepted_positions:
            accepted_lower = accepted.lower().strip()
            
            # Calcular similaridade
            similarity = SequenceMatcher(None, position_lower, accepted_lower).ratio()
            
            # Verificar se contém a palavra
            if accepted_lower in position_lower or position_lower in accepted_lower:
                similarity = max(similarity, 0.85)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = accepted
        
        if best_match:
            return {
                "matched_position": best_match,
                "similarity": best_similarity
            }
        
        return None
    
    def validate_multiple_experiences(
        self,
        extractions: List[DocumentExtraction],
        course: Course
    ) -> Dict[str, Any]:
        """
        Validar múltiplas experiências e consolidar resultado
        """
        if not extractions:
            return {
                "status": "rejected",
                "reason": "Nenhuma experiência encontrada",
                "total_months": 0,
                "required_months": course.minimum_months
            }
        
        # Validar cada experiência
        individual_validations = []
        total_months = 0
        approved_count = 0
        
        for extraction in extractions:
            validation = self.validate_experience(extraction, course)
            individual_validations.append(validation)
            
            if validation["status"] == "approved":
                approved_count += 1
                total_months += extraction.months_worked or 0
        
        # Determinar status consolidado
        consolidated_status = "rejected"
        if total_months >= course.minimum_months and approved_count > 0:
            consolidated_status = "approved"
        elif total_months >= course.minimum_months * 0.8:  # 80% do requisito
            consolidated_status = "manual_review"
        
        return {
            "status": consolidated_status,
            "total_months": total_months,
            "required_months": course.minimum_months,
            "approved_experiences": approved_count,
            "total_experiences": len(extractions),
            "individual_validations": individual_validations
        }
