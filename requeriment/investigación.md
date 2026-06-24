# Investigación de Factibilidad: Sistema de Extracción y Análisis de Tendencias en Redes Sociales

## 1. Resumen Ejecutivo

Se investigó la factibilidad técnica de construir un sistema que extraiga posts de redes sociales cada 10 minutos, identifique tendencias (trending topics), genere modelos estadísticos/analíticos y presente un dashboard near real-time. El stack objetivo es **Python 3 + tecnologías open source**.

**Conclusión**: FACTIBLE. Existen MCP servers, APIs públicas, librerías Python y repositorios open source que cubren todas las plataformas solicitadas. La combinación **TrendsMCP + Trend-Pulse + FastAPI + Streamlit** permite una POC funcional en semanas.

---

## 2. Cobertura por Plataforma

### 2.1 MCP Servers Disponibles (2026)

La investigación se centró en MCP (Model Context Protocol) servers, que permiten a agentes de IA conectarse con redes sociales de forma estandarizada.

| Plataforma | TrendsMCP | SocialCrawl | CreatorCrawl | SocialFetch | Ayrshare | Postiz |
|---|---|---|---|---|---|---|
| Twitter/X | ✅ Live feeds | ✅ Perfiles, tweets | ✅ Perfil, tweets, transcript | ✅ Posts | ✅ 13+ plataformas | ✅ |
| Facebook | — | ✅ Perfiles, posts, grupos | — | ✅ Posts | ✅ | ✅ |
| Instagram | — | ✅ Perfiles, posts, reels | ✅ Perfiles, posts, reels | ✅ Posts | ✅ | ✅ |
| LinkedIn | — | ✅ Perfiles, company, posts | ✅ Perfil, company, posts | ✅ Posts | ✅ | ✅ |
| TikTok | ✅ Hashtag vol. | ✅ 26 endpoints | ✅ 12 tools | ✅ Posts | ✅ | ✅ |
| YouTube | ✅ Search vol. | ✅ 12 endpoints | ✅ 8 tools | ✅ Posts, transcript | ✅ | ✅ |
| Pinterest | — | ✅ 4 endpoints | — | — | ✅ | ✅ |
| Reddit | ✅ Mention vol. | ✅ 7 endpoints | ✅ Search, subreddit | ✅ Posts | ✅ | ✅ |
| Threads | — | ✅ 5 endpoints | — | ✅ Posts | ✅ | ✅ |
| Bluesky | — | — | — | — | — | ✅ |

### 2.2 MCP Servers Destacados

#### TrendsMCP (trendsmcp.ai) — **RECOMENDADO para POC**
- **Fuentes**: Google Search, YouTube, TikTok, Reddit, Amazon, Wikipedia, News, X/Twitter, npm, Steam, App Store, Spotify, GitHub y más (25+ fuentes)
- **Live feeds**: Google Trends, TikTok Trending Hashtags, YouTube Trending, X/Twitter Trending, Reddit Hot Posts, Wikipedia Trending, etc.
- **Free tier**: 100 requests/mes, sin tarjeta de crédito
- **Python SDK**: `pip install trendsmcp-py` o `tiktok-trends-api`
- **MCP endpoint**: `https://api.trendsmcp.ai/mcp`
- **Repo**: https://github.com/trendsmcp/trends-mcp

#### Trend-Pulse (claude-world/trend-pulse) — **RECOMENDADO para POC**
- **37 fuentes** (20 built-in + 17 plugins)
- **Zero auth** para fuentes built-in (Google Trends, Reddit, Hacker News, Wikipedia, GitHub, etc.)
- **Plugin sources**: YouTube Trending, Threads, X/Twitter, TikTok Trending, Pinterest, LinkedIn Trending, Weibo, Xiaohongshu
- **29 herramientas MCP**: get_trending, search_trends, search_semantic, get_trend_clusters, get_lifecycle_prediction, get_trend_velocity
- **Dashboard web**: Streamlit + FastAPI
- **License**: MIT. **Stars**: 40+
- **Repo**: https://github.com/claude-world/trend-pulse

#### SocialCrawl MCP
- **21 plataformas**, 108 endpoints
- Datos: perfiles, posts, comentarios, trending, analytics
- Requiere API key (pago)

#### CreatorCrawl MCP
- **6 plataformas**: TikTok, Instagram, YouTube, LinkedIn, Twitter/X, Reddit
- **60+ tools** incluyendo trending-feed, popular-creators, popular-hashtags
- Requiere API key

