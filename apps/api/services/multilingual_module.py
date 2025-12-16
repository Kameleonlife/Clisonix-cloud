"""
Multilingual Response Module for Curiosity Ocean
Advanced language detection, translation, and cultural adaptation
Supports multiple languages with cultural context awareness
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SupportedLanguage(Enum):
    ALBANIAN = "sq"
    ENGLISH = "en" 
    ITALIAN = "it"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    GREEK = "el"
    TURKISH = "tr"
    SERBIAN = "sr"
    CROATIAN = "hr"
    MACEDONIAN = "mk"
    AUTO = "auto"

@dataclass
class LanguageDetectionResult:
    detected_language: SupportedLanguage
    confidence: float
    cultural_context: Dict[str, str]
    regional_variant: Optional[str] = None

@dataclass
class CulturalContext:
    formal_level: str  # formal, informal, casual
    cultural_references: List[str]
    communication_style: str  # direct, indirect, poetic
    humor_style: str  # dry, playful, philosophical

class MultilingualModule:
    """
    Advanced multilingual processing with cultural awareness
    Handles language detection, translation, and cultural adaptation
    """
    
    def __init__(self):
        # Language detection patterns (simplified but effective)
        self.language_patterns = {
            SupportedLanguage.ALBANIAN: {
                "indicators": ["është", "janë", "që", "për", "me", "në", "nga", "te", "si", "çfarë", "pse", "kur", "ku", "dhe", "ose", "por", "edhe", "gjithashtu", "gjithmonë", "kurrë"],
                "unique_chars": ["ë", "ç", "ï", "ë", "ö", "ü"],
                "grammar_patterns": [r"\b\w+ë\b", r"\b\w+në\b", r"\b\w+it\b"],
                "cultural_markers": ["ballkan", "shqiptar", "tradita", "kultura", "familia", "besa", "mikpritja"]
            },
            SupportedLanguage.ENGLISH: {
                "indicators": ["the", "and", "or", "but", "is", "are", "was", "were", "have", "has", "what", "why", "how", "when", "where", "who", "which", "that", "this", "these", "those"],
                "unique_chars": [],
                "grammar_patterns": [r"\b\w+ing\b", r"\b\w+ed\b", r"\b\w+ly\b"],
                "cultural_markers": ["culture", "tradition", "society", "community", "freedom", "innovation"]
            },
            SupportedLanguage.ITALIAN: {
                "indicators": ["è", "sono", "che", "di", "per", "in", "con", "da", "su", "come", "cosa", "perché", "quando", "dove", "chi", "quale", "questo", "quello", "questi", "quelli"],
                "unique_chars": ["à", "è", "é", "ì", "ò", "ù"],
                "grammar_patterns": [r"\b\w+are\b", r"\b\w+ere\b", r"\b\w+ire\b"],
                "cultural_markers": ["famiglia", "tradizione", "cultura", "arte", "bellezza", "passione"]
            },
            SupportedLanguage.SPANISH: {
                "indicators": ["es", "son", "que", "de", "para", "en", "con", "por", "como", "qué", "por qué", "cuándo", "dónde", "quién", "cuál", "este", "ese", "estos", "esos"],
                "unique_chars": ["ñ", "á", "é", "í", "ó", "ú", "ü"],
                "grammar_patterns": [r"\b\w+ar\b", r"\b\w+er\b", r"\b\w+ir\b"],
                "cultural_markers": ["familia", "tradición", "cultura", "comunidad", "fiesta", "respeto"]
            },
            SupportedLanguage.FRENCH: {
                "indicators": ["est", "sont", "que", "de", "pour", "dans", "avec", "par", "sur", "comme", "quoi", "pourquoi", "quand", "où", "qui", "quel", "ce", "cette", "ces", "ceux"],
                "unique_chars": ["à", "è", "é", "ë", "ç", "ù", "û", "ô", "î", "ï"],
                "grammar_patterns": [r"\b\w+er\b", r"\b\w+ir\b", r"\b\w+re\b"],
                "cultural_markers": ["famille", "tradition", "culture", "art", "beauté", "élégance"]
            },
            SupportedLanguage.GERMAN: {
                "indicators": ["ist", "sind", "dass", "von", "für", "in", "mit", "bei", "auf", "wie", "was", "warum", "wann", "wo", "wer", "welche", "diese", "jene", "alle", "keine"],
                "unique_chars": ["ä", "ö", "ü", "ß"],
                "grammar_patterns": [r"\b\w+en\b", r"\b\w+er\b", r"\b\w+es\b"],
                "cultural_markers": ["familie", "tradition", "kultur", "gemeinschaft", "ordnung", "effizienz"]
            }
        }
        
        # Cultural response templates
        self.cultural_templates = {
            SupportedLanguage.ALBANIAN: {
                "greeting": ["Mirë se erdhe në oqeanin e kureshtjes!", "Gëzuar që po eksploro!"],
                "encouragement": ["Vazhdoni të pyesni!", "Kureshtja është çelësi i dijes!"],
                "wisdom_intro": ["Një mençuri e vjetër thotë:", "Siç thonë të moshuar:"],
                "cultural_connection": ["Në kulturën tonë ballkanike:", "Tradita jonë na mëson:"],
                "excitement": ["Sa interesante!", "Kjo është mahnitëse!", "Fantastike!"],
                "deep_thinking": ["Le të mendojmë thellë...", "Kjo kërkon reflektim..."],
                "chaos_expressions": ["Çmenduri kreative!", "Kaos i bukur!", "Magjia e pakufishme!"],
                "philosophical": ["Filozofikisht...", "Në thellësi...", "Spiritualisht..."]
            },
            SupportedLanguage.ENGLISH: {
                "greeting": ["Welcome to the ocean of curiosity!", "Delighted you're exploring!"],
                "encouragement": ["Keep questioning!", "Curiosity is the key to knowledge!"],
                "wisdom_intro": ["Ancient wisdom says:", "As the wise say:"],
                "cultural_connection": ["In our global culture:", "Humanity teaches us:"],
                "excitement": ["How fascinating!", "This is amazing!", "Incredible!"],
                "deep_thinking": ["Let's think deeply...", "This requires reflection..."],
                "chaos_expressions": ["Creative madness!", "Beautiful chaos!", "Infinite magic!"],
                "philosophical": ["Philosophically...", "In depth...", "Spiritually..."]
            },
            SupportedLanguage.ITALIAN: {
                "greeting": ["Benvenuti nell'oceano della curiosità!", "Che bello esplorare!"],
                "encouragement": ["Continuate a domandare!", "La curiosità è la chiave!"],
                "wisdom_intro": ["La saggezza antica dice:", "Come dicono i saggi:"],
                "cultural_connection": ["Nella nostra cultura:", "La tradizione ci insegna:"],
                "excitement": ["Che interessante!", "Questo è fantastico!", "Incredibile!"],
                "deep_thinking": ["Pensiamo profondamente...", "Questo richiede riflessione..."],
                "chaos_expressions": ["Follia creativa!", "Bel caos!", "Magia infinita!"],
                "philosophical": ["Filosoficamente...", "In profondità...", "Spiritualmente..."]
            }
        }
        
        # Regional variants and cultural nuances
        self.regional_variants = {
            SupportedLanguage.ALBANIAN: {
                "tosk": {"markers": ["këtu", "atje"], "cultural": "southern_albanian"},
                "gheg": {"markers": ["ktu", "atje"], "cultural": "northern_albanian"}
            },
            SupportedLanguage.ENGLISH: {
                "american": {"markers": ["mom", "color", "center"], "cultural": "american"},
                "british": {"markers": ["mum", "colour", "centre"], "cultural": "british"},
                "australian": {"markers": ["mate", "arvo"], "cultural": "australian"}
            }
        }

    def detect_language(self, text: str, user_preference: SupportedLanguage = SupportedLanguage.AUTO) -> LanguageDetectionResult:
        """
        Advanced language detection with cultural context
        """
        if user_preference != SupportedLanguage.AUTO:
            cultural_context = self._analyze_cultural_context(text, user_preference)
            return LanguageDetectionResult(
                detected_language=user_preference,
                confidence=1.0,
                cultural_context=cultural_context,
                regional_variant=self._detect_regional_variant(text, user_preference)
            )
        
        # Score each language
        language_scores = {}
        text_lower = text.lower()
        
        for lang, patterns in self.language_patterns.items():
            score = 0
            
            # Count indicator words
            indicator_matches = sum(1 for word in patterns["indicators"] if word in text_lower)
            score += indicator_matches * 2
            
            # Count unique characters
            char_matches = sum(1 for char in patterns["unique_chars"] if char in text)
            score += char_matches * 1.5
            
            # Check grammar patterns
            grammar_matches = sum(1 for pattern in patterns["grammar_patterns"] 
                                if re.search(pattern, text, re.IGNORECASE))
            score += grammar_matches * 1
            
            # Cultural markers bonus
            cultural_matches = sum(1 for marker in patterns["cultural_markers"] if marker in text_lower)
            score += cultural_matches * 3
            
            language_scores[lang] = score
        
        # Find best match
        if not language_scores or max(language_scores.values()) == 0:
            detected_lang = SupportedLanguage.ENGLISH  # Default fallback
            confidence = 0.5
        else:
            detected_lang = max(language_scores, key=language_scores.get)
            max_score = language_scores[detected_lang]
            total_score = sum(language_scores.values())
            confidence = min(0.95, max_score / max(total_score, 1))
        
        cultural_context = self._analyze_cultural_context(text, detected_lang)
        regional_variant = self._detect_regional_variant(text, detected_lang)
        
        return LanguageDetectionResult(
            detected_language=detected_lang,
            confidence=confidence,
            cultural_context=cultural_context,
            regional_variant=regional_variant
        )

    def _analyze_cultural_context(self, text: str, language: SupportedLanguage) -> Dict[str, str]:
        """Analyze cultural context and communication style"""
        text_lower = text.lower()
        
        # Determine formality level
        formal_indicators = ["ju", "tuaj", "you", "your", "lei", "suo", "usted", "su", "vous", "votre", "sie", "ihr"]
        informal_indicators = ["ti", "tënde", "tu", "tuo", "tú", "te", "du", "dein"]
        
        formal_count = sum(1 for word in formal_indicators if word in text_lower)
        informal_count = sum(1 for word in informal_indicators if word in text_lower) 
        
        if formal_count > informal_count:
            formal_level = "formal"
        elif informal_count > 0:
            formal_level = "informal"
        else:
            formal_level = "neutral"
        
        # Detect communication style
        direct_indicators = ["çfarë", "pse", "si", "what", "why", "how", "cosa", "perché", "come"]
        poetic_indicators = ["bukur", "beautiful", "bello", "hermoso", "beau", "schön"]
        
        direct_count = sum(1 for word in direct_indicators if word in text_lower)
        poetic_count = sum(1 for word in poetic_indicators if word in text_lower)
        
        if poetic_count > 0:
            communication_style = "poetic"
        elif direct_count > 2:
            communication_style = "direct"
        else:
            communication_style = "balanced"
        
        # Detect humor style
        humor_indicators = {
            "philosophical": ["universi", "universe", "universo", "realitet", "reality", "realtà"],
            "playful": ["lojë", "play", "gioco", "juego", "jeu", "spiel"],
            "absurd": ["çmendur", "crazy", "pazzo", "loco", "fou", "verrückt"]
        }
        
        humor_style = "balanced"
        for style, indicators in humor_indicators.items():
            if any(word in text_lower for word in indicators):
                humor_style = style
                break
        
        return {
            "formal_level": formal_level,
            "communication_style": communication_style,
            "humor_style": humor_style,
            "cultural_depth": "medium"  # Could be enhanced with more analysis
        }

    def _detect_regional_variant(self, text: str, language: SupportedLanguage) -> Optional[str]:
        """Detect regional language variants"""
        if language not in self.regional_variants:
            return None
        
        text_lower = text.lower()
        variants = self.regional_variants[language]
        
        for variant, data in variants.items():
            if any(marker in text_lower for marker in data["markers"]):
                return variant
        
        return None

    def adapt_response_culturally(self, response: str, target_language: SupportedLanguage, 
                                cultural_context: Dict[str, str]) -> str:
        """
        Adapt response based on cultural context and language
        """
        if target_language not in self.cultural_templates:
            return response  # No adaptation available
        
        templates = self.cultural_templates[target_language]
        
        # Add cultural greeting if appropriate
        if cultural_context.get("formal_level") == "formal":
            if target_language == SupportedLanguage.ALBANIAN:
                response = "🙏 " + response
            elif target_language == SupportedLanguage.ITALIAN:
                response = "🎭 " + response
        
        # Adjust for communication style
        if cultural_context.get("communication_style") == "poetic":
            # Add more poetic language
            poetic_intro = templates.get("philosophical", [""])[0]
            if poetic_intro:
                response = f"{poetic_intro} {response}"
        
        # Add cultural expressions based on humor style
        humor_style = cultural_context.get("humor_style", "balanced")
        if humor_style == "philosophical":
            wisdom_intro = templates.get("wisdom_intro", [""])[0]
            if wisdom_intro and "WISDOM" in response:
                response = response.replace("✨ OCEAN WISDOM:", f"✨ {wisdom_intro}")
        
        return response

    def get_cultural_encouragement(self, language: SupportedLanguage) -> str:
        """Get culturally appropriate encouragement"""
        if language in self.cultural_templates:
            return self.cultural_templates[language]["encouragement"][0]
        return "Keep exploring!"

    def get_cultural_excitement(self, language: SupportedLanguage, level: str = "normal") -> str:
        """Get culturally appropriate excitement expression"""
        if language not in self.cultural_templates:
            return "Amazing!"
        
        templates = self.cultural_templates[language]
        
        if level == "chaos":
            return templates.get("chaos_expressions", ["Amazing!"])[0]
        elif level == "philosophical":
            return templates.get("philosophical", ["Fascinating!"])[0]
        else:
            return templates.get("excitement", ["Great!"])[0]

    def translate_asi_terms(self, terms: Dict[str, str], target_language: SupportedLanguage) -> Dict[str, str]:
        """Translate ASI-specific terms to target language"""
        
        asi_translations = {
            SupportedLanguage.ALBANIAN: {
                "network_connections": "lidhje rrjeti",
                "knowledge_domains": "domene dijesh", 
                "creativity_index": "indeksi i kreativitetit",
                "imagination_score": "pikët e imagjinatës",
                "infinite_potential": "potencial i pafund",
                "data_streams": "rrjedha të dhënash",
                "pattern_recognition": "njohje modelesh",
                "neural_processing": "procesim neural",
                "deep_analysis": "analizë e thellë",
                "synthesis": "sintezë"
            },
            SupportedLanguage.ITALIAN: {
                "network_connections": "connessioni di rete",
                "knowledge_domains": "domini di conoscenza",
                "creativity_index": "indice di creatività", 
                "imagination_score": "punteggio immaginazione",
                "infinite_potential": "potenziale infinito",
                "data_streams": "flussi di dati",
                "pattern_recognition": "riconoscimento pattern",
                "neural_processing": "elaborazione neurale",
                "deep_analysis": "analisi profonda",
                "synthesis": "sintesi"
            },
            SupportedLanguage.SPANISH: {
                "network_connections": "conexiones de red",
                "knowledge_domains": "dominios de conocimiento",
                "creativity_index": "índice de creatividad",
                "imagination_score": "puntuación imaginación", 
                "infinite_potential": "potencial infinito",
                "data_streams": "flujos de datos",
                "pattern_recognition": "reconocimiento de patrones",
                "neural_processing": "procesamiento neural",
                "deep_analysis": "análisis profundo",
                "synthesis": "síntesis"
            }
        }
        
        if target_language not in asi_translations:
            return terms  # Return original if no translation available
        
        translations = asi_translations[target_language]
        translated_terms = {}
        
        for key, value in terms.items():
            translated_terms[key] = translations.get(key, value)
        
        return translated_terms

# Global multilingual instance
_multilingual_instance = None

def get_multilingual_module() -> MultilingualModule:
    """Get singleton instance of the multilingual module"""
    global _multilingual_instance
    if _multilingual_instance is None:
        _multilingual_instance = MultilingualModule()
    return _multilingual_instance


