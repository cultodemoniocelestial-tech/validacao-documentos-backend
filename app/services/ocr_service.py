import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from dateutil import parser as date_parser
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

from app.core.config import settings


class OCRService:
    """Serviço para extração de texto via OCR"""
    
    def __init__(self):
        self.ocr_engine = "tesseract"
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extrair texto de uma imagem"""
        try:
            # Usar Tesseract
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='por')
            return text
        except Exception as e:
            print(f"Erro ao extrair texto da imagem: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrair texto de um PDF"""
        try:
            # Converter PDF para imagens
            images = convert_from_path(pdf_path, dpi=300)
            all_text = []
            
            for i, image in enumerate(images):
                # Salvar temporariamente
                temp_image_path = f"/tmp/page_{i}.jpg"
                image.save(temp_image_path, 'JPEG')
                
                # Extrair texto
                text = self.extract_text_from_image(temp_image_path)
                all_text.append(text)
                
                # Remover arquivo temporário
                os.remove(temp_image_path)
            
            return "\n\n".join(all_text)
        except Exception as e:
            print(f"Erro ao extrair texto do PDF: {e}")
            return ""
    
    def extract_text(self, file_path: str, file_type: str) -> str:
        """Extrair texto de um arquivo (imagem ou PDF)"""
        if file_type == "pdf":
            return self.extract_text_from_pdf(file_path)
        else:
            return self.extract_text_from_image(file_path)
    
    def parse_work_experience(self, text: str) -> List[Dict[str, Any]]:
        """
        Parsear experiências profissionais do texto extraído
        Procura por padrões comuns em carteiras de trabalho
        """
        experiences = []
        
        # Padrões para identificar informações
        company_patterns = [
            r'(?:empresa|empregador|razão social)[\s:]+([^\n]+)',
            r'CNPJ[\s:]+[\d\.\/\-]+[\s]+([^\n]+)',
        ]
        
        position_patterns = [
            r'(?:cargo|função|ocupação)[\s:]+([^\n]+)',
            r'CBO[\s:]+[\d\-]+[\s]+([^\n]+)',
        ]
        
        date_patterns = [
            r'(?:admissão|entrada|início|data de entrada)[\s:]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
            r'(?:saída|desligamento|término|data de saída)[\s:]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
        ]
        
        # Dividir texto em blocos (cada experiência)
        lines = text.split('\n')
        current_experience = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_experience:
                    experiences.append(current_experience)
                    current_experience = {}
                continue
            
            # Tentar extrair empresa
            for pattern in company_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    current_experience['company_name'] = match.group(1).strip()
            
            # Tentar extrair cargo
            for pattern in position_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    current_experience['position'] = match.group(1).strip()
            
            # Tentar extrair datas
            date_matches = re.findall(r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}', line)
            if date_matches:
                if 'start_date' not in current_experience and len(date_matches) > 0:
                    current_experience['start_date'] = date_matches[0]
                if len(date_matches) > 1:
                    current_experience['end_date'] = date_matches[1]
                elif 'start_date' in current_experience and len(date_matches) == 1:
                    if 'admiss' not in line.lower() and 'entrada' not in line.lower():
                        current_experience['end_date'] = date_matches[0]
        
        # Adicionar última experiência
        if current_experience:
            experiences.append(current_experience)
        
        # Calcular meses trabalhados
        for exp in experiences:
            if 'start_date' in exp:
                try:
                    start = self._parse_date(exp['start_date'])
                    end = self._parse_date(exp.get('end_date', datetime.now().strftime('%d/%m/%Y')))
                    
                    if start and end:
                        months = (end.year - start.year) * 12 + (end.month - start.month)
                        exp['months_worked'] = max(0, months)
                except Exception as e:
                    print(f"Erro ao calcular meses: {e}")
                    exp['months_worked'] = 0
        
        return experiences
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parsear string de data para datetime"""
        try:
            # Tentar diferentes formatos
            formats = ['%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y']
            for fmt in formats:
                try:
                    return datetime.strptime(date_str.strip(), fmt)
                except ValueError:
                    continue
            
            # Tentar parser automático
            return date_parser.parse(date_str, dayfirst=True)
        except Exception:
            return None
