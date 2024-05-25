from transformers import pipeline

# Load Llama 3 model from Hugging Face
llama3_model = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B")

# Generate text using the Llama 3 model
prompt = "Once upon a time"
generated_text = llama3_model(prompt, max_length=50, do_sample=True)

# Print the generated text
print(generated_text[0]['generated_text'])


