from transformers import pipeline
import logging

# Set up logging to avoid too much noise from transformers
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

# Initialize the zero-shot classification pipeline
# Using a fast, lightweight model
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")

def classify_text(text, candidate_labels, multi_label=False):
    """
    Classifies text into one or more categories using zero-shot classification.
    """
    try:
        # Take a sample if text is too long (BART has a 512 token limit)
        input_text = text[:1000]
        
        result = classifier(input_text, candidate_labels, multi_label=multi_label)
        
        if multi_label:
            # Return labels with confidence > 0.3
            return [label for label, score in zip(result["labels"], result["scores"]) if score > 0.3]
        else:
            # Return the top label
            return result["labels"][0]
            
    except Exception as e:
        print(f"Error in zero-shot classification: {str(e)}")
        return "General"
