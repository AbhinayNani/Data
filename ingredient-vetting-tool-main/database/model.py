import pandas as pd

# Load the dataset from CSV
csv_file_path = './dataset_new.csv'  # Path to your CSV file
df = pd.read_csv(csv_file_path)

# Check the structure of the dataset
print(df.head())

# Dataset structure should be:
# id   name         description
# 1    Chemical A   "Chemical A is a preservative that may cause irritation."
# 2    Chemical B   "Chemical B is used as a fragrance and is generally safe."

# Combine 'name' and 'description' for training input
df['input_text'] = df['name'] + ": " + df['description']



from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.model_selection import train_test_split
import torch

# Load the pre-trained T5 tokenizer and model
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

# Split data into training and testing
train_texts, test_texts = train_test_split(df['input_text'].tolist(), test_size=0.2)

# Tokenize the input text
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=512)

# Prepare the dataset for PyTorch
class ChemicalDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __len__(self):
        return len(self.encodings['input_ids'])

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

train_dataset = ChemicalDataset(train_encodings)
test_dataset = ChemicalDataset(test_encodings)

# Fine-tune the model using Hugging Face's Trainer
from transformers import Trainer, TrainingArguments

# Set training arguments
training_args = TrainingArguments(
    output_dir='./results',            # Output directory for checkpoints
    per_device_train_batch_size=8,     # Batch size for training
    per_device_eval_batch_size=8,      # Batch size for evaluation
    num_train_epochs=3,                # Number of training epochs
    logging_dir='./logs',              # Logging directory
)

# Set up the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Train the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./trained_model")
tokenizer.save_pretrained("./trained_model")

# Load the saved model and tokenizer
from transformers import T5Tokenizer, T5ForConditionalGeneration

model = T5ForConditionalGeneration.from_pretrained('./trained_model')
tokenizer = T5Tokenizer.from_pretrained('./trained_model')

# Function to generate summaries for new chemicals
def summarize_chemicals(chemical_list):
    input_texts = [chemical for chemical in chemical_list]  # Already concatenated name + description
    input_encodings = tokenizer(input_texts, return_tensors='pt', padding=True, truncation=True)
    
    # Generate summaries
    summaries = model.generate(input_encodings['input_ids'])
    
    # Decode the summaries
    decoded_summaries = [tokenizer.decode(summary, skip_special_tokens=True) for summary in summaries]
    
    return decoded_summaries

# Example usage with new chemicals (combination of name and description)
new_chemicals = [
    "Chemical A: A preservative that may cause skin irritation.",
    "Chemical B: A fragrance with a mild, non-irritating scent."
]

summaries = summarize_chemicals(new_chemicals)
print(summaries)


from fastapi import FastAPI
from transformers import T5Tokenizer, T5ForConditionalGeneration

app = FastAPI()

# Load the trained model and tokenizer once
model = T5ForConditionalGeneration.from_pretrained('./trained_model')
tokenizer = T5Tokenizer.from_pretrained('./trained_model')

@app.post("/summarize/")
async def summarize_chemicals(chemical_list: list):
    input_texts = [chemical for chemical in chemical_list]
    input_encodings = tokenizer(input_texts, return_tensors='pt', padding=True, truncation=True)

    # Generate summaries
    summaries = model.generate(input_encodings['input_ids'])
    decoded_summaries = [tokenizer.decode(summary, skip_special_tokens=True) for summary in summaries]

    return {"summaries": decoded_summaries}

# Run the API
# Run with: uvicorn myfile:app --reload




# Function to summarize a list of chemicals
def summarize_chemicals(tfidf_vectorizer, tfidf_matrix, chemical_data, chemical_names):
    summaries = []
    for chemical_name in chemical_names:
        chemical_row = chemical_data[chemical_data['name'] == chemical_name]
        if not chemical_row.empty:
            # Compute similarity between the chemical's description and the TF-IDF matrix
            idx = chemical_row.index[0]
            cosine_similarities = cosine_similarity(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()
            related_docs_indices = cosine_similarities.argsort()[:-5:-1] # Get top 5 similar descriptions
            
            # Generate summary (here we just concatenate the top related descriptions as an example)
            summary = f"{chemical_name}: "
            for i in related_docs_indices:
                summary += chemical_data.iloc[i]['description'] + " "
            summaries.append(summary.strip())
        else:
            summaries.append(f"{chemical_name}: Information not available in the model.")
    return "\n".join(summaries)

# Example usage
csv_file_path = './dataset_new.csv'  # Path to your CSV file
chemical_data = load_chemical_data(csv_file_path)
tfidf_vectorizer, tfidf_matrix = train_summarizer_model(chemical_data)

# Example user input of chemical names
user_provided_chemicals = ["african butter", "agarose", "aka2"]

# Generate and print summaries
print(summarize_chemicals(tfidf_vectorizer, tfidf_matrix, chemical_data, user_provided_chemicals))
