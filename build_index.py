import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import MarkdownHeaderTextSplitter
from config import DATA_FOLDER, DB_FOLDER, COLLECTION_NAME, EMBEDDING_MODEL

# Define headers for structured markdown chunking
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3")
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

def build_index():
    """Builds the ChromaDB vector index from markdown documents."""
    print("Initializing ChromaDB and Embedding model...")
    huggingface_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=DB_FOLDER)

    # Remove old collection to rebuild safely
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print("Removed old collection.")
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME, embedding_function=huggingface_ef)

    print(f"\nScanning '{DATA_FOLDER}' for markdown files...")
    if not os.path.exists(DATA_FOLDER):
        print(f"Error: Folder '{DATA_FOLDER}' not found.")
        return

    all_docs = []
    all_metadata = []
    all_ids = []
    doc_id_counter = 0

    for subdir, dirs, files in os.walk(DATA_FOLDER):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()

                    # Chunk logic via header lineage
                    chunks = markdown_splitter.split_text(text)

                    for i, chunk in enumerate(chunks):
                        header_lineage = " -> ".join([f"{v}" for k, v in chunk.metadata.items()])
                        if not header_lineage:
                            header_lineage = file.replace("_", " ").replace(".md", "")

                        embed_text = (
                            f"Document: {file.replace('_', ' ').replace('.md', '')}\n"
                            f"Section: {header_lineage}\n\n"
                            f"Content:\n{chunk.page_content}"
                        )
                        
                        all_docs.append(embed_text)
                        all_metadata.append({
                            "file_path": file_path,
                            "source_file": file,
                            "chunk_index": str(i),
                            "total_chunks": str(len(chunks)),
                            "header_lineage": header_lineage
                        })
                        all_ids.append(f"doc_{doc_id_counter}")
                        doc_id_counter += 1

                    print(f"   ✅ Indexed via Markdown Splitter: {file_path} ({len(chunks)} sections mapped)")
                except Exception as e:
                    print(f"   ⚠️  Error reading {file}: {e}")

    if all_docs:
        print(f"\nAdding {len(all_docs)} entries to ChromaDB...")
        batch_size = 100
        for i in range(0, len(all_docs), batch_size):
            end = min(i + batch_size, len(all_docs))
            collection.add(
                documents=all_docs[i:end],
                metadatas=all_metadata[i:end],
                ids=all_ids[i:end],
            )
        print("\n✅ Index built successfully!")
        print(f"   Total entries indexed: {len(all_docs)}")
    else:
        print("No markdown files found to process.")

if __name__ == "__main__":
    build_index()
