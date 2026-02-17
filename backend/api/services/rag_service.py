"""
RAG Service para el Chat de la Wiki
Utiliza Gemini para responder preguntas basadas en el contenido de la Wiki

Diseñado para ser compatible con migración futura a:
- PostgreSQL + pgvector en Cloud SQL
- Vertex AI Search
"""

import os
import re
import json
import logging
import numpy as np
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

import google.generativeai as genai

from django.conf import settings
from django.db import models

logger = logging.getLogger(__name__)


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calcula la similitud de coseno entre dos vectores"""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class RAGService:
    """Servicio de Retrieval-Augmented Generation para el Wiki Chat"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if RAGService._initialized:
            return
            
        self.api_key = getattr(settings, 'GEMINI_API_KEY', os.environ.get('GEMINI_API_KEY'))
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY no configurada. El chat no funcionará.")
            self.enabled = False
            RAGService._initialized = True
            return
        
        try:
            # Configurar Gemini
            genai.configure(api_key=self.api_key)
            
            # Modelo para chat (usando gemini-2.0-flash que es rápido y económico)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Modelo para embeddings
            self.embedding_model = 'models/gemini-embedding-001'
            
            self.enabled = True
            logger.info("RAG Service inicializado correctamente")
        except Exception as e:
            logger.error(f"Error inicializando RAG Service: {e}")
            self.enabled = False
        
        RAGService._initialized = True
    
    def _clean_html(self, html_content: str) -> str:
        """Limpia HTML y extrae texto plano"""
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, 'html.parser')
        # Eliminar scripts y styles
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        # Limpiar espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _get_embedding(self, text: str) -> List[float]:
        """Genera embedding para un texto usando Gemini"""
        if not self.enabled:
            return []
        try:
            # Truncar texto si es muy largo (límite de tokens)
            max_chars = 8000
            if len(text) > max_chars:
                text = text[:max_chars]
            
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generando embedding: {e}")
            return []
    
    def _get_query_embedding(self, text: str) -> List[float]:
        """Genera embedding para una consulta"""
        if not self.enabled:
            return []
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generando embedding de consulta: {e}")
            return []
    
    def index_page(self, page_id: int, title: str, content: str, sections: List[Dict] = None) -> bool:
        """
        Indexa una página de la Wiki generando y almacenando su embedding
        
        El embedding se guarda en WikiPageEmbedding para fácil migración a pgvector
        """
        if not self.enabled:
            return False
        
        from api.models import WikiPage, WikiPageEmbedding
        
        try:
            # Limpiar contenido HTML
            clean_content = self._clean_html(content)
            
            # Crear documento de texto
            doc_text = f"Título: {title}\n\nContenido: {clean_content}"
            
            # Agregar secciones si existen
            if sections:
                for section in sections:
                    section_text = self._clean_html(section.get('content', ''))
                    if section_text:
                        doc_text += f"\n\nSección {section.get('title', '')}: {section_text}"
            
            # Generar embedding
            embedding = self._get_embedding(doc_text)
            
            if not embedding:
                logger.warning(f"No se pudo generar embedding para página {page_id}")
                return False
            
            # Obtener página
            try:
                page = WikiPage.objects.get(id=page_id)
            except WikiPage.DoesNotExist:
                logger.error(f"Página {page_id} no existe")
                return False
            
            # Guardar o actualizar embedding
            WikiPageEmbedding.objects.update_or_create(
                page=page,
                defaults={
                    'content_text': doc_text[:10000],  # Limitar tamaño
                    'embedding': embedding
                }
            )
            
            logger.info(f"Página '{title}' indexada correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error indexando página: {e}")
            return False
    
    def index_all_pages(self) -> int:
        """Indexa todas las páginas publicadas de la Wiki"""
        from api.models import WikiPage
        
        if not self.enabled:
            return 0
        
        pages = WikiPage.objects.filter(is_published=True).prefetch_related('sections')
        indexed = 0
        
        for page in pages:
            sections_data = [
                {'title': s.title, 'content': s.content}
                for s in page.sections.filter(is_active=True)
            ]
            
            full_content = f"{page.heading or ''}\n{page.description or ''}\n{page.content or ''}"
            
            if self.index_page(page.id, page.title, full_content, sections_data):
                indexed += 1
        
        logger.info(f"Indexadas {indexed} de {pages.count()} páginas")
        return indexed
    
    def search_similar(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Busca documentos similares a la consulta
        
        Usa búsqueda por similitud de coseno.
        Fácil de migrar a pgvector con: 
        SELECT * FROM embeddings ORDER BY embedding <=> query_embedding LIMIT n
        """
        if not self.enabled:
            return []
        
        from api.models import WikiPageEmbedding
        
        try:
            query_embedding = self._get_query_embedding(query)
            
            if not query_embedding:
                return []
            
            # Obtener todos los embeddings (para SQLite)
            # En PostgreSQL con pgvector esto sería una query nativa mucho más eficiente
            embeddings = WikiPageEmbedding.objects.select_related('page').all()
            
            if not embeddings:
                return []
            
            # Calcular similitudes
            results = []
            for emb in embeddings:
                if emb.embedding:
                    similarity = cosine_similarity(query_embedding, emb.embedding)
                    results.append({
                        'content': emb.content_text,
                        'metadata': {
                            'page_id': emb.page.id,
                            'title': emb.page.title,
                            'slug': emb.page.slug
                        },
                        'similarity': similarity
                    })
            
            # Ordenar por similitud (mayor primero) y tomar los top n
            results.sort(key=lambda x: x['similarity'], reverse=True)
            
            return results[:n_results]
            
        except Exception as e:
            logger.error(f"Error buscando documentos similares: {e}")
            return []
    
    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> Dict:
        """
        Procesa un mensaje del usuario y genera una respuesta basada en la Wiki
        
        Args:
            user_message: Pregunta del usuario
            conversation_history: Historial de conversación previo
            
        Returns:
            Dict con la respuesta y metadatos
        """
        if not self.enabled:
            return {
                'response': 'Lo siento, el asistente no está disponible en este momento. Por favor, configura la API key de Gemini.',
                'sources': [],
                'error': True
            }
        
        try:
            # 1. Buscar documentos relevantes
            relevant_docs = self.search_similar(user_message, n_results=3)
            
            # 2. Construir contexto
            context = ""
            sources = []
            
            for doc in relevant_docs:
                # Solo incluir documentos con similitud razonable
                if doc.get('similarity', 0) > 0.3:
                    context += f"\n---\n{doc['content']}\n"
                    if doc['metadata'].get('title'):
                        sources.append({
                            'title': doc['metadata']['title'],
                            'page_id': doc['metadata'].get('page_id'),
                            'slug': doc['metadata'].get('slug')
                        })
            
            # 3. Construir prompt con instrucciones específicas
            system_prompt = """Eres un asistente virtual de la Wiki corporativa. Tu rol es ayudar a los usuarios respondiendo preguntas ÚNICAMENTE basándote en la información proporcionada en el contexto.

REGLAS IMPORTANTES:
1. SOLO responde con información que esté en el contexto proporcionado
2. Si la información no está en el contexto, di claramente "No tengo información sobre eso en la Wiki. ¿Puedo ayudarte con algo más?"
3. Sé conciso y directo en tus respuestas
4. Si es relevante, menciona de qué página proviene la información
5. Responde en el mismo idioma que el usuario
6. Usa formato claro con viñetas o números si hay múltiples puntos
7. NO inventes información que no esté en el contexto
8. Sé amable y profesional"""

            # Construir historial de conversación
            chat_history = ""
            if conversation_history:
                for msg in conversation_history[-5:]:  # Últimos 5 mensajes
                    role = "Usuario" if msg.get('role') == 'user' else "Asistente"
                    chat_history += f"{role}: {msg.get('content', '')}\n"
            
            # Prompt final
            if context:
                full_prompt = f"""{system_prompt}

CONTEXTO DE LA WIKI:
{context}

{f"HISTORIAL DE CONVERSACIÓN:{chr(10)}{chat_history}" if chat_history else ""}

PREGUNTA DEL USUARIO: {user_message}

RESPUESTA (basada SOLO en el contexto de la Wiki):"""
            else:
                full_prompt = f"""{system_prompt}

No se encontró información relevante en la Wiki para esta consulta.

PREGUNTA DEL USUARIO: {user_message}

RESPUESTA:"""

            # 4. Generar respuesta con Gemini
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,  # Baja temperatura para respuestas más precisas
                    max_output_tokens=1024,
                )
            )
            
            response_text = response.text if response.text else "No pude generar una respuesta."
            
            return {
                'response': response_text,
                'sources': sources,
                'error': False
            }
            
        except Exception as e:
            logger.error(f"Error en chat: {e}")
            return {
                'response': f'Lo siento, ocurrió un error al procesar tu pregunta. Por favor, intenta de nuevo.',
                'sources': [],
                'error': True
            }
    
    def get_stats(self) -> Dict:
        """Retorna estadísticas del índice"""
        from api.models import WikiPageEmbedding
        
        try:
            count = WikiPageEmbedding.objects.count()
            return {
                'enabled': self.enabled,
                'indexed_documents': count,
                'model': 'gemini-2.0-flash',
                'embedding_model': getattr(self, 'embedding_model', 'gemini-embedding-001'),
                'database': 'Django ORM (migrable a PostgreSQL + pgvector)'
            }
        except Exception as e:
            return {
                'enabled': self.enabled,
                'indexed_documents': 0,
                'model': 'gemini-2.0-flash',
                'embedding_model': 'gemini-embedding-001',
                'note': 'Configura GEMINI_API_KEY para activar el chat'
            }


# Función para obtener instancia (lazy loading)
_rag_service = None

def get_rag_service():
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service


# Para compatibilidad
rag_service = property(lambda self: get_rag_service())
