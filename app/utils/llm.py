from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generate_response(prompt):
    try:
        # Use max_new_tokens to limit only the generated output length
        # Add truncation to ensure we don't exceed GPT-2's 1024 token limit
        result = generator(
            prompt, 
            max_new_tokens=100, 
            truncation=True, 
            pad_token_id=50256,
            clean_up_tokenization_spaces=True
        )
        # Extract only the newly generated text if possible, or clean up the output
        full_text = result[0]["generated_text"]
        # GPT-2 usually repeats the prompt, we can try to strip it
        if full_text.startswith(prompt):
            return full_text[len(prompt):].strip()
        return full_text
    except Exception as e:
        return f"Error generating response: {str(e)}"