#### Social Fetch MCP
- TikTok, Instagram, YouTube, X/Twitter, Telegram, Facebook, Threads, LinkedIn, Reddit, Spotify
- Hosteado (OAuth), sin API keys en config

### 2.3 Librerías Python Nativas por Plataforma

| Plataforma | Librería | API Oficial | Free Tier |
|---|---|---|---|
| Twitter/X | `tweepy` | Twitter API v2 | Basic ($100/mes) |
| Reddit | `praw` | Reddit API | Gratuito |
| YouTube | `google-api-python-client` | YouTube Data API v3 | 10K unidades/día |
| Facebook/Instagram | `facebook-sdk` | Meta Graph API | Gratuito (con límites) |
| TikTok | `TikTokApi` (community) | TikTok Research API | Limitado |
| LinkedIn | `linkedin-api` | LinkedIn API | Limitado |
| Pinterest | `pinterest-api` | Pinterest API | Gratuito |
| Threads | — | Threads API (Meta) | Gratuito |

---

## 3. Repositorios GitHub Relevantes

### 3.1 Proyectos de Detección de Tendencias

| Proyecto | Stars | Descripción | Stack |
|---|---|---|---|
| **trend-pulse** | ⭐40+ | Agregador de tendencias, 37 fuentes, MCP, dashboard | Python, Streamlit, FastAPI |
| **SocialED** | ⭐597 | 19 algoritmos de detección de eventos sociales | PyTorch, DGL |
| **trends-engine** | — | Detección con velocidad + aceleración, pipeline NLP | Python, Qdrant, LLM |
| **trendingcontent-agent** | ⭐38 | Agente de tendencias + generación de contenido | Python, Hermes/OpenClaw |
| **social-trends-mcp** | — | Trends en X, TikTok, YouTube, Instagram (MCP) | Python, Docker |
| **social-attention-monitor** | ⭐1 | Monitoreo de atención social near real-time | FastAPI, Streamlit, NLP |
| **trendflow** | ⭐9 | Google Trends type-safe queries | Python pandas |
| **veyl.io** | ⭐3 | Inteligencia social Instagram + TikTok | FastAPI, Qdrant, Supabase |

### 3.2 Proyectos de Scraping/APIs

| Proyecto | Stars | Descripción |
|---|---|---|
| **social-media-scraping-apis** | ⭐1109 | APIs de scraping para todas las plataformas |

### 3.3 MCP Servers Open Source

| Proyecto | Plataformas | License |
|---|---|---|
| `trendsmcp/trends-mcp` | 25+ fuentes | MIT |
| `socialcrawl/mcp` | 21 plataformas | — |
| `creatorcrawl/mcp-server` | 6 plataformas | MIT |
| `social-freak-ltd/socialfetch-mcp` | 10 plataformas | MIT |
| `woosal1337/media-mcp` | Twitter/X, YouTube, Instagram | — |
| `upload-post-mcp` | 10+ plataformas | MIT |
| `posteverywhere/mcp` | 8 plataformas | — |
| `social-media-mcp-server` | 6 plataformas (649 tools) | — |

---

## 4. Algoritmos de Detección de Tendencias

### 4.1 Enfoque Velocidad + Aceleración (trends-engine)

El algoritmo más maduro encontrado en open source:

1. **Ventanas de tiempo**: Agregación de menciones por ventana (ej: cada 10 min)
2. **Línea base**: Promedio histórico de menciones para cada keyword/tema
3. **Velocidad**: `(menciones_actuales - linea_base) / linea_base`
4. **Aceleración**: Cambio en velocidad entre ventanas consecutivas
5. **Estados del ciclo de vida**: BASELINE → EMERGING → GROWING → PEAKING → DECLINING → VIRAL

### 4.2 Pipeline NLP (7 etapas)

Identificado en trends-engine y social-attention-monitor:

1. Limpieza de texto (HTML, URLs, menciones, whitespace)
2. Sentiment analysis (VADER + RoBERTa)
3. Extracción de keywords (YAKE, TF-IDF)
4. Reconocimiento de entidades (NER)
5. Asignación de tópicos (keyword matching + embedding similarity)
6. Embeddings (BGE-small-en-v1.5, 384-dim)
7. Indexación vectorial (Qdrant)

### 4.3 SocialED: 19 Algoritmos de Detección de Eventos

Librería académica con implementaciones de GNNs para detección de eventos: EventX, KPGNN, FinEvent, QSGNN, ETGNN, HISEvent, HyperSED, etc.

---

## 5. Stack Tecnológico Recomendado para la POC

