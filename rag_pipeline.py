import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from config import (
    DB_FOLDER, COLLECTION_NAME, EMBEDDING_MODEL, MASTER_REPORT_PATH,
    BROAD_QUERY_KEYWORDS, QUERY_OPTIMIZER_PROMPT, TOP_K_DOCS
)

class RAGPipeline:
    def __init__(self):
        """Initializes the Vector Database client and embedding pipeline."""
        print("Loading ChromaDB Document Router...")
        self.chroma_client = chromadb.PersistentClient(path=DB_FOLDER)
        self.huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
        
        try:
            self.collection = self.chroma_client.get_collection(
                name=COLLECTION_NAME, 
                embedding_function=self.huggingface_ef
            )
            print(f"✅ ChromaDB ready. {self.collection.count()} documents indexed.")
        except Exception:
            print("WARNING: ChromaDB collection not found! Run build_index.py first.")
            self.collection = None

    def is_broad_query(self, query: str) -> bool:
        """Determines if the query seeks a general overview or list."""
        q = query.lower()
        return any(kw in q for kw in BROAD_QUERY_KEYWORDS)

    def read_file_content(self, file_path: str) -> str:
        """Reads and returns the specified file content."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"⚠️ Could not read file {file_path}: {e}")
            return None

    def optimize_query(self, user_input: str, conversation_history: list, client: OpenAI, model: str) -> str:
        """Expands acronyms and resolves conversational pronouns."""
        optimized_query = user_input
        try:
            optimizer_messages = [{"role": "system", "content": QUERY_OPTIMIZER_PROMPT}]
            # Provide recent history context for pronoun resolution
            recent_history = [m for m in conversation_history if m["role"] != "system"][-4:]
            optimizer_messages.extend(recent_history)
            optimizer_messages.append({"role": "user", "content": f"Optimize this query: {user_input}"})

            opt_response = client.chat.completions.create(
                model=model,
                messages=optimizer_messages,
                temperature=0,
            )
            optimized_query = opt_response.choices[0].message.content.strip()
            print(f"🔍 Original: '{user_input}' | Optimized: '{optimized_query}'")
        except Exception as e:
            print(f"⚠️ Query optimizer failed, using original: {e}")
        
        return optimized_query

    def retrieve_context(self, optimized_query: str) -> str:
        """Retrieves targeted context chunks or broad overview files via vector search."""
        context_text = ""
        full_contents = []

        if self.is_broad_query(optimized_query):
            print("🗺️ Broad query detected — loading master report.")
            content = self.read_file_content(MASTER_REPORT_PATH)
            if content:
                full_contents.append(
                    f"=== SOURCE: MASTER REPORT ===\n{content}\n=== END OF REPORT ==="
                )
        elif self.collection:
            try:
                results = self.collection.query(
                    query_texts=[optimized_query],
                    n_results=TOP_K_DOCS,
                )
                matched_metadatas = results['metadatas'][0]
                matched_documents = results['documents'][0]
                
                print(f"📄 Router selected {len(matched_metadatas)} chunk(s):")
                for i, meta in enumerate(matched_metadatas):
                    source_file = meta.get("source_file", "unknown")
                    header_lineage = meta.get("header_lineage", "General")
                    print(f"   -> {source_file} ({header_lineage})")
                    
                    chunk_text = matched_documents[i]
                    full_contents.append(
                        f"=== MATCH {i+1} ===\n{chunk_text}\n=== END OF MATCH {i+1} ==="
                    )
            except Exception as e:
                print(f"⚠️ ChromaDB routing failed: {e}")

        if full_contents:
            context_text = (
                "\n\n--- UNIVERSITY KNOWLEDGE BASE (Answer strictly from this) ---\n\n"
                + "\n\n".join(full_contents)
                + "\n\n--- END OF KNOWLEDGE BASE ---"
            )
        
        return context_text
