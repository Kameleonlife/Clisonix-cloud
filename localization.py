# -*- coding: utf-8 -*-
"""Lightweight localization utilities for Clisonix runtimes."""

from __future__ import annotations

from typing import Dict, Iterable, Mapping, Optional


_DEFAULT_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "status.header": "âœ… System status",
        "status.state.operational": "Operational",
        "status.state.degraded": "Degraded",
        "analysis.header": "ðŸ“Š System analysis ({duration_ms}ms)",
        "analysis.insight.none": "ðŸ’¡ Albi: System is stable.",
        "analysis.insight.some": "ðŸ’¡ Albi: Detected anomalies that need inspection.",
        "health.header": "ðŸ’š System health",
        "insight.cpu_high": "ðŸ’¡ Albi: CPU usage exceeds 85%. Consider reducing load or enabling caching.",
        "insight.ram_high": "ðŸ’¡ Albi: RAM usage is near the limit. Consider optimizing running processes.",
        "insight.disk_high": "ðŸ’¡ Albi: Disk is almost full. Cleanup is recommended.",
        "insight.health_stable": "ðŸ’¡ Albi: Overall health is stable.",
        "insight.good": "ðŸ’¡ Albi: System state looks good with no visible anomalies.",
        "optimization.header": "âš¡ System optimization",
        "optimization.insight": "ðŸ’¡ Albi: Performance improved by {gain:.2f}% after optimization.",
        "backup.header.success": "ðŸ’¾ Backup completed successfully",
        "backup.header.short": "ðŸ’¾ Backup",
        "backup.insight.none": "ðŸ’¡ Albi: No 'data' directory to back up.",
        "backup.insight.success": "ðŸ’¡ Albi: {size_gb} GB saved successfully.",
    },
    "sq": {
        "status.header": "âœ… Statusi i sistemit",
        "status.state.operational": "Operativ",
        "status.state.degraded": "I degraduar",
        "analysis.header": "ðŸ“Š Analiza e sistemit ({duration_ms}ms)",
        "analysis.insight.none": "💡 Albi: Sistemi është i qëndrueshëm.",
        "analysis.insight.some": "💡 Albi: Zbuluar anomali që kërkojnë inspektim.",
        "health.header": "🏥 Shëndeti i sistemit",
        "insight.cpu_high": "💡 Albi: CPU është mbi 85%. Sugjeroj reduktim të ngarkesës ose caching.",
        "insight.ram_high": "💡 Albi: RAM po shkon drejt limitit. Sugjeroj optimizim të proceseve.",
        "insight.disk_high": "💡 Albi: Disku është pothuajse plot. Rekomandohet pastrim.",
        "insight.health_stable": "💡 Albi: Shëndeti i përgjithshëm është i qëndrueshëm.",
        "insight.good": "💡 Albi: Gjendje e mirë, pa anomali të dukshme.",
        "optimization.header": "⚡ Optimizimi i sistemit",
        "optimization.insight": "💡 Albi: Performanca u përmirësua me {gain:.2f}% pas optimizimit.",
        "backup.header.success": "💾 Backup i kryer me sukses",
        "backup.header.short": "ðŸ’¾ Backup",
        "backup.insight.none": "ðŸ’¡ Albi: AsnjÃ« dosje 'data' pÃ«r t'u ruajtur.",
        "backup.insight.success": "ðŸ’¡ Albi: {size_gb} GB tÃ« ruajtura me sukses.",
    },
    "es": {
        "status.header": "âœ… Estado del sistema",
        "status.state.operational": "Operativo",
        "status.state.degraded": "Degradado",
        "analysis.header": "ðŸ“Š AnÃ¡lisis del sistema ({duration_ms}ms)",
        "analysis.insight.none": "ðŸ’¡ Albi: El sistema estÃ¡ estable.",
        "analysis.insight.some": "ðŸ’¡ Albi: Se detectaron anomalÃ­as que requieren revisiÃ³n.",
        "health.header": "ðŸ’š Salud del sistema",
        "insight.cpu_high": "ðŸ’¡ Albi: La CPU supera el 85 %. Reduce la carga o activa cachÃ©.",
        "insight.ram_high": "ðŸ’¡ Albi: La RAM estÃ¡ cerca del lÃ­mite. Optimiza los procesos.",
        "insight.disk_high": "ðŸ’¡ Albi: El disco estÃ¡ casi lleno. Se recomienda limpieza.",
        "insight.health_stable": "ðŸ’¡ Albi: La salud general es estable.",
        "insight.good": "ðŸ’¡ Albi: El estado es bueno, sin anomalÃ­as visibles.",
        "optimization.header": "âš¡ OptimizaciÃ³n del sistema",
        "optimization.insight": "ðŸ’¡ Albi: El rendimiento mejorÃ³ en {gain:.2f}% tras la optimizaciÃ³n.",
        "backup.header.success": "ðŸ’¾ Respaldo completado con Ã©xito",
        "backup.header.short": "ðŸ’¾ Respaldo",
        "backup.insight.none": "ðŸ’¡ Albi: No existe el directorio 'data' para respaldar.",
        "backup.insight.success": "ðŸ’¡ Albi: {size_gb} GB guardados correctamente.",
    },
}


class LocalizationManager:
    """Provides key-based translations with optional string formatting."""

    def __init__(
        self,
        translations: Optional[Mapping[str, Mapping[str, str]]] = None,
        default_language: str = "en",
    ) -> None:
        source = translations if translations is not None else _DEFAULT_TRANSLATIONS
        self._translations: Dict[str, Dict[str, str]] = {
            lang.lower(): dict(values) for lang, values in source.items()
        }
        self.default_language = default_language.lower()

    def available_languages(self) -> Iterable[str]:
        return tuple(sorted(self._translations.keys()))

    def translate(self, key: str, language: Optional[str] = None, **format_kwargs: object) -> str:
        lang = (language or self.default_language).lower()
        template = self._lookup(lang, key)
        if template is None:
            template = self._lookup(self.default_language, key)
        if template is None:
            return key
        if format_kwargs:
            try:
                return template.format(**format_kwargs)
            except Exception:
                return template
        return template

    def add_translations(self, language: str, entries: Mapping[str, str]) -> None:
        lang = language.lower()
        bucket = self._translations.setdefault(lang, {})
        bucket.update(entries)

    def set_default_language(self, language: str) -> None:
        lang = language.lower()
        if lang not in self._translations:
            raise ValueError(f"Unsupported language: {language}")
        self.default_language = lang

    def _lookup(self, language: str, key: str) -> Optional[str]:
        return self._translations.get(language, {}).get(key)

    def clone(self) -> "LocalizationManager":
        return LocalizationManager(self._translations, self.default_language)


DEFAULT_LOCALIZATION = LocalizationManager()

