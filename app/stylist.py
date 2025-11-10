import chromadb
from openai import OpenAI
from typing import List
from fastapi import HTTPException

from . import database, config


SYSTEM_PROMPT = (
    "You are an expert fashion stylist. Your task is to create a complete, stylish outfit "
    "that is practical and comfortable for the user's specific request and weather."
)

USER_PROMPT_TEMPLATE = """
User Request: '{user_query}'
Current Weather Context: '{weather_context}'

Here are the most relevant items from my wardrobe:
{retrieved_clothes_str}

Please suggest one complete outfit using only the available items. Your reasoning MUST be based on both style and the functional properties of the items as they relate to the weather. After the outfit, add a section called 'Suggested Additions'. In this section, identify if any critical pieces (like shoes) are missing or if any enhancement pieces (like an accessory) would elevate the look. If nothing is needed, state 'None'.
"""



class AIStylist:
    """
    Encapsulates the entire AI styling pipeline.
    """
    def __init__(self, user_wardrobe: List[database.WardrobeItem]):
        if not user_wardrobe:
            raise ValueError("Wardrobe cannot be empty.")
        self.user_wardrobe = user_wardrobe
        self.owner_id = user_wardrobe[0].owner_id
        self.vector_collection = self._setup_vector_db()
        self.llm_client = OpenAI(api_key=config.settings.OPENAI_API_KEY)

    def _setup_vector_db(self):
        """
        Private method to prepare the in-memory ChromaDB collection for the user's wardrobe.
        """
        client = chromadb.Client()
        collection_name = f"user_{self.owner_id}_wardrobe"
        collection = client.get_or_create_collection(name=collection_name)
        
        # Clear any old data for this user to ensure a fresh session
        if collection.count() > 0:
            ids_to_delete = [item.id for item in collection.get()['ids']]
            collection.delete(ids=ids_to_delete)

        documents_to_embed = []
        ids = []
        for item in self.user_wardrobe:
            full_description = self._create_item_description(item)
            documents_to_embed.append(full_description)
            ids.append(str(item.id))
        
        collection.add(documents=documents_to_embed, ids=ids)
        return collection

    def _create_item_description(self, item: database.WardrobeItem) -> str:
        """
        Generates a detailed text description of a single wardrobe item for embedding.
        """
        properties = item.item_metadata.get('properties', [])
        properties_str = ', '.join(properties) if isinstance(properties, list) else 'N/A'
        
        return (
            f"Item Name: {item.name}. "
            f"Style: {item.item_metadata.get('style', 'N/A')}. "
            f"Category: {item.item_metadata.get('category', 'N/A')}. "
            f"Material: {item.item_metadata.get('material', 'N/A')}. "
            f"Properties: {properties_str}."
        )

    def _retrieve_relevant_items(self, query: str, n_results: int = 7) -> str:
        """
        Queries the vector DB to find items relevant to the user's request.
        """
        retrieved_items = self.vector_collection.query(
            query_texts=[query],
            n_results=min(n_results, len(self.user_wardrobe))
        )
        
        retrieved_clothes_list = [f"- {doc}" for doc in retrieved_items['documents'][0]]
        return "\n".join(retrieved_clothes_list)

    def _generate_suggestion(self, user_query: str, weather_context: str, retrieved_clothes_str: str) -> str:
        """
        Calls the LLM with the final, formatted prompt to generate the outfit suggestion.
        """
        user_prompt = USER_PROMPT_TEMPLATE.format(
            user_query=user_query,
            weather_context=weather_context,
            retrieved_clothes_str=retrieved_clothes_str
        )
        
        try:
            response = self.llm_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI: {e}") 
            raise HTTPException(status_code=503, detail="The AI styling service is currently unavailable.")

    def get_suggestion(self, user_query: str, weather_context: str) -> str:
        """
        The main public method that executes the full pipeline.
        """
        # 1. Retrieval
        combined_query = f"{user_query} suitable for {weather_context}"
        retrieved_clothes = self._retrieve_relevant_items(combined_query)
        
        # 2. Generation
        suggestion = self._generate_suggestion(user_query, weather_context, retrieved_clothes)
        
        return suggestion