# analysis/sentiment.py

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes text to find emotional keywords and assign a sentiment score.
    This enables the Director to make motivated creative decisions based on content.
    """
    sentiment_scores = {"intensity": 0, "urgency": 0, "positive": 0, "negative": 0, "energy": 0}
    
    if not text:
        return sentiment_scores
    
    text_lower = text.lower()
    
    # Intensity keywords - trigger aggressive effects
    intensity_words = [
        "crazy", "insane", "unbelievable", "mind-blowing", "epic", "incredible", 
        "amazing", "shocking", "extreme", "wild", "massive", "huge", "enormous"
    ]
    if any(word in text_lower for word in intensity_words):
        sentiment_scores["intensity"] = 1

    # Urgency keywords - trigger fast cuts and transitions
    urgency_words = [
        "now", "hurry", "quick", "right now", "don't wait", "immediately", 
        "fast", "rapid", "urgent", "rush", "suddenly", "breaking"
    ]
    if any(word in text_lower for word in urgency_words):
        sentiment_scores["urgency"] = 1

    # High energy keywords - trigger screen shake and dynamic effects
    energy_words = [
        "explosive", "dynamic", "powerful", "intense", "electric", "energetic",
        "pumped", "excited", "hyped", "fired up", "adrenaline", "action"
    ]
    if any(word in text_lower for word in energy_words):
        sentiment_scores["energy"] = 1

    # Positive keywords - influence color and effect selection
    positive_words = [
        "love", "great", "awesome", "fantastic", "wonderful", "perfect",
        "brilliant", "excellent", "outstanding", "superb", "magnificent"
    ]
    if any(word in text_lower for word in positive_words):
        sentiment_scores["positive"] = 1

    # Negative keywords - may trigger different visual treatments
    negative_words = [
        "terrible", "awful", "horrible", "disaster", "nightmare", "catastrophe",
        "failed", "broken", "destroyed", "ruined", "devastated"
    ]
    if any(word in text_lower for word in negative_words):
        sentiment_scores["negative"] = 1

    return sentiment_scores

def get_creative_intent(sentiment_scores: dict) -> dict:
    """
    Converts sentiment analysis into specific creative directives for the Director.
    """
    creative_intent = {
        "effect_multiplier": 1.0,
        "cut_frequency": 1.0,
        "transition_probability": 0.5,
        "recommended_effects": [],
        "emotional_context": "neutral"
    }
    
    # High intensity content should have more effects
    if sentiment_scores["intensity"]:
        creative_intent["effect_multiplier"] = 1.5
        creative_intent["recommended_effects"].append("zoom_punch")
        creative_intent["emotional_context"] = "intense"
    
    # Urgent content should have faster cuts
    if sentiment_scores["urgency"]:
        creative_intent["cut_frequency"] = 1.8
        creative_intent["transition_probability"] = 0.8
        
    # High energy content should have screen shake
    if sentiment_scores["energy"]:
        creative_intent["recommended_effects"].append("screen_shake")
        creative_intent["effect_multiplier"] *= 1.3
        creative_intent["emotional_context"] = "energetic"
    
    # Positive content might use different visual treatments
    if sentiment_scores["positive"]:
        creative_intent["emotional_context"] = "positive"
        
    # Negative content might require different handling
    if sentiment_scores["negative"]:
        creative_intent["emotional_context"] = "negative"
        creative_intent["recommended_effects"].append("glitch")
    
    return creative_intent