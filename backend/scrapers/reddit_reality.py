"""
Reddit Reality Scanner - Enhanced Edition
Professional-grade Reddit market intelligence with sentiment analysis
"""

import requests
import re
import json
import time
import random
from typing import Dict, Optional, List, Tuple
from collections import Counter
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class RedditMarketData:
    """Complete market data for a subreddit"""
    subreddit: str
    hiring_posts: int
    for_hire_posts: int
    total_posts: int
    saturation_ratio: float
    activity_score: float
    market_status: str

    # Top Demands
    top_demands: List[Tuple[str, int]]

    # Categories breakdown
    categories: Dict[str, int]

    # Engagement metrics
    avg_upvotes: float
    avg_comments: float

    # Sentiment
    sentiment_score: float  # -1 to 1
    sentiment_label: str  # POSITIVE, NEUTRAL, NEGATIVE

    # Metadata
    scraped_at: datetime = None
    is_estimated: bool = False
    error_message: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "platform": f"r/{self.subreddit}",
            "subreddit": self.subreddit,
            "hiring_posts": self.hiring_posts,
            "for_hire_posts": self.for_hire_posts,
            "total_posts": self.total_posts,
            "saturation_ratio": round(self.saturation_ratio, 2),
            "activity_score": round(self.activity_score, 1),
            "market_status": self.market_status,
            "top_demands": self.top_demands[:20],  # Limit for response size
            "categories": self.categories,
            "avg_upvotes": round(self.avg_upvotes, 1),
            "avg_comments": round(self.avg_comments, 1),
            "sentiment_score": round(self.sentiment_score, 2),
            "sentiment_label": self.sentiment_label,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "is_estimated": self.is_estimated,
            "error": self.error_message
        }


