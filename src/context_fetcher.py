# -*- coding: utf-8 -*-
import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TrendContextFetcher:
    def __init__(self):
        # Try to initialize Reddit client if credentials are present
        self.reddit = None
        self.reddit_enabled = False
        
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "trend-listening-agent-v1.0")
        
        if self.reddit_client_id and self.reddit_client_secret:
            try:
                import praw
                self.reddit = praw.Reddit(
                    client_id=self.reddit_client_id,
                    client_secret=self.reddit_client_secret,
                    user_agent=self.reddit_user_agent
                )
                # Quick validation check (read-only)
                self.reddit.read_only = True
                self.reddit_enabled = True
                logger.info("Reddit PRAW client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Reddit PRAW client: {e}. Reddit search will be disabled.")
        else:
            logger.info("Reddit credentials missing in environment. Reddit search is disabled.")

    def fetch_google_news(self, query, lang="es", limit=10):
        """
        Fetches Google News RSS search results for a given query.
        Returns a list of titles and descriptions. No API key required.
        """
        logger.info(f"Fetching Google News RSS for query: '{query}'")
        
        # Configure RSS URL based on language
        if lang == "es":
            url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=es-419&gl=MX&ceid=MX:es-419"
        else:
            url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
            
        results = []
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            
            for item in items[:limit]:
                title = item.find("title").text if item.find("title") is not None else ""
                description = item.find("description").text if item.find("description") is not None else ""
                # Clean simple HTML from description if any
                if description:
                    # Quick tags removal
                    import re
                    description = re.sub('<[^<]+?>', '', description)
                
                results.append({
                    "source": "Google News",
                    "title": title,
                    "text": description
                })
        except Exception as e:
            logger.error(f"Error fetching Google News for '{query}': {e}")
            
        return results

    def fetch_reddit_context(self, query, limit=5):
        """
        Fetches posts and top comments from Reddit using PRAW.
        """
        if not self.reddit_enabled or not self.reddit:
            logger.debug("Reddit fetch skipped (client not enabled).")
            return []
            
        logger.info(f"Fetching Reddit posts for query: '{query}'")
        results = []
        try:
            # Search relevant posts
            submissions = self.reddit.subreddit("all").search(query, sort="relevance", time_filter="week", limit=limit)
            
            for sub in submissions:
                post_content = f"Post Title: {sub.title}\nContent: {sub.selftext[:500]}"
                results.append({
                    "source": f"Reddit - r/{sub.subreddit.display_name}",
                    "title": sub.title,
                    "text": sub.selftext[:1000]
                })
                
                # Fetch top comments
                sub.comments.replace_more(limit=0) # Only top comments, no deep loading
                comments_text = []
                for comment in sub.comments[:5]:
                    comments_text.append(comment.body[:300])
                
                if comments_text:
                    results.append({
                        "source": f"Reddit - r/{sub.subreddit.display_name} (Comments)",
                        "title": f"Comments on: {sub.title[:50]}",
                        "text": " | ".join(comments_text)
                    })
        except Exception as e:
            logger.error(f"Error fetching Reddit context for '{query}': {e}")
            
        return results

    def get_consolidated_corpus(self, query, lang="es"):
        """
        Gathers context from all enabled sources and returns:
        1. A single consolidated text string (corpus)
        2. A list of raw result objects for metadata
        """
        news_data = self.fetch_google_news(query, lang=lang)
        reddit_data = self.fetch_reddit_context(query)
        
        all_data = news_data + reddit_data
        
        # Build clean text corpus
        corpus_parts = []
        for idx, item in enumerate(all_data):
            corpus_parts.append(f"[{item['source']}] {item['title']}: {item['text']}")
            
        consolidated_corpus = "\n\n".join(corpus_parts)
        
        return consolidated_corpus, all_data

if __name__ == "__main__":
    # Test execution
    from dotenv import load_dotenv
    load_dotenv()
    
    fetcher = TrendContextFetcher()
    corpus, raw = fetcher.get_consolidated_corpus("oribe shampoo fda recall", lang="en")
    print(f"--- CORPUS GENERATED (Length: {len(corpus)}) ---")
    print(corpus[:1000])
    print("--- RAW DATA SOURCES COUNT ---")
    print(len(raw))
