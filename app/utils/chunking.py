from app.config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def recursive_character_splitter(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """
    Splits text into chunks of specified size with overlap.
    Simple implementation of recursive character splitting.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - chunk_overlap)
        
        # Prevent infinite loop if overlap >= size
        if chunk_size <= chunk_overlap:
            break
            
    return chunks
