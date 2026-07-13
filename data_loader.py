import os
from datasets import load_dataset

class KnowledgeDataLoader:
    """
    Handles automatic downloading, caching, and preprocessing of the 
    internal knowledge base dataset from Hugging Face.
    """
    def __init__(self, dataset_name: str = "ag_news", cache_dir: str = "./data"):
        self.dataset_name = dataset_name
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def load_or_download(self):
        print(f"Checking/Downloading dataset: {self.dataset_name}...")
        # Using a public QA/Text dataset as a surrogate for an internal dataset
        dataset = load_dataset(self.dataset_name, cache_dir=self.cache_dir)
        return dataset

    def prepare_mock_internal_data(self):
        """
        Generates production-grade structured mock logs matching the 
        customer support scenarios if the remote dataset doesn't contain them.
        """
        return [
            {
                "id": "BUG-8842",
                "title": "V4.2 Sync Tool Connection Pool Exhaustion",
                "type": "Jira Ticket",
                "content": "Engineering identified a bug in the version 4.2 sync tool where the connection pool exhausts during migrations exceeding 50,000 records, triggering a Gateway Timeout (504). Assigned to Sarah Jenkins (Backend Team).",
                "status": "Active"
            },
            {
                "id": "KB-0411",
                "title": "Handling Timeout 504 in High-Volume Migrations",
                "type": "Knowledge Base",
                "content": "Instruct the customer to lower their batch migration size to 10,000 records in their config file. A permanent patch is scheduled for release this Thursday.",
                "status": "Published"
            }
        ]

if __name__ == "__main__":
    loader = KnowledgeDataLoader()
    data = loader.load_or_download()
    print("Dataset ready for model training and retrieval.")