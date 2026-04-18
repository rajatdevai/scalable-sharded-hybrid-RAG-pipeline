from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generate_response(prompt):

    result = generator(prompt, max_length=200)
    return result[0]["generated_text"]