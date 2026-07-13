# Trend Intelligence & Social Listening Hub
### Plataforma Premium de Inteligencia de Tendencias B2B para Marketing y Publicidad

Este proyecto es una plataforma de **Inteligencia de Tendencias** y **Escucha Social** de alto valor para agencias de publicidad, departamentos de mercadeo y marcas comerciales. El sistema extrae tendencias de múltiples redes sociales, recopila su contexto de conversación y genera análisis cualitativos de sentimiento, clasificación de seguridad de marca (*Brand Safety*) e ideas de contenido creativo (*Brand Playbooks*) automáticas utilizando Procesamiento de Lenguaje Natural (NLP) y modelos de lenguaje (LLM).

---

## 🚀 Características Clave

* **Monitoreo Multiplataforma**: Conexión con tendencias en Google Trends, TikTok, YouTube, Reddit, X (Twitter), Wikipedia y Amazon.
* **Contextualización de Tendencias (Zero-Auth)**: Extracción en tiempo real de noticias (Google News RSS) y discusiones en foros (Reddit PRAW) para responder *¿Por qué es tendencia hoy?*.
* **Análisis de Sentimiento Cuantitativo**: Scoring de polaridad (Positivo, Negativo, Neutral) empleando la librería optimizada `VADER`.
* **Motor Cualitativo con Gemini LLM**: Clasificación de **Brand Safety** con semáforo de riesgo, identificación de sectores de marketing de interés y redacción de 3 ideas de contenido creativo listas para usar.
* **Sistema de Contingencia (Fallback)**: Si no se configuran credenciales de Gemini, el analizador degrada elegantemente a un motor heurístico local para que el pipeline no se detenga.
* **Caché Inteligente de Costos**: Almacenamiento local en JSON (`src/output/trend_analysis_cache.json`) que evita re-analizar las mismas tendencias en un intervalo corto de tiempo, ahorrando un 90% en costos de tokens.
* **Dashboard Streamlit Premium**: Interfaz moderna de estilo oscuro, visualizaciones en Plotly, y panel administrativo integrado para correr la actualización de tendencias bajo demanda.

---

## 📁 Estructura del Repositorio

```
├── requirements.txt                   # Dependencias de Python
├── .env.example                       # Plantilla de variables de entorno
├── README.md                          # Guía general de inicio rápido
├── src/
│   ├── context_fetcher.py             # Extractor de noticias y posts en Reddit
│   ├── nlp_analyzer.py                # Pipeline de sentimiento y llamadas Gemini LLM
│   ├── pipeline_enriquecido.py        # Orquestador del pipeline y manejo de caché
│   ├── dashboard_app.py               # Aplicación e interfaz del Dashboard Streamlit
│   └── output/
│       ├── all_trending_data_enriched.csv    # Dataset enriquecido de producción
│       ├── trend_analysis_cache.json  # Archivo de caché de análisis de tendencias
│       └── ...                        # Snapshots históricos en CSV
└── requeriment/
    ├── 20260624_investigación_inicial.md     # Viabilidad y MCP Servers
    ├── 20260624_srs.md                # Requisitos de software (SRS)
    └── 20260712_enfoque_actual.md     # Enfoque comercial, KPIs y fórmulas
```

---

## 🛠️ Instalación y Configuración

### 1. Requisitos Previos
* Python 3.11 o superior instalado.

### 2. Instalación de Dependencias
Clona el repositorio e instala los paquetes necesarios desde la raíz del proyecto:
```bash
pip install -r requirements.txt
```

### 3. Configuración de Variables de Entorno
Copia el archivo de ejemplo para crear tu configuración local:
```bash
cp .env.example .env
```
Abre el archivo `.env` e ingresa tus credenciales:
* `GEMINI_API_KEY`: Requerido para el análisis cualitativo avanzado (resúmenes e ideas).
* `REDDIT_CLIENT_ID` y `REDDIT_CLIENT_SECRET`: Opcionales para buscar discusiones en Reddit (PRAW).

---

## 🖥️ Uso del Sistema

El flujo de trabajo consta de dos pasos principales:

### Paso 1: Ejecutar el Pipeline de Enriquecimiento (NLP + LLM)
Para recolectar tendencias, descargar su contexto e indexar el sentimiento, ejecuta:
```bash
python src/pipeline_enriquecido.py
```
*Este comando consultará los datos, enriquecerá el dataset final y generará/actualizará el archivo de caché en `src/output/`.*

### Paso 2: Iniciar el Dashboard Interactivo
Para explorar de forma visual el Radar de Tendencias, los reportes de sentimiento y los *Brand Playbooks*, ejecuta:
```bash
streamlit run src/dashboard_app.py
```
*Se abrirá automáticamente un navegador con la interfaz premium en **http://localhost:8501**.*

---

## 📊 KPIs de Inteligencia Comercial
El sistema calcula y documenta el impacto de tendencias bajo fórmulas rigurosas de marketing analítico:
* **Velocidad de la Tendencia ($V_t$)**: Mide el incremento del volumen en tiempo real.
* **Aceleración de la Tendencia ($A_t$)**: Mide el factor multiplicador de viralidad.
* **Puntuación de Sentimiento Neto ($NSS$)**: Balance de la percepción del público.
* **Puntuación de Impacto de Tendencia ($TIS$)**: Puntaje de 0 a 100 que pondera volumen, velocidad y visibilidad multiplataforma, penalizado a $0.0$ si la tendencia representa un riesgo reputacional alto (Brand Safety).

*Para ver las ecuaciones matemáticas completas, consulta el documento [20260712_enfoque_actual.md](file:///Users/fabiofernandezaguilar/repo/threading_socialnetworks_post/requeriment/20260712_enfoque_actual.md).*
