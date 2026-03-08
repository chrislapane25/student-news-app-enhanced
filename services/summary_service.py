import os
import anthropic

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def summarize_article(text, max_length=150):
    """
    Summarize article text using Claude API
    
    Args:
        text: Article text to summarize
        max_length: Maximum length of summary in words (approx)
    
    Returns:
        Summary string
    """
    if not CLAUDE_API_KEY:
        # Fallback to simple summarization
        return create_simple_summary(text, max_length)
    
    if not text or len(text.strip()) < 50:
        raise ValueError("Text too short to summarize")
    
    try:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"""Please provide a concise summary of the following article in 2-3 sentences. 
Keep it around {max_length} words maximum. Focus on the key points.

Article:
{text}

Summary:"""
                }
            ]
        )
        
        summary = message.content[0].text.strip()
        return summary
        
    except Exception as e:
        # Fallback to simple summarization if Claude API fails
        print(f"Warning: Claude API error, using fallback: {e}")
        return create_simple_summary(text, max_length)

def create_simple_summary(text, max_length=150):
    """
    Simple fallback summarization using sentence extraction
    
    Args:
        text: Text to summarize
        max_length: Maximum length in words
    
    Returns:
        Summary string
    """
    # Split into sentences
    sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    
    if not sentences:
        return text[:200] + "..." if len(text) > 200 else text
    
    # Take first 1-2 sentences as summary
    summary = '. '.join(sentences[:2])
    
    # Truncate to max length if needed
    words = summary.split()
    if len(words) > max_length:
        summary = ' '.join(words[:max_length]) + '...'
    
    return summary + '.' if not summary.endswith('.') else summary
