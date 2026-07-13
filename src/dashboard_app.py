# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os
import json
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

# Import the enrichment function so users can run it from the UI
from pipeline_enriquecido import run_enrichment_pipeline

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Trend Intelligence Hub",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS (Glassmorphism & Clean Typography)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.main-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(90deg, #FF4B4B 0%, #FF8F00 50%, #FF4B4B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 1.1rem;
    color: #888888;
    margin-bottom: 25px;
}

/* Glassmorphism Metric Card */
.metric-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    text-align: center;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #FF4B4B;
    margin-bottom: 2px;
}

.metric-label {
    font-size: 0.9rem;
    font-weight: 400;
    color: #bbbbbb;
}

/* Badges */
.badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
    margin-right: 8px;
    margin-bottom: 8px;
}
.badge-safe { background-color: rgba(46, 204, 113, 0.15); color: #2ecc71; border: 1px solid rgba(46, 204, 113, 0.3); }
.badge-low { background-color: rgba(52, 152, 219, 0.15); color: #3498db; border: 1px solid rgba(52, 152, 219, 0.3); }
.badge-medium { background-color: rgba(241, 196, 15, 0.15); color: #f1c40f; border: 1px solid rgba(241, 196, 15, 0.3); }
.badge-high { background-color: rgba(231, 76, 60, 0.15); color: #e74c3c; border: 1px solid rgba(231, 76, 60, 0.3); }

.badge-vertical { background-color: rgba(155, 89, 182, 0.15); color: #9b59b6; border: 1px solid rgba(155, 89, 182, 0.3); }

/* Playbook Idea Card */
.playbook-card {
    background: rgba(255, 255, 255, 0.02);
    border-left: 4px solid #FF8F00;
    padding: 15px;
    margin-bottom: 12px;
    border-radius: 4px 12px 12px 4px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.playbook-title {
    font-weight: 600;
    color: #FF8F00;
    margin-bottom: 4px;
}

</style>
""", unsafe_allow_html=True)

# Helper function to load data
ENRICHED_CSV = "src/output/all_trending_data_enriched.csv"

@st.cache_data
def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

# Load dataset
df = load_data(ENRICHED_CSV)

# Header Section
st.markdown('<div class="main-title">Trend Intelligence & Social Listening Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Análisis avanzado de tendencias enriquecido con sentimientos e inteligencia de marca para marketing B2B</div>', unsafe_allow_html=True)

if df is None:
    # Empty State - Setup & Run
    st.warning("⚠️ No se encontró el dataset enriquecido (`all_trending_data_enriched.csv`).")
    st.info("Para comenzar, por favor ejecuta el Pipeline de Enriquecimiento que recolectará datos de noticias/Reddit y generará el análisis de NLP y LLM.")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        limit_per_type = st.slider("Tendencias por Fuente", min_value=1, max_value=10, value=3)
        run_btn = st.button("🚀 Ejecutar Pipeline de Enriquecimiento", use_container_width=True)
        
    if run_btn:
        with st.spinner("Ejecutando pipeline (extrayendo contexto de Google News/Reddit y corriendo NLP)... Esto puede tardar 1-2 minutos."):
            try:
                run_enrichment_pipeline(limit_per_type=limit_per_type)
                st.success("¡Pipeline ejecutado con éxito! Recargando datos...")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"Error al ejecutar el pipeline: {e}")
else:
    # Sidebar Filters
    st.sidebar.markdown("### 🎛️ Filtros de Inteligencia")
    
    # 1. Search Query
    search_q = st.sidebar.text_input("🔍 Buscar tendencia o palabra clave", "")
    
    # 2. Source Type Filter
    all_sources = ["Todas"] + list(df['type'].dropna().unique())
    source_filter = st.sidebar.selectbox("📱 Plataforma / Fuente", all_sources)
    
    # 3. Vertical Industry Filter
    # Extract unique verticals from the dataset
    all_verticals = set()
    for v_str in df['target_verticals'].dropna():
        for v in v_str.split(","):
            if v.strip():
                all_verticals.add(v.strip())
    verticals_list = ["Todos"] + sorted(list(all_verticals))
    vertical_filter = st.sidebar.selectbox("💼 Sector Industrial (Marketing Vertical)", verticals_list)

    # 4. Brand Safety Filter
    safety_filter = st.sidebar.multiselect(
        "🛡️ Brand Safety Rating",
        options=["Safe", "Low Risk", "Medium Risk", "High Risk"],
        default=["Safe", "Low Risk", "Medium Risk", "High Risk"]
    )

    # Apply Filters to dataframe
    filtered_df = df.copy()
    
    if search_q:
        filtered_df = filtered_df[filtered_df['TrendingTopic'].str.contains(search_q, case=False, na=False)]
        
    if source_filter != "Todas":
        filtered_df = filtered_df[filtered_df['type'] == source_filter]
        
    if vertical_filter != "Todos":
        filtered_df = filtered_df[filtered_df['target_verticals'].str.contains(vertical_filter, case=False, na=False)]
        
    if safety_filter:
        filtered_df = filtered_df[filtered_df['brand_safety_rating'].isin(safety_filter)]
        
    # Also separate enriched trends (which have summaries/NLP data) from raw ones
    enriched_trends_df = filtered_df[filtered_df['summary'].notna()]
    
    # --- METRICS SECTION ---
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    
    with m_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(filtered_df)}</div>
            <div class="metric-label">Tendencias Totales Encontradas</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(enriched_trends_df)}</div>
            <div class="metric-label">Tendencias con Análisis Premium</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col3:
        avg_sent = filtered_df['sentiment_compound'].mean() if not filtered_df['sentiment_compound'].isna().all() else 0.0
        sentiment_label = "Neutral"
        color = "#f1c40f"
        if avg_sent >= 0.05:
            sentiment_label = "Positivo"
            color = "#2ecc71"
        elif avg_sent <= -0.05:
            sentiment_label = "Negativo"
            color = "#e74c3c"
            
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {color}">{avg_sent:.2f}</div>
            <div class="metric-label">Sentimiento Promedio ({sentiment_label})</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m_col4:
        high_risk_count = len(filtered_df[filtered_df['brand_safety_rating'] == 'High Risk'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: {'#e74c3c' if high_risk_count > 0 else '#2ecc71'}">{high_risk_count}</div>
            <div class="metric-label">Tendencias de Alto Riesgo (PR)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MAIN CONTENT LAYOUT ---
    left_col, right_col = st.columns([2, 3])
    
    with left_col:
        st.markdown("### 📊 Listado de Tendencias")
        
        # Select list of trends
        if filtered_df.empty:
            st.info("No se encontraron tendencias con los filtros aplicados.")
            selected_trend_name = None
        else:
            # We want to highlight enriched ones by prepending a star or label
            trend_options = []
            for idx, row in filtered_df.iterrows():
                prefix = "🌟 [Premium] " if pd.notna(row['summary']) else "📝 [Simple] "
                trend_options.append(f"{prefix}{row['TrendingTopic']} ({row['type']})")
                
            selected_option = st.selectbox(
                "Selecciona una tendencia para desplegar el Análisis Inteligente",
                trend_options,
                index=0
            )
            
            # Extract clean trend name and type
            selected_trend_name = selected_option.split("] ")[1].split(" (")[0]
            selected_type = selected_option.split(" (")[-1][:-1]
            
            selected_row = filtered_df[(filtered_df['TrendingTopic'] == selected_trend_name) & (filtered_df['type'] == selected_type)].iloc[0]

        # General Visualizations in Left Panel
        if not filtered_df.empty:
            st.markdown("#### Distribución de Sentimientos")
            sent_counts = filtered_df['sentiment'].value_counts()
            if not sent_counts.empty:
                fig_pie = px.pie(
                    values=sent_counts.values,
                    names=sent_counts.index,
                    color=sent_counts.index,
                    color_discrete_map={"Positive": "#2ecc71", "Negative": "#e74c3c", "Neutral": "#95a5a6"},
                    hole=0.4,
                    height=260
                )
                fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            st.markdown("#### Clasificación de Brand Safety")
            safety_counts = filtered_df['brand_safety_rating'].value_counts()
            if not safety_counts.empty:
                fig_safety = px.bar(
                    x=safety_counts.index,
                    y=safety_counts.values,
                    color=safety_counts.index,
                    color_discrete_map={"Safe": "#2ecc71", "Low Risk": "#3498db", "Medium Risk": "#f1c40f", "High Risk": "#e74c3c"},
                    labels={"x": "Rating", "y": "Tendencias"},
                    height=220
                )
                fig_safety.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_safety, use_container_width=True)

    with right_col:
        if selected_trend_name:
            st.markdown(f"## {selected_trend_name}")
            st.markdown(f"**Origen:** {selected_row['type']} | **Posición en Ranking:** #{int(selected_row['Top'])} | **Capturado el:** {selected_row['api_timestamp']}")
            
            # Check if this trend is enriched
            if pd.isna(selected_row['summary']):
                st.info("ℹ️ Esta tendencia solo tiene datos crudos de ranking. No se ha corrido el análisis premium de NLP/LLM para ella.")
                
                # Show quick manual analysis button
                manual_btn = st.button(f"⚡ Analizar '{selected_trend_name}' en tiempo real", use_container_width=True)
                if manual_btn:
                    with st.spinner(f"Analizando '{selected_trend_name}'..."):
                        try:
                            # Re-run pipeline forcing just this trend to bypass limits if needed, 
                            # but we can simply run the pipeline for all or filter
                            # In this case we call the pipeline which uses cache or fetches new
                            run_enrichment_pipeline(limit_per_type=10)
                            st.success("¡Análisis completado!")
                            st.cache_data.clear()
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                # --- PREMIUM BRAND INTEL DETAILS ---
                col_i1, col_i2 = st.columns([3, 2])
                
                with col_i1:
                    st.markdown("### 🔍 ¿Qué se está diciendo? (Contexto)")
                    st.write(selected_row['summary'])
                    
                    # Target Verticals Badges
                    st.markdown("#### 💼 Sectores Industriales Clave")
                    verticals = selected_row['target_verticals'].split(",")
                    for v in verticals:
                        if v.strip():
                            st.markdown(f'<span class="badge badge-vertical">{v.strip()}</span>', unsafe_allow_html=True)
                            
                with col_i2:
                    # Brand Safety Box
                    safety = selected_row['brand_safety_rating']
                    badge_class = "badge-safe"
                    if safety == "Low Risk":
                        badge_class = "badge-low"
                    elif safety == "Medium Risk":
                        badge_class = "badge-medium"
                    elif safety == "High Risk":
                        badge_class = "badge-high"
                        
                    st.markdown("### 🛡️ Seguridad de Marca")
                    st.markdown(f'<span class="badge {badge_class}" style="font-size: 1.2rem; padding: 10px 20px;">{safety}</span>', unsafe_allow_html=True)
                    st.write(selected_row['brand_safety_reason'])
                    
                    # Sentiment Mini Gauge
                    compound = selected_row['sentiment_compound']
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = compound,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Sentimiento Polarity (-1 a 1)", 'font': {'size': 14}},
                        gauge = {
                            'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "white"},
                            'bar': {'color': "#FF8F00"},
                            'bgcolor': "rgba(255, 255, 255, 0.05)",
                            'borderwidth': 2,
                            'bordercolor': "rgba(255, 255, 255, 0.1)",
                            'steps': [
                                {'range': [-1, -0.05], 'color': 'rgba(231, 76, 60, 0.15)'},
                                {'range': [-0.05, 0.05], 'color': 'rgba(149, 165, 166, 0.15)'},
                                {'range': [0.05, 1], 'color': 'rgba(46, 204, 113, 0.15)'}
                            ],
                        }
                    ))
                    fig_gauge.update_layout(height=180, margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_gauge, use_container_width=True)

                # --- PLAYBOOK SECTION ---
                st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
                st.markdown("### 💡 Brand Playbook (Sugerencias Creativas de Contenido)")
                st.markdown("Ángulos sugeridos por nuestro motor de IA para que marcas comerciales capitalicen o respondan a la tendencia:")
                
                ideas = selected_row['marketing_ideas'].split(" | ")
                for idx, idea in enumerate(ideas):
                    if idea.strip():
                        # Parse out format or title if any
                        parts = idea.split(":")
                        if len(parts) > 1:
                            title = parts[0].strip()
                            desc = ":".join(parts[1:]).strip()
                        else:
                            title = f"Estrategia de Contenido {idx+1}"
                            desc = idea.strip()
                            
                        st.markdown(f"""
                        <div class="playbook-card">
                            <div class="playbook-title">💡 {title}</div>
                            <div style="font-size: 0.95rem; line-height: 1.4; color: #dddddd;">{desc}</div>
                        </div>
                        """, unsafe_allow_html=True)

                # --- PDF REPORT SIMULATION ---
                st.markdown("<br>", unsafe_allow_html=True)
                pdf_col1, pdf_col2 = st.columns([3, 1])
                with pdf_col1:
                    st.markdown("*(Estudio Ejecutivo valorado en USD $1,500/mes para agencias y marcas comerciales)*")
                with pdf_col2:
                    # Provide simple raw data export for this trend
                    raw_trend_json = {
                        "trend": selected_trend_name,
                        "source": selected_row["type"],
                        "ranking": int(selected_row["Top"]),
                        "timestamp": str(selected_row["api_timestamp"]),
                        "sentiment": selected_row["sentiment"],
                        "sentiment_compound": float(selected_row["sentiment_compound"]),
                        "brand_safety": selected_row["brand_safety_rating"],
                        "brand_safety_reason": selected_row["brand_safety_reason"],
                        "verticals": selected_row["target_verticals"].split(","),
                        "playbook": selected_row["marketing_ideas"].split(" | ")
                    }
                    st.download_button(
                        label="📥 Descargar Reporte JSON",
                        data=json.dumps(raw_trend_json, indent=2, ensure_ascii=False),
                        file_name=f"reporte_{selected_trend_name.replace(' ', '_')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                    
    # Admin Controls at the bottom
    st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    with st.expander("🛠️ Panel de Administración del Sistema"):
        st.write("Configuración del scheduler y actualización de base de datos.")
        adm_col1, adm_col2 = st.columns(2)
        with adm_col1:
            st.write(f"**Ubicación del dataset:** `{ENRICHED_CSV}`")
            st.write(f"**Estado de API Gemini:** {'🟢 Conectado' if os.getenv('GEMINI_API_KEY') else '🔴 Desconectado (Usando Heurísticas)'}")
        with adm_col2:
            st.write(f"**Última actualización de datos:** {filtered_df['record_timestamp'].max() if not filtered_df.empty else 'N/A'}")
            re_run = st.button("🔄 Forzar Recolección y Análisis de Nuevas Tendencias", use_container_width=True)
            if re_run:
                with st.spinner("Conectando con api.trendsmcp.ai y corriendo enriquecimiento..."):
                    try:
                        run_enrichment_pipeline(limit_per_type=3)
                        st.success("¡Actualización exitosa!")
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