class RedditRealityScanner:
    """
    Enhanced Reddit market intelligence scanner
    Features: sentiment analysis, category classification, engagement tracking
    """

    # User agents for rotation
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]

    # Keywords to ignore in extraction
    IGNORE_WORDS = {
        'hiring', 'looking', 'needed', 'need', 'want', 'seeking',
        'budget', 'usd', 'hourly', 'hour', 'week', 'month',
        'remote', 'onsite', 'full', 'time', 'part', 'contract',
        'the', 'and', 'for', 'with', 'that', 'this', 'have', 'from',
        'your', 'will', 'are', 'our', 'can', 'about', 'work',
        'please', 'apply', 'must', 'experience', 'years', 'help'
    }

    # Category keywords for classification
    CATEGORIES = {
        'development': ['developer', 'programmer', 'coding', 'software', 'frontend', 'backend', 'fullstack', 'web', 'mobile', 'app', 'api', 'database'],
        'design': ['designer', 'design', 'ui', 'ux', 'graphic', 'logo', 'branding', 'illustration', 'figma', 'photoshop'],
        'writing': ['writer', 'writing', 'content', 'copywriter', 'blog', 'article', 'editor', 'editing', 'seo'],
        'video': ['video', 'editing', 'youtube', 'animation', 'motion', 'premiere', 'after effects', 'vfx'],
        'marketing': ['marketing', 'seo', 'social', 'media', 'ads', 'advertising', 'growth', 'email', 'campaign'],
        'data': ['data', 'analyst', 'analytics', 'python', 'machine', 'learning', 'ai', 'statistics'],
        'audio': ['audio', 'music', 'sound', 'podcast', 'voice', 'mixing', 'mastering'],
        'admin': ['virtual', 'assistant', 'admin', 'support', 'customer', 'service', 'data entry']
    }

    # Sentiment words
    POSITIVE_WORDS = {
        'great', 'excellent', 'amazing', 'good', 'best', 'fantastic',
        'awesome', 'perfect', 'wonderful', 'excited', 'opportunity',
        'competitive', 'flexible', 'growth', 'team', 'innovative'
    }

    NEGATIVE_WORDS = {
        'urgent', 'asap', 'cheap', 'low', 'budget', 'tight',
        'difficult', 'challenging', 'complex', 'strict', 'deadline',
        'unpaid', 'exposure', 'equity', 'rev share', 'no pay'
    }

    # Market status thresholds
    STATUS_THRESHOLDS = {
        "GOLDMINE": 2,      # ratio < 2 (more hiring than for hire)
        "HEALTHY": 10,      # ratio < 10
        "SATURATED": 30,    # ratio < 30
        "DEAD": float('inf') # ratio >= 30
    }

    def __init__(self, cache_ttl_seconds: int = 300):
        self.cache = {}
        self.cache_ttl = cache_ttl_seconds
        self.request_count = 0
        self.last_request_time = None

    def _get_headers(self) -> Dict[str, str]:
        """Get randomized request headers"""
        return {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    def _rate_limit(self):
        """Implement rate limiting"""
        if self.last_request_time:
            elapsed = (datetime.utcnow() - self.last_request_time).total_seconds()
            if elapsed < 1.0:  # Reddit is stricter - 1 second between requests
                time.sleep(1.0 - elapsed)
        self.last_request_time = datetime.utcnow()

    def _make_request(self, url: str, max_retries: int = 3) -> Optional[Dict]:
        """Make HTTP request with retry logic"""
        self._rate_limit()

        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url,
                    headers=self._get_headers(),
                    timeout=15
                )
                self.request_count += 1

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    wait_time = 5 * (attempt + 1)
                    print(f"[Reddit] Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"[Reddit] HTTP {response.status_code}")

            except requests.RequestException as e:
                print(f"[Reddit] Request error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))

        return None

    def _extract_keywords(self, title: str) -> List[str]:
        """Extract meaningful keywords from post title"""
        # Remove common prefixes
        title = re.sub(r'^\[(hiring|for hire|for_hire)\]\s*', '', title, flags=re.IGNORECASE)

        # Extract words (4+ characters)
        words = re.findall(r'\b[a-z]{4,}\b', title.lower())

        # Filter out ignore words
        keywords = [w for w in words if w not in self.IGNORE_WORDS]

        return keywords

    def _classify_category(self, text: str) -> str:
        """Classify post into category based on keywords"""
        text_lower = text.lower()

        category_scores = {}
        for category, keywords in self.CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                category_scores[category] = score

        if category_scores:
            return max(category_scores, key=category_scores.get)

        return 'other'

    def _calculate_sentiment(self, text: str) -> Tuple[float, str]:
        """
        Calculate sentiment score from text

        Returns:
            Tuple of (score, label)
            Score: -1 (negative) to 1 (positive)
            Label: NEGATIVE, NEUTRAL, POSITIVE
        """
        text_lower = text.lower()
        words = set(re.findall(r'\b[a-z]+\b', text_lower))

        positive_count = len(words & self.POSITIVE_WORDS)
        negative_count = len(words & self.NEGATIVE_WORDS)
        total = positive_count + negative_count

        if total == 0:
            return 0.0, "NEUTRAL"

        score = (positive_count - negative_count) / total

        if score > 0.2:
            label = "POSITIVE"
        elif score < -0.2:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        return score, label

    def _get_market_status(self, ratio: float) -> str:
        """Determine market status based on saturation ratio"""
        if ratio < self.STATUS_THRESHOLDS["GOLDMINE"]:
            return "GOLDMINE"
        elif ratio < self.STATUS_THRESHOLDS["HEALTHY"]:
            return "HEALTHY"
        elif ratio < self.STATUS_THRESHOLDS["SATURATED"]:
            return "SATURATED"
        else:
            return "DEAD"

    def _calculate_activity_score(self, saturation_ratio: float, total_posts: int) -> float:
        """
        Calculate activity score (0-100)
        Higher score = healthier market
        """
        # Base score from saturation (lower ratio = higher score)
        if saturation_ratio <= 1:
            saturation_score = 100
        elif saturation_ratio <= 5:
            saturation_score = 80 - (saturation_ratio - 1) * 10
        elif saturation_ratio <= 20:
            saturation_score = 40 - (saturation_ratio - 5) * 2
        else:
            saturation_score = max(0, 10 - (saturation_ratio - 20) * 0.5)

        # Volume bonus (more posts = more active market)
        if total_posts >= 100:
            volume_bonus = 10
        elif total_posts >= 50:
            volume_bonus = 5
        else:
            volume_bonus = 0

        return min(100, saturation_score + volume_bonus)

    def _generate_fallback_data(self, subreddit: str) -> RedditMarketData:
        """Generate fallback data when scraping fails"""
        seed = sum(ord(c) for c in subreddit)
        random.seed(seed)

        hiring = random.randint(5, 30)
        for_hire = random.randint(20, 80)
        ratio = for_hire / max(hiring, 1)

        random.seed()

        return RedditMarketData(
            subreddit=subreddit,
            hiring_posts=hiring,
            for_hire_posts=for_hire,
            total_posts=hiring + for_hire,
            saturation_ratio=ratio,
            activity_score=self._calculate_activity_score(ratio, hiring + for_hire),
            market_status=self._get_market_status(ratio),
            top_demands=[("data unavailable", 0)],
            categories={},
            avg_upvotes=0,
            avg_comments=0,
            sentiment_score=0,
            sentiment_label="NEUTRAL",
            scraped_at=datetime.utcnow(),
            is_estimated=True,
            error_message="Fallback data (API unavailable)"
        )

    def get_saturation_metrics(self, subreddit: str = "forhire") -> Dict:
        """
        Get saturation metrics (backward compatible interface)

        Returns:
            Dict with market metrics
        """
        data = self.get_market_data(subreddit)
        result = data.to_dict()

        # Add backward compatible fields
        result["supply_posts"] = data.for_hire_posts
        result["demand_posts"] = data.hiring_posts

        return result

    def get_market_data(self, subreddit: str, limit: int = 100) -> RedditMarketData:
        """
        Get comprehensive market data for a subreddit

        Args:
            subreddit: Subreddit name (without r/)
            limit: Number of posts to analyze

        Returns:
            RedditMarketData with all metrics
        """
        try:
            url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
            data = self._make_request(url)

            if not data:
                return self._generate_fallback_data(subreddit)

            posts = data.get('data', {}).get('children', [])

            if not posts:
                return self._generate_fallback_data(subreddit)

            # Initialize counters
            hiring_count = 0
            for_hire_count = 0
            keywords = []
            categories = Counter()
            sentiment_scores = []
            upvotes = []
            comments = []

            for post in posts:
                post_data = post.get('data', {})
                title = post_data.get('title', '').lower()
                body = post_data.get('selftext', '')

                # Count post types
                if '[hiring]' in title:
                    hiring_count += 1
                    # Extract keywords from hiring posts
                    keywords.extend(self._extract_keywords(title))
                    # Classify category
                    category = self._classify_category(title + ' ' + body)
                    categories[category] += 1
                elif '[for hire]' in title or '[for_hire]' in title:
                    for_hire_count += 1

                # Calculate sentiment
                full_text = title + ' ' + body
                sentiment, _ = self._calculate_sentiment(full_text)
                sentiment_scores.append(sentiment)

                # Track engagement
                upvotes.append(post_data.get('ups', 0))
                comments.append(post_data.get('num_comments', 0))

            # Calculate metrics
            total_posts = hiring_count + for_hire_count
            demand = max(hiring_count, 1)
            ratio = round(for_hire_count / demand, 2)

            # Aggregate keywords
            keyword_counts = Counter(keywords).most_common(50)

            # Calculate averages
            avg_upvotes = sum(upvotes) / len(upvotes) if upvotes else 0
            avg_comments = sum(comments) / len(comments) if comments else 0
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

            # Determine sentiment label
            if avg_sentiment > 0.15:
                sentiment_label = "POSITIVE"
            elif avg_sentiment < -0.15:
                sentiment_label = "NEGATIVE"
            else:
                sentiment_label = "NEUTRAL"

            return RedditMarketData(
                subreddit=subreddit,
                hiring_posts=hiring_count,
                for_hire_posts=for_hire_count,
                total_posts=total_posts,
                saturation_ratio=ratio,
                activity_score=self._calculate_activity_score(ratio, total_posts),
                market_status=self._get_market_status(ratio),
                top_demands=keyword_counts,
                categories=dict(categories),
                avg_upvotes=avg_upvotes,
                avg_comments=avg_comments,
                sentiment_score=avg_sentiment,
                sentiment_label=sentiment_label,
                scraped_at=datetime.utcnow(),
                is_estimated=False
            )

        except Exception as e:
            print(f"[Reddit] Analysis failed for r/{subreddit}: {e}")
            return self._generate_fallback_data(subreddit)

    def batch_analyze(
        self,
        subreddits: List[str],
        delay_between: float = 1.5
    ) -> List[RedditMarketData]:
        """
        Analyze multiple subreddits

        Args:
            subreddits: List of subreddit names
            delay_between: Delay between requests (seconds)

        Returns:
            List of RedditMarketData objects
        """
        results = []

        for subreddit in subreddits:
            data = self.get_market_data(subreddit)
            results.append(data)

            if delay_between > 0:
                time.sleep(delay_between)

        return results

    def get_combined_demands(self, subreddits: List[str]) -> List[Tuple[str, int]]:
        """
        Get combined top demands across multiple subreddits

        Args:
            subreddits: List of subreddit names

        Returns:
            List of (keyword, count) tuples
        """
        all_keywords = Counter()

        for subreddit in subreddits:
            data = self.get_market_data(subreddit)
            for keyword, count in data.top_demands:
                all_keywords[keyword] += count

        return all_keywords.most_common(60)

    def get_stats(self) -> Dict:
        """Get scanner statistics"""
        return {
            "total_requests": self.request_count,
            "cache_ttl_seconds": self.cache_ttl
        }