### 5.1 Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────┐
│                   Schedule Layer                      │
│          APScheduler / Celery Beat (cada 10 min)     │
├─────────────────────────────────────────────────────┤
│                 Data Collection Layer                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │TrendsMCP │ │Trend-    │ │Librerías │             │
│  │ API      │ │Pulse MCP │ │Nativas   │             │
│  │(25+ src) │ │(37 src)  │ │(praw,    │             │
│  │          │ │          │ │tweepy,   │             │
│  │          │ │          │ │youtube)  │             │
│  └──────────┘ └──────────┘ └──────────┘             │
├─────────────────────────────────────────────────────┤
│                 Processing Layer                      │
│  ┌──────────────────────────────────────────────┐    │
│  │  NLP Pipeline: VADER → Keywords → Topics      │    │
│  │  Trend Detection: Velocity + Acceleration     │    │
│  │  Vector Store: Qdrant (embeddings)             │    │
│  └──────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────┤
│                 Storage Layer                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │PostgreSQL│ │  Redis   │ │  Qdrant  │             │
│  │(datos)   │ │ (cache)  │ │(vectors) │             │
│  └──────────┘ └──────────┘ └──────────┘             │
├─────────────────────────────────────────────────────┤
│                   API Layer                           │
│              FastAPI + WebSockets                     │
├─────────────────────────────────────────────────────┤
│                Dashboard Layer                        │
│     Streamlit + Plotly (+ Grafana opcional)          │
└─────────────────────────────────────────────────────┘
```

### 5.2 Stack Detallado

| Componente | Tecnología | Razón |
|---|---|---|
| **Lenguaje** | Python 3.11+ | Ecosistema NLP/data science |
| **API Framework** | FastAPI | Async, rendimiento, docs automáticas |
| **Dashboard** | Streamlit | Rápido prototipado, interactivo |
| **Base de datos** | PostgreSQL + TimescaleDB | Time-series optimizado |
| **Cache** | Redis | Cache de API, colas, pub/sub |
| **Vector Store** | Qdrant | Búsqueda semántica de tendencias |
| **NLP** | VADER + Transformers (HuggingFace) | Sentiment, emociones, NER |
| **Trend Detection** | Algoritmo Velocidad + Aceleración | trends-engine / custom |
| **Scheduler** | APScheduler | Tareas periódicas ligeras |
| **Streaming** | WebSockets (FastAPI) | Actualizaciones near real-time |
| **Visualización** | Plotly + Streamlit Charts | Charts interactivos |
| **Container** | Docker + Docker Compose | Entorno reproducible |
| **MCP Clients** | `trendsmcp-py`, `trend-pulse` | Fuentes de datos |

### 5.3 APIs de Datos Recomendadas

| Fuente | Método Principal | Costo |
|---|---|---|
| **TrendsMCP** | API REST + MCP (25+ feeds) | Free: 100 req/mes |
| **Trend-Pulse** | Python lib + MCP (37 fuentes) | Gratuito (MIT) |
| **Reddit** | PRAW (API oficial) | Gratuito |
| **YouTube** | YouTube Data API v3 | Gratuito (10K ud/día) |
| **X/Twitter** | Tweepy (API v2) | Basic: $100/mes |
| **Google Trends** | trend-pulse / pytrends | Gratuito |

---

## 6. Roadmap para la POC

### Fase 1: Fundación (Semanas 1-2)
- [x] Investigación completada
- [ ] Configurar entorno Python 3.11+, FastAPI, PostgreSQL, Redis, Qdrant (Docker)
- [ ] Implementar colector TrendsMCP (primer feed: Google Trends)
- [ ] Implementar colector Trend-Pulse (Reddit, Hacker News, YouTube Trending)
- [ ] Pipeline NLP básico (VADER sentiment + keyword extraction)
- [ ] Almacenamiento en PostgreSQL

### Fase 2: Cobertura Multi-Plataforma (Semanas 3-4)
- [ ] Integrar PRAW para Reddit (posts y comentarios)
- [ ] Integrar YouTube Data API v3 (videos trending)
- [ ] Integrar TrendsMCP TikTok, X/Twitter, Amazon, Wikipedia
- [ ] Plugin sources de Trend-Pulse (Threads, LinkedIn, Pinterest)
- [ ] Mecanismo de fallback: si API falla, usar Trend-Pulse scraping

### Fase 3: Detección de Tendencias (Semanas 5-6)
- [ ] Implementar algoritmo Velocidad + Aceleración
- [ ] Ciclo de vida de tendencias (EMERGING → GROWING → PEAKING → DECLINING)
- [ ] Clustering semántico con embeddings (Qdrant + BGE)
- [ ] Correlación cross-platform (misma tendencia en múltiples redes)
- [ ] Optimizar scheduler a 10 minutos (APScheduler)

### Fase 4: Dashboard y API (Semanas 7-8)
- [ ] API REST (FastAPI) para consultar tendencias
- [ ] WebSockets para actualizaciones en vivo
- [ ] Dashboard Streamlit: trending topics globales
- [ ] Dashboard Streamlit: tendencias por plataforma
- [ ] Dashboard Streamlit: evolución temporal (time series)
- [ ] Dashboard Streamlit: sentiment analysis por tendencia
- [ ] Dashboard Streamlit: mapa de calor cross-platform

### Fase 5: Refinamiento (Semanas 9-10)
- [ ] Alertas de tendencias emergentes
- [ ] Exportación de datos (CSV, JSON)
- [ ] Tests y documentación
- [ ] Despliegue Docker Compose completo

---

## 7. Riesgos y Mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| APIs rate limits | Alto | Múltiples fuentes, caching, backoff |
| Costo APIs X/Twitter | Medio | Usar TrendsMCP + Trend-Pulse como fallback |
| Cambios en APIs de plataformas | Alto | Capa de abstracción, monitoreo |
| Volumen de datos | Medio | PostgreSQL + TimescaleDB, particionado |
| Precisión de tendencias | Medio | Múltiples algoritmos, validación cruzada |

---

## 8. Referencias

### MCP Servers
1. TrendsMCP - https://trendsmcp.ai - https://github.com/trendsmcp/trends-mcp
2. Trend-Pulse - https://github.com/claude-world/trend-pulse
3. SocialCrawl MCP - https://github.com/socialcrawl/mcp
4. CreatorCrawl MCP - https://github.com/creatorcrawl/mcp-server
5. Social Fetch MCP - https://github.com/social-freak-ltd/socialfetch-mcp
6. OpenTweet MCP - https://opentweet.io/mcp
7. Ayrshare MCP - https://github.com/vanman2024/ayrshare-mcp
8. Postiz MCP - https://postiz.com/mcp
9. Social Trends MCP - https://github.com/caicai-yao/social-trends-mcp
10. UploadPost MCP - https://github.com/chen-friedman/upload-post-mcp
11. PostEverywhere MCP - https://github.com/posteverywhere/mcp
12. Social Media MCP Server - https://www.npmjs.com/package/@muhammadhamidraza/social-media-mcp-server
13. Media MCP - https://github.com/woosal1337/media-mcp
14. Trendsmcp TikTok - https://github.com/trendsmcp/tiktok-trends-api
15. Trendsmcp Python Client - https://github.com/trendsmcp/trendsmcp-py

### Proyectos Open Source
16. SocialED - https://github.com/RingBDStack/SocialED
17. Trends Engine - https://github.com/sbkriz/trends-engine
18. TrendingContent Agent - https://github.com/gabogabucho/trendingcontent-agent
19. Social Attention Monitor - https://github.com/ignaciolinari/social-attention-monitor
20. TrendFlow - https://github.com/dariomory/trendflow
21. veyl.io - https://github.com/RomeoCavazza/veyl.io
22. Social Media Trend Tracker - https://github.com/AbhayAyare/Social-Media-Trend-Tracker
23. Social Media Scraping APIs - https://github.com/cporter202/social-media-scraping-apis
24. SocioSential - https://github.com/h9zdev/SocioSential
25. TrendPilot - https://github.com/Sastik/trend-pilot
26. ChronoPredict - https://github.com/mwasifanwar/ChronoPredict
27. TrendForge - https://github.com/manmit-s/trend-forge-knowcode

### Librerías Python
28. Tweepy - https://github.com/tweepy/tweepy
29. PRAW - https://github.com/praw-dev/praw
30. VADER Sentiment - https://github.com/cjhutto/vaderSentiment
31. HuggingFace Transformers - https://github.com/huggingface/transformers
32. Qdrant - https://github.com/qdrant/qdrant
33. FastAPI - https://github.com/fastapi/fastapi
34. Streamlit - https://github.com/streamlit/streamlit
35. APScheduler - https://github.com/agronholm/apscheduler

### Artículos y Documentación
36. Best MCP Servers for Social Media 2026 - https://opentweet.io/blog/best-mcp-servers-social-media-2026
37. Trends MCP Documentation - https://trendsmcp.ai/docs
38. Model Context Protocol - https://modelcontextprotocol.io
