from app.utils.router import classify_text
from app.config.constants import ALLOWED_CATEGORIES

def get_shard(doc):
    # Use AI to classify the document topic
    category = classify_text(doc, ALLOWED_CATEGORIES)
    
    # Map category to lower_case_shard name
    shard_name = f"{category.lower()}_shard"
    
    return shard_name
