# -*- coding: utf-8 -*-
import os
import json
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TrendNLPAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_enabled = False
        
        if self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                # Test initializing the model
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.gemini_enabled = True
                logger.info("Gemini AI API client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}. LLM features will fall back to heuristics.")
        else:
            logger.info("GEMINI_API_KEY missing in environment. Heuristic fallback will be used for summaries.")

    def analyze_sentiment_vader(self, text):
        """
        Uses VADER to return sentiment polarity.
        Returns:
            category: 'Positive', 'Negative', 'Neutral'
            scores: dict with keys 'compound', 'pos', 'neu', 'neg'
        """
        if not text:
            return "Neutral", {"compound": 0.0, "pos": 0.0, "neu": 1.0, "neg": 0.0}
            
        # VADER is optimized for short sentences; for a large corpus, we score paragraph chunks and average them
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        if not paragraphs:
            paragraphs = [text]
            
        compounds = []
        pos_scores = []
        neu_scores = []
        neg_scores = []
        
        for p in paragraphs[:15]: # Cap at 15 paragraphs for performance
            scores = self.vader.polarity_scores(p)
            compounds.append(scores['compound'])
            pos_scores.append(scores['pos'])
            neu_scores.append(scores['neu'])
            neg_scores.append(scores['neg'])
            
        avg_scores = {
            "compound": sum(compounds) / len(compounds) if compounds else 0.0,
            "pos": sum(pos_scores) / len(pos_scores) if pos_scores else 0.0,
            "neu": sum(neu_scores) / len(neu_scores) if neu_scores else 1.0,
            "neg": sum(neg_scores) / len(neg_scores) if neg_scores else 0.0
        }
        
        # Classify based on compound score
        if avg_scores["compound"] >= 0.05:
            category = "Positive"
        elif avg_scores["compound"] <= -0.05:
            category = "Negative"
        else:
            category = "Neutral"
            
        return category, avg_scores

    def analyze_trend_llm(self, trend_name, corpus, lang="es"):
        """
        Queries Gemini API to generate:
        1. Context summary (why is it trending?)
        2. Brand Safety Assessment (Safe, Low, Medium, High Risk) + justification
        3. Marketing Actionability (verticals interested, 3 creative ideas)
        """
        if not self.gemini_enabled or not corpus:
            return self._heuristic_fallback(trend_name, corpus, lang)
            
        prompt = f"""
        Actúa como un Consultor Senior de Marketing y Analista de Social Listening.
        Analiza la siguiente tendencia de internet y el corpus de texto recopilado sobre ella.
        
        Tendencia: "{trend_name}"
        
        Corpus de contexto:
        \"\"\"
        {corpus[:4000]}
        \"\"\"
        
        Genera un análisis en formato JSON estricto con la siguiente estructura exacta:
        {{
            "summary": "Explicación clara en 1 o 2 párrafos de por qué este tema es tendencia hoy y qué es lo principal que se está discutiendo (en español).",
            "brand_safety_rating": "Safe" | "Low Risk" | "Medium Risk" | "High Risk",
            "brand_safety_reason": "Breve explicación de por qué tiene esa clasificación de seguridad de marca (ej. si involucra política, crímenes, estafas, recalls, o si es entretenimiento familiar).",
            "target_verticals": ["Lista", "De", "Sectores", "Ej: Consumo Masivo, Retail, Finanzas, Tecnología, Cuidado Personal"],
            "marketing_ideas": [
                "Idea de contenido 1: específica para esta tendencia, indicando qué formato usar (ej. TikTok, Post, Meme) y el ángulo creativo.",
                "Idea de contenido 2...",
                "Idea de contenido 3..."
            ]
        }}
        
        Responde ÚNICAMENTE con el objeto JSON válido. No agregues texto markdown fuera del JSON.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json", "temperature": 0.2}
            )
            data = json.loads(response.text)
            return data
        except Exception as e:
            logger.error(f"Error calling Gemini API for '{trend_name}': {e}. Falling back to heuristics.")
            return self._heuristic_fallback(trend_name, corpus, lang)

    def _heuristic_fallback(self, trend_name, corpus, lang="es"):
        """
        Fallback logic when LLM fails or is disabled.
        Uses rule-based heuristics to classify safety and generate general templates.
        """
        # 1. Determine safety based on trigger words in the corpus
        corpus_lower = corpus.lower() if corpus else ""
        high_risk_words = ["recall", "fda", "accident", "death", "muerte", "incident", "strike", "crime", "fraud", "scam", "arrest", "investigation", "lawsuit", "court", "outbreak", "parasite"]
        medium_risk_words = ["health", "salud", "clash", "protest", "strike", "huelga", "layoff", "despido", "shutdown", "drop"]
        
        safety = "Safe"
        reason = "No se detectaron palabras clave conflictivas de seguridad de marca."
        
        for w in high_risk_words:
            if w in corpus_lower:
                safety = "High Risk"
                reason = f"Se detectaron términos sensibles de alto riesgo (como '{w}') en el contexto de la tendencia."
                break
                
        if safety == "Safe":
            for w in medium_risk_words:
                if w in corpus_lower:
                    safety = "Medium Risk"
                    reason = f"Se detectaron términos moderadamente sensibles (como '{w}') en el contexto de la tendencia."
                    break
        
        # 2. Extract some basic lines for a summary
        lines = [line.strip() for line in corpus.split("\n") if line.strip() and not line.startswith("[")]
        summary_text = ""
        if lines:
            summary_text = f"La tendencia '{trend_name}' está activa. De acuerdo con las noticias iniciales: " + " ".join(lines[:2])
        else:
            summary_text = f"No se pudo extraer el contexto completo para la tendencia '{trend_name}'. El tema está generando volumen de búsquedas y menciones en múltiples plataformas."
            
        # 3. Choose verticals
        verticals = ["Consumo Masivo", "Medios & Entretenimiento"]
        if "shampoo" in corpus_lower or "cosmetic" in corpus_lower or "skin" in corpus_lower:
            verticals.append("Belleza & Cuidado Personal")
        if "recall" in corpus_lower or "fda" in corpus_lower:
            verticals.append("Legal & RRPP")
        if "game" in corpus_lower or "consol" in corpus_lower or "app" in corpus_lower or "tech" in corpus_lower:
            verticals.append("Tecnología & Videojuegos")
            
        # 4. Generate basic template ideas
        ideas = [
            f"Monitoreo de Marca: Seguir de cerca el desarrollo de '{trend_name}' para evaluar si impacta directamente a nuestra marca o competidores.",
            f"Post Informativo: Crear una infografía informativa aclarando mitos y verdades si es relevante para el sector de la marca.",
            f"Participación en Redes (Trend Hijacking): Si la marca es afín y el riesgo es 'Safe', crear un meme de reacción rápida usando los hashtags de la tendencia."
        ]
        
        return {
            "summary": summary_text,
            "brand_safety_rating": safety,
            "brand_safety_reason": reason,
            "target_verticals": verticals,
            "marketing_ideas": ideas
        }

if __name__ == "__main__":
    # Test execution
    from dotenv import load_dotenv
    load_dotenv()
    
    analyzer = TrendNLPAnalyzer()
    
    # Test sentiment
    sentiment, scores = analyzer.analyze_sentiment_vader("I absolutely love this new shampoo! It makes my hair shine.")
    print("Sentiment:", sentiment, scores)
    
    # Test LLM summary
    test_corpus = "[Google News] Oribe recall: Oribe Hair Care recalls certain aerosol shampoos due to benzene presence. | FDA alert: FDA announces voluntary recall of Oribe Dry Shampoo products."
    llm_analysis = analyzer.analyze_trend_llm("oribe shampoo fda recall", test_corpus)
    print("LLM Analysis JSON:")
    print(json.dumps(llm_analysis, indent=2, ensure_ascii=False))
