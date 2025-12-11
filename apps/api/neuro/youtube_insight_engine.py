class YouTubeInsightEngine:

    def analyze(self, meta: dict) -> dict:
        snippet = meta.get("snippet", {})
        stats = meta.get("statistics", {})
        title = snippet.get("title", "")
        desc = snippet.get("description", "")
        tags = snippet.get("tags", []) or []
        
        # ----------------------------
        # 1. Emotional Tone (from text)
        # ----------------------------
        emotion = self._emotion_from_text(title + " " + desc)

        # ----------------------------
        # 2. Engagement Score
        # ----------------------------
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0)) if "likeCount" in stats else 0
        comments = int(stats.get("commentCount", 0)) if "commentCount" in stats else 0

        engagement = self._engagement(views, likes, comments)

        # ----------------------------
        # 3. Core topics (primitive extraction)
        # ----------------------------
        topics = self._topics(title, desc, tags)

        # ----------------------------
        # 4. Trend Potential
        # ----------------------------
        trend = self._trend_score(engagement, emotion)

        # ----------------------------
        # 5. Target Audience
        # ----------------------------
        audience = self._audience(topics)

        # ----------------------------
        # 6. BrainSync recommendation
        # ----------------------------
        bs_mode = self._brainsync_mode(emotion)

        return {
            "title": title,
            "description": desc,
            "emotion": emotion,
            "topics": topics,
            "engagement_score": engagement,
            "trend": trend,
            "target_audience": audience,
            "recommended_brainsync_mode": bs_mode
        }

    # ============================
    # Helper Methods
    # ============================

    def _emotion_from_text(self, text):
        text = text.lower()
        if any(w in text for w in ["amazing","great","wow","love"]):
            return "positive"
        if any(w in text for w in ["sad","terrible","cry","pain"]):
            return "sad"
        if any(w in text for w in ["angry","mad","fight"]):
            return "angry"
        if any(w in text for w in ["calm","peace","relax"]):
            return "calm"
        return "neutral"

    def _engagement(self, v, l, c):
        if v == 0:
            return 0
        return round(((l + c) / v) * 1000, 2)

    def _topics(self, title, desc, tags):
        keywords = []
        for w in (title + " " + desc).split():
            if len(w) > 5:
                keywords.append(w.lower())
        return list(set(keywords[:10] + tags[:5]))

    def _trend_score(self, engagement, emotion):
        base = engagement
        if emotion == "positive":
            base *= 1.2
        if emotion == "angry":
            base *= 1.4
        if emotion == "sad":
            base *= 0.8
        return round(min(base, 100), 2)

    def _audience(self, topics):
        if any("finance" in t for t in topics):
            return "adults/investors"
        if any("gaming" in t for t in topics):
            return "teens/gamers"
        if any("tutorial" in t for t in topics):
            return "general learners"
        return "general"

    def _brainsync_mode(self, emotion):
        mapping = {
            "positive": "motivation",
            "angry": "recovery",
            "sad": "recovery",
            "calm": "relax",
            "neutral": "focus"
        }
        return mapping.get(emotion, "relax")
