import pandas as pd

# Load the CSV data
csv_file_path = 'C:/Users/prash/Desktop/shawn/ingredient-vetting-tool-main/ingredient-vetting-tool-main/dataset_new.csv'  # Path to your CSV file
df = pd.read_csv(csv_file_path)

# Check the data structure
print(df.head())

# Assuming the CSV has columns: 'id', 'name', 'description'
# Preprocess the 'description' field (lowercase, clean if necessary)
df['description'] = df['description'].apply(lambda x: x.lower())


from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.model_selection import train_test_split
import torch

# Load the T5 tokenizer and model
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

# Combine chemical names with their descriptions for the summarization task
df['input_text'] = 'summarize: ' + df['name'] + ' ' + df['description']

# Split the data into training and test sets
train_texts, test_texts = train_test_split(df['input_text'], test_size=0.2)

# Tokenize the input text for training
train_encodings = tokenizer(train_texts.tolist(), truncation=True, padding=True, max_length=512)
test_encodings = tokenizer(test_texts.tolist(), truncation=True, padding=True, max_length=512)

# Prepare PyTorch datasets
class ChemicalDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __len__(self):
        return len(self.encodings['input_ids'])

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

train_dataset = ChemicalDataset(train_encodings)
test_dataset = ChemicalDataset(test_encodings)

# Train the model using Hugging Face's Trainer API
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir='./results',
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Train the model
trainer.train()


# Save the trained model and tokenizer
model.save_pretrained('./trained_model')
tokenizer.save_pretrained('./trained_model')


# Load the trained model
from transformers import T5Tokenizer, T5ForConditionalGeneration

model = T5ForConditionalGeneration.from_pretrained('./trained_model')
tokenizer = T5Tokenizer.from_pretrained('./trained_model')

# Function to summarize chemical descriptions dynamically
def summarize_chemicals_by_id(chemical_ids, df, model, tokenizer):
    summaries = []
    
    for chemical_id in chemical_ids:
        # Look up the chemical by ID in the dataframe
        chemical_data = df[df['id'] == chemical_id]
        if not chemical_data.empty:
            input_text = 'summarize: ' + chemical_data['name'].values[0] + ' ' + chemical_data['description'].values[0]
            
            # Tokenize the input text
            input_encodings = tokenizer(input_text, return_tensors='pt', truncation=True, padding=True)
            
            # Generate the summary
            summary_ids = model.generate(input_encodings['input_ids'])
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)
        else:
            summaries.append(f"Chemical with ID {chemical_id} not found.")
    
    return summaries

# Example usage
chemical_ids = [1, 2, 3]  # List of chemical IDs
summaries = summarize_chemicals_by_id(chemical_ids, df, model, tokenizer)
print(summaries)


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define the input schema
class ChemicalRequest(BaseModel):
    chemical_ids: list

# Endpoint for summarizing chemicals
@app.post("/summarize/")
def summarize_chemicals(request: ChemicalRequest):
    summaries = summarize_chemicals_by_id(request.chemical_ids, df, model, tokenizer)
    return {"summaries": summaries}

# Run with `uvicorn app:app --reload`
