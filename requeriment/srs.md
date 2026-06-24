# Software Requirements Specification — Sistema de Monitoreo de Tendencias en Redes Sociales

## Stack Tecnológico
- **Lenguaje**: Python 3.11+
- **API Framework**: FastAPI
- **Dashboard**: Streamlit + Plotly
- **Base de Datos**: PostgreSQL + TimescaleDB (Supabase con MCP)
- **Cache/Streaming**: Redis (Para la etapa #2)
- **Vector Store**: Qdrant, Postgresql con la exterción pg_vector en Supabase
- **NLP**: VADER + HuggingFace Transformers
- **Scheduler**: APScheduler
- **Containerización**: Docker + Docker Compose
- **Fuentes de Datos**: TrendsMCP API, Trend-Pulse (MCP + Python lib), PRAW, YouTube Data API v3, Tweepy

---

## Requerimientos Funcionales

### Módulo 1: Recolección de Datos

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-01 | El sistema debe extraer posts/tendencias cada 10 minutos desde un mínimo de 10 fuentes de datos | Alta |
| RF-02 | El sistema debe soportar las siguientes plataformas: Twitter/X, Facebook, Instagram, LinkedIn, TikTok, YouTube, Pinterest, Reddit, Threads | Alta |
| RF-03 | El sistema debe utilizar TrendsMCP API como fuente primaria unificada para Google Trends, YouTube, TikTok, Reddit, X/Twitter, Amazon, Wikipedia | Alta |
| RF-04 | El sistema debe utilizar Trend-Pulse como fuente secundaria (scraping sin auth) para Weibo, Threads, Pinterest, LinkedIn Trending, Xiaohongshu | Media |
| RF-05 | El sistema debe integrar PRAW para acceso directo a datos de Reddit (posts, comentarios, subreddits) | Alta |
| RF-06 | El sistema debe integrar YouTube Data API v3 para datos de videos trending | Alta |
| RF-07 | El sistema debe integrar Tweepy para acceso directo a Twitter/X API v2 (opcional, si hay presupuesto) | Media |
| RF-08 | El sistema debe implementar un mecanismo de fallback: si una API falla, debe intentar con otra fuente o scraper | Alta |
| RF-09 | El sistema debe manejar rate limits con backoff exponencial y colas de reintentos | Alta |
| RF-10 | El sistema debe almacenar datos crudos (raw) en PostgreSQL antes del procesamiento | Alta |

### Módulo 2: Procesamiento NLP

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-11 | El sistema debe limpiar el texto de los posts (eliminar HTML, URLs, menciones, whitespace) | Alta |
| RF-12 | El sistema debe realizar análisis de sentimiento usando VADER (rápido, rule-based) | Alta |
| RF-13 | El sistema debe realizar análisis de sentimiento profundo usando RoBERTa (HuggingFace) para mayor precisión | Media |
| RF-14 | El sistema debe detectar emociones (joy, anger, sadness, fear, surprise) en los posts | Media |
| RF-15 | El sistema debe extraer keywords relevantes de cada post usando YAKE o TF-IDF | Alta |
| RF-16 | El sistema debe generar embeddings semánticos (BGE-small-en-v1.5, 384-dim) para cada post | Alta |
| RF-17 | El sistema debe almacenar embeddings en Qdrant para búsqueda semántica | Alta |

### Módulo 3: Detección de Tendencias

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-18 | El sistema debe calcular la frecuencia de menciones por keyword/tópico en ventanas de 10 minutos | Alta |
| RF-19 | El sistema debe implementar el algoritmo de Velocidad + Aceleración para detectar tendencias emergentes | Alta |
| RF-20 | El sistema debe clasificar tendencias en ciclos de vida: BASELINE, EMERGING, GROWING, PEAKING, DECLINING, VIRAL | Alta |
| RF-21 | El sistema debe calcular línea base histórica (promedio móvil) para cada keyword | Alta |
| RF-22 | El sistema debe detectar correlación cross-platform (misma tendencia en múltiples redes) | Alta |
| RF-23 | El sistema debe agrupar tendencias similares usando similitud semántica (Qdrant + BGE) | Alta |
| RF-24 | El sistema debe rankear tendencias por score compuesto (velocidad + aceleración + volumen + sentimiento) | Alta |
| RF-25 | El sistema debe detectar anomalías (picos repentinos de menciones) usando métodos estadísticos | Media |

### Módulo 4: API REST

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-26 | El sistema debe exponer endpoint GET `/api/v1/trends` para obtener tendencias actuales | Alta |
| RF-27 | El sistema debe exponer endpoint GET `/api/v1/trends/{platform}` para tendencias por plataforma | Alta |
| RF-28 | El sistema debe exponer endpoint GET `/api/v1/trends/history/{keyword}` para histórico de una tendencia | Alta |
| RF-29 | El sistema debe exponer endpoint POST `/api/v1/refresh` para forzar actualización manual | Alta |
| RF-30 | El sistema debe exponer endpoint GET `/api/v1/health` para monitoreo de salud del sistema | Alta |
| RF-31 | El sistema debe exponer WebSocket `/ws/trends` para push de tendencias en tiempo real | Alta |
| RF-32 | El sistema debe exponer endpoint GET `/api/v1/trends/cross-platform` para tendencias que cruzan múltiples plataformas | Media |
| RF-33 | El sistema debe exponer endpoint GET `/docs` con Swagger UI para documentación interactiva | Media |

### Módulo 5: Dashboard

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-34 | El dashboard debe mostrar un ranking global de tendencias con score compuesto | Alta |
| RF-35 | El dashboard debe permitir filtrar tendencias por plataforma específica | Alta |
| RF-36 | El dashboard debe mostrar la evolución temporal de cada tendencia (gráfico time series) | Alta |
| RF-37 | El dashboard debe mostrar el análisis de sentimiento por tendencia (positivo/negativo/neutral) | Alta |
| RF-38 | El dashboard debe mostrar el ciclo de vida de cada tendencia (emerging, growing, peaking, declining) | Alta |
| RF-39 | El dashboard debe mostrar un mapa de calor cross-platform (qué tendencias están en qué plataformas) | Alta |
| RF-40 | El dashboard debe actualizarse automáticamente cada 10 minutos (o vía WebSocket) | Alta |
| RF-41 | El dashboard debe permitir búsqueda de keywords y exploración de tendencias relacionadas | Media |
| RF-42 | El dashboard debe mostrar alertas de tendencias emergentes (notificaciones visuales) | Media |
| RF-43 | El dashboard debe permitir exportar datos a CSV/JSON | Baja |

---

## Requerimientos No Funcionales

### Rendimiento

| ID | Requerimiento | Prioridad |
|---|---|---|
| RNF-01 | El ciclo completo de recolección + procesamiento no debe exceder 5 minutos (para caber en ventana de 10 min) | Alta |
| RNF-02 | La API REST debe responder en < 500ms para consultas de tendencias actuales | Alta |
| RNF-03 | El dashboard debe cargar en < 3 segundos en navegador moderno | Alta |
| RNF-04 | El sistema debe soportar la recolección concurrente de al menos 10 fuentes simultáneas | Alta |
| RNF-05 | La base de datos debe soportar inserción de ~10,000 registros/día (creciendo con uso) | Media |

### Escalabilidad

| ID | Requerimiento | Prioridad |
|---|---|---|
| RNF-06 | La arquitectura debe permitir agregar nuevas fuentes de datos sin modificar el core del sistema (plugin-based) | Alta |
| RNF-07 | El sistema debe ser horizontalmente escalable (múltiples workers de recolección) | Media |
| RNF-08 | Los componentes deben estar containerizados (Docker) para despliegue reproducible | Alta |

### Disponibilidad y Confiabilidad

| ID | Requerimiento | Prioridad |
|---|---|---|
| RNF-09 | El sistema debe continuar operando si una fuente de datos falla (degradación graceful) | Alta |
| RNF-10 | El scheduler debe registrar logs de todas las ejecuciones (éxito/fallo, duración, volúmenes) | Alta |
| RNF-11 | El sistema debe tener reintentos automáticos para fallos transitorios (máx 3 intentos) | Alta |
| RNF-12 | El sistema debe exponer métricas de salud (Prometheus `/metrics`) | Media |

### Seguridad

| ID | Requerimiento | Prioridad |
|---|---|---|
| RNF-13 | Las API keys y tokens deben manejarse via variables de entorno, no en código fuente | Alta |
| RNF-14 | La API REST debe requerir autenticación (API key o JWT) en producción | Alta |
| RNF-15 | Las conexiones a bases de datos deben usar contraseñas seguras y redes internas (Docker) | Alta |
| RNF-16 | El dashboard no debe exponer API keys ni información sensible en el frontend | Alta |

### Mantenibilidad

| ID | Requerimiento | Prioridad |
|---|---|---|
| RNF-17 | El código debe seguir PEP 8 y usar type hints en Python | Alta |
| RNF-18 | Cada módulo debe tener tests unitarios (pytest, cobertura > 70%) | Alta |
| RNF-19 | Debe existir documentación de setup (README con docker-compose) | Alta |
| RNF-20 | Los logs deben ser estructurados (JSON) para facilitar debugging | Media |

### Legal y Compliance

| ID | Requerimiento | Prioridad |
|---|---|---|
| RNF-21 | El sistema debe cumplir con los términos de servicio de cada plataforma (usar APIs oficiales) | Alta |
| RNF-22 | Los datos recolectados deben ser de acceso público (no autenticado) | Alta |
| RNF-23 | El sistema no debe almacenar información personal identificable (PII) de usuarios | Alta |
| RNF-24 | El sistema debe respetar robots.txt y rate limits de cada plataforma | Alta |
| RNF-25 | Implementar mecanismo de opt-out para fuentes scraping (cumplir con GDPR/CCPA si aplica) | Media |

### Stack Tecnológico (Especificaciones)

| ID | Requerimiento | Prioridad |
|---|---|---|
| RNF-26 | Python 3.11 o superior | Alta |
| RNF-27 | PostgreSQL 16+ con extensión TimescaleDB para time-series | Alta |
| RNF-28 | Redis 7+ para caching y pub/sub | Alta |
| RNF-29 | Qdrant 1.10+ para almacenamiento vectorial | Alta |
| RNF-30 | Docker 24+ y Docker Compose 2+ para orquestación | Alta |
| RNF-31 | FastAPI con soporte async para endpoints | Alta |
| RNF-32 | Streamlit 1.35+ para dashboard interactivo | Alta |
| RNF-33 | APScheduler 3.10+ para tareas periódicas | Alta |
| RNF-34 | httpx + aiohttp para llamadas HTTP asíncronas | Alta |
| RNF-35 | sqlalchemy + asyncpg para ORM asíncrono con PostgreSQL | Alta |
