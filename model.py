import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import Dataset

class FineTuner:
    """
    Encapsulates the Hugging Face model loading, inference, and fine-tuning framework
    tailored for production-grade domain adaptation.
    """
    def __init__(self, model_name: str = "gpt2"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def fine_tune(self, raw_data: list, output_dir: str = "./model_output"):
        """
        Executes a supervised fine-tuning loop on the internal knowledge base text data.
        """
        texts = [f"Ticket: {d['title']} \nContent: {d['content']}" for d in raw_data]
        dataset = Dataset.from_dict({"text": texts})

        def tokenize_function(examples):
            return self.tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

        tokenized_dataset = dataset.map(tokenize_function, batched=True)

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=2,
            save_steps=10,
            save_total_limit=1,
            logging_steps=1,
            learning_rate=5e-5,
            weight_decay=0.01,
            fp16=torch.cuda.is_available()
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset
        )
        trainer.train()
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        print("Model training successfully completed.")

    def generate_response(self, prompt: str) -> str:
        """
        Standard generative fallback generation directly using the model pipeline.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=100, 
                pad_token_id=self.tokenizer.eos_token_id
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)