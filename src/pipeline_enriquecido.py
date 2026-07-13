# -*- coding: utf-8 -*-
import os
import json
import datetime
import pandas as pd
import logging
from dotenv import load_dotenv

# Import our new modules
from context_fetcher import TrendContextFetcher
from nlp_analyzer import TrendNLPAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

CACHE_FILE = "src/output/trend_analysis_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}. Starting fresh.")
    return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save cache: {e}")

def run_enrichment_pipeline(input_csv=None, limit_per_type=3):
    """
    Runs the full enrichment pipeline.
    If input_csv is provided, it loads it instead of calling the TrendsMCP API.
    Limits enrichment to the top `limit_per_type` trends per source type to control API costs/time.
    """
    logger.info("Starting Trend Enrichment Pipeline...")
    
    # 1. Load Data
    if input_csv and os.path.exists(input_csv):
        logger.info(f"Loading base trends from local CSV: {input_csv}")
        df = pd.read_csv(input_csv)
    else:
        # Fallback to loading the existing CSV in output folder
        default_csv = "src/output/20260712_203500_all_trending_data.csv"
        if os.path.exists(default_csv):
            logger.info(f"Input CSV not found/specified. Loading default snapshot: {default_csv}")
            df = pd.read_csv(default_csv)
        else:
            logger.error("No base trends CSV found. Run trendstopic_poc.py first to fetch raw trends.")
            return None

    # 2. Filter top trends to analyze
    # To avoid API overhead, we select the top N trends for each unique 'type'
    logger.info(f"Filtering top {limit_per_type} trends per source type for detailed NLP analysis.")
    df['Top'] = pd.to_numeric(df['Top'], errors='coerce')
    
    # Select trends to enrich
    top_df = df.groupby('type').apply(lambda x: x.nsmallest(limit_per_type, 'Top')).reset_index(drop=True)
    
    # Get unique trend names
    unique_trends = top_df['TrendingTopic'].dropna().unique()
    logger.info(f"Found {len(unique_trends)} unique trends to analyze.")

    # Initialize modules
    fetcher = TrendContextFetcher()
    analyzer = TrendNLPAnalyzer()
    cache = load_cache()

    enriched_data = {}
    
    # 3. Process each trend
    for idx, trend in enumerate(unique_trends):
        logger.info(f"[{idx+1}/{len(unique_trends)}] Processing trend: '{trend}'")
        
        # Check cache first
        if trend in cache:
            logger.info(f"Found cached analysis for '{trend}'")
            enriched_data[trend] = cache[trend]
            continue
            
        # Determine language (if it looks like English/Spanish)
        # For simplicity, we search in English for global sources, Spanish for others.
        lang = "en" if any(x in trend.lower() for x in ["the", "shampoo", "recall", "news", "health"]) else "es"
        
        # Fetch Context
        corpus, raw_sources = fetcher.get_consolidated_corpus(trend, lang=lang)
        
        if not corpus.strip():
            logger.warning(f"No context found for trend '{trend}'. Skipping LLM analysis.")
            # Set default empty analysis
            analysis = analyzer._heuristic_fallback(trend, corpus="", lang=lang)
            sentiment_cat, sentiment_scores = "Neutral", {"compound": 0.0, "pos": 0.0, "neu": 1.0, "neg": 0.0}
        else:
            # Analyze Sentiment
            sentiment_cat, sentiment_scores = analyzer.analyze_sentiment_vader(corpus)
            
            # Analyze using Gemini/LLM
            analysis = analyzer.analyze_trend_llm(trend, corpus, lang=lang)
            
        # Structure the enriched entry
        enriched_entry = {
            "sentiment": sentiment_cat,
            "sentiment_compound": sentiment_scores["compound"],
            "sentiment_pos": sentiment_scores["pos"],
            "sentiment_neu": sentiment_scores["neu"],
            "sentiment_neg": sentiment_scores["neg"],
            "summary": analysis.get("summary", ""),
            "brand_safety_rating": analysis.get("brand_safety_rating", "Safe"),
            "brand_safety_reason": analysis.get("brand_safety_reason", ""),
            "target_verticals": ",".join(analysis.get("target_verticals", [])),
            "marketing_ideas": " | ".join(analysis.get("marketing_ideas", [])),
            "analyzed_at": datetime.datetime.now().isoformat()
        }
        
        # Cache results
        enriched_data[trend] = enriched_entry
        cache[trend] = enriched_entry
        save_cache(cache)

    # 4. Map enriched data back to the DataFrame
    logger.info("Mapping NLP results back to the dataset.")
    
    # We will enrich the original DataFrame, setting NaN for trends that weren't selected
    # This keeps the full dataset intact but adds the premium columns for the top ones.
    for col in ["sentiment", "sentiment_compound", "sentiment_pos", "sentiment_neu", "sentiment_neg", 
                "summary", "brand_safety_rating", "brand_safety_reason", "target_verticals", "marketing_ideas"]:
        df[col] = df['TrendingTopic'].map(lambda x: enriched_data.get(x, {}).get(col, None))
        
    # Save the enriched dataset
    output_path = "src/output/all_trending_data_enriched.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Enriched dataset successfully saved to: {output_path}")
    
    # Also save a copy with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    df.to_csv(f"src/output/{timestamp}_all_trending_data_enriched.csv", index=False)
    
    return df

if __name__ == "__main__":
    # Run the pipeline with the default historical CSV
    run_enrichment_pipeline(limit_per_type=3)
