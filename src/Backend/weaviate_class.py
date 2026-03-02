import weaviate
from Attack_dataset.load_attack import load_attack_data_bert, load_attack_data_openai
from CWE_dataset.load_cwe import load_cwe_data_bert, load_cwe_data_openai
from CWE_dataset.load_cwe import load_cwe_data_gpt_oss,load_cwe_data_baai,load_cwe_data_e5,load_cwe_data_labse
from Attack_dataset.load_attack import load_attack_data_gpt_oss,load_attack_data_baai,load_attack_data_e5,load_attack_data_labse
import weaviate
import json
import os       
class WeaviateClass:
    def __init__(self):
        # Initialize Weaviate client
        self.WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        self.client = weaviate.Client(self.WEAVIATE_URL,startup_period=20)

        print(f"Connected to Weaviate at {self.WEAVIATE_URL}", flush=True)
        self.wipe_all_data()
        self.store_bert()
        self.weaviateModelStatus = "BERT"
    def store_data(self, attack_data, attack_embeddings, cwe_data, cwe_embeddings ):
        # Load data and embeddings
         
        # Step 1: Set up Weaviate schemas if they don't exist
        existing_classes = self.client.schema.get()

        if not any(cls['class'] == 'Attack_Entry' for cls in existing_classes['classes']):
            attack_schema = {
                "class": "Attack_Entry",
                "description": "A class to store attack entries with vectorized embeddings",
                "properties": [
                    {"name": "attackID", "dataType": ["string"], "description": "Unique identifier for the attack pattern"},
                    {"name": "type", "dataType": ["string"], "description": "Type of the attack"},
                    {"name": "name", "dataType": ["string"], "description": "Name of the attack"},
                    {"name": "description", "dataType": ["text"], "description": "Detailed description of the attack"}
                ],
                "vectorizer": "none"
            }
            self.client.schema.create_class(attack_schema)

        if not any(cls['class'] == 'CWE_Entry' for cls in existing_classes['classes']):
            cwe_schema = {
                "class": "CWE_Entry",
                "description": "A class to store CWE entries with vectorized embeddings",
                "properties": [
                    {"name": "cweID", "dataType": ["string"], "description": "CWE ID"},
                    {"name": "name", "dataType": ["string"], "description": "CWE Name"},
                    {"name": "description", "dataType": ["text"], "description": "CWE Description"},
                    {"name": "extendedDescription", "dataType": ["text"], "description": "CWE Extended Description"}
                ],
                "vectorizer": "none"
            }
            self.client.schema.create_class(cwe_schema)

        # Add data to Weaviate
        with self.client.batch as batch:
            batch.batch_size = 100  # Adjust as needed
            for entry, embedding in zip(attack_data, attack_embeddings):
                batch.add_data_object(entry, "Attack_Entry", vector=embedding)

            for entry, embedding in zip(cwe_data, cwe_embeddings):
                batch.add_data_object(entry, "CWE_Entry", vector=embedding)

        print("BERT (Attack and CWE) data stored in Weaviate. from mosified class",flush=True)
        
       
    def store_bert(self):
        # Load data and embeddings
        attack_data, attack_embeddings = load_attack_data_bert()
        cwe_data, cwe_embeddings = load_cwe_data_bert()
        self.store_data(attack_data, attack_embeddings , cwe_data, cwe_embeddings)
            # Step 1: Set up Weaviate schemas if they don't exist
            # existing_classes = self.client.schema.get()

            # if not any(cls['class'] == 'Attack_Entry' for cls in existing_classes['classes']):
            #     attack_schema = {
            #         "class": "Attack_Entry",
            #         "description": "A class to store attack entries with vectorized embeddings",
            #         "properties": [
            #             {"name": "attackID", "dataType": ["string"], "description": "Unique identifier for the attack pattern"},
            #             {"name": "type", "dataType": ["string"], "description": "Type of the attack"},
            #             {"name": "name", "dataType": ["string"], "description": "Name of the attack"},
            #             {"name": "description", "dataType": ["text"], "description": "Detailed description of the attack"}
            #         ],
            #         "vectorizer": "none"
            #     }
            #     self.client.schema.create_class(attack_schema)

            # if not any(cls['class'] == 'CWE_Entry' for cls in existing_classes['classes']):
            #     cwe_schema = {
            #         "class": "CWE_Entry",
            #         "description": "A class to store CWE entries with vectorized embeddings",
            #         "properties": [
            #             {"name": "cweID", "dataType": ["string"], "description": "CWE ID"},
            #             {"name": "name", "dataType": ["string"], "description": "CWE Name"},
            #             {"name": "description", "dataType": ["text"], "description": "CWE Description"},
            #             {"name": "extendedDescription", "dataType": ["text"], "description": "CWE Extended Description"}
            #         ],
            #         "vectorizer": "none"
            #     }
            #     self.client.schema.create_class(cwe_schema)

            # # Add data to Weaviate
            # with self.client.batch as batch:
            #     batch.batch_size = 100  # Adjust as needed
            #     for entry, embedding in zip(attack_data, attack_embeddings):
            #         batch.add_data_object(entry, "Attack_Entry", vector=embedding)

            #     for entry, embedding in zip(cwe_data, cwe_embeddings):
            #         batch.add_data_object(entry, "CWE_Entry", vector=embedding)

            # print("BERT (Attack and CWE) data stored in Weaviate.") 
            #    
    def store_baai(self):

        # Load data and embeddings
        attack_data, attack_embeddings = load_attack_data_baai()
        cwe_data, cwe_embeddings = load_cwe_data_baai()
        self.store_data(attack_data, attack_embeddings , cwe_data, cwe_embeddings)
    def store_e5(self):

        # Load data and embeddings
        attack_data, attack_embeddings = load_attack_data_e5()
        cwe_data, cwe_embeddings = load_cwe_data_e5()
        self.store_data(attack_data, attack_embeddings , cwe_data, cwe_embeddings)
    def store_labse(self):

        # Load data and embeddings
        attack_data, attack_embeddings = load_attack_data_labse()
        cwe_data, cwe_embeddings = load_cwe_data_labse()
        self.store_data(attack_data, attack_embeddings , cwe_data, cwe_embeddings)

   
    def store_gpt_oss(self):
        # Load data and embeddings
        attack_data, attack_embeddings = load_attack_data_gpt_oss()
        cwe_data, cwe_embeddings = load_cwe_data_gpt_oss()
        self.store_data(attack_data, attack_embeddings , cwe_data, cwe_embeddings)
    
   

    
    def store_openai(self):
        cwe_data = load_cwe_data_openai()
        attack_data = load_attack_data_openai()
        
        # Step 1: Create Weaviate schemas if they do not exist
        existing_classes = self.client.schema.get() or {"classes": []}
        if not any(cls['class'] == 'CWE_Entry' for cls in existing_classes['classes']):
            cwe_schema = {
                "class": "CWE_Entry",
                "description": "Schema to store CWE entries with embeddings",
                "properties": [
                    {"name": "cweID", "dataType": ["string"], "description": "CWE ID of the entry"},
                    {"name": "name", "dataType": ["string"], "description": "Name of the CWE entry"},
                    {"name": "description", "dataType": ["text"], "description": "Detailed description of the CWE"},
                    {"name": "extendedDescription", "dataType": ["text"], "description": "Extended description of the CWE"}
                ],
                "vectorizer": "none"
            }
            self.client.schema.create_class(cwe_schema)
        else:
            print("CWE_Entry schema already exists, skipping creation.")

        if not any(cls['class'] == 'Attack_Entry' for cls in existing_classes['classes']):
            attack_schema = {
                "class": "Attack_Entry",
                "description": "Schema to store Attack entries with embeddings",
                "properties": [
                    {"name": "attackID", "dataType": ["string"], "description": "Unique identifier for the Attack entry"},
                    {"name": "type", "dataType": ["string"], "description": "Type of the attack entry"},
                    {"name": "name", "dataType": ["string"], "description": "Name of the attack entry"},
                    {"name": "description", "dataType": ["text"], "description": "Detailed description of the attack"}
                ],
                "vectorizer": "none"
            }
            self.client.schema.create_class(attack_schema)
            print("Attack_Entry schema created.")
        else:
            print("Attack_Entry schema already exists, skipping creation.")

        # Add data to Weaviate
        with self.client.batch as batch:
            batch.batch_size = 100
            # Attack data
            for entry in attack_data:
                attack_entry = {
                    "attackID": entry["id"],
                    "type": entry["type"],
                    "name": entry["name"],
                    "description": entry["description"]
                }
                batch.add_data_object(attack_entry, "Attack_Entry", vector=entry["embedding"])

            # CWE data
            for entry in cwe_data:
                cwe_entry = {
                    "cweID": entry["cweID"],
                    "name": entry["name"],
                    "description": entry["description"],
                    "extendedDescription": entry.get("extendedDescription", "")
                }
                batch.add_data_object(cwe_entry, "CWE_Entry", vector=entry["embedding"])

        print("OPENAI (Attack and CWE) data stored in Weaviate.")
        
    def cwe_bert_query(self, query_embedding):
        result = self.client.query.get("CWE_Entry", ["cweID", "name", "description", "extendedDescription"]).with_additional(["distance"]).with_near_vector({"vector": query_embedding.tolist()}).with_limit(920).do()
        print("\n=== DEBUG: Raw Weaviate Results ===")
        #print(result,flush=True)
        return result

    def attack_bert_query(self, query_embedding):
        result = self.client.query.get("Attack_Entry", ["attackID", "type", "name", "description"]).with_additional(["distance"]).with_near_vector({"vector": query_embedding.tolist()}).with_limit(5).do()
        print("\n=== DEBUG: Raw Weaviate Results ===")
        # print(result)
        return result

    def cwe_openai_query(self, query_embedding):
        return self.client.query.get("CWE_Entry", ["cweID", "name", "description", "extendedDescription"]).with_near_vector({"vector": query_embedding}).with_limit(5).do()
    
    def attack_openai_query(self, query_embedding):
       result =  self.client.query.get("Attack_Entry", ["attackID", "type", "name", "description"]).with_near_vector({"vector": query_embedding}).with_limit(5).do()
       print("\n=== DEBUG: Raw Weaviate Results ===")
    #    print(result)
       return result

    def wipe_all_data(self):
        """
        Wipe all data and schemas from Weaviate.
        """
        existing_classes = self.client.schema.get() or {"classes": []}
        for cls in existing_classes['classes']:
            class_name = cls['class']
            #print(f"Deleting class: {class_name} and all associated data...")
            self.client.schema.delete_class(class_name)
        print("All data and schemas have been wiped. Weaviate is now clean.")