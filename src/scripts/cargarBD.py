from langchain_chroma import Chroma
import argparse
import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from dotenv import load_dotenv
import time
from rag.componentes.database import VectorDatabase

load_dotenv()


DATA_SOURCE_PATH = "data/texto"

def main():
    # Punto de entrada y orquestador de la carga de documentos a la base de datos.
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        VectorDatabase.limpiar_bd()

    # Crea o actualiza la base de datos.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

def load_documents():
    print("📂 Loading documents from:", DATA_SOURCE_PATH)
    document_loader = DirectoryLoader(path=DATA_SOURCE_PATH, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    return document_loader.load()


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=500,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    print(f'type(VectorDatabase()): {type(VectorDatabase())}')
    print(f'type(VectorDatabase()._db): {type(VectorDatabase()._db)}')
    db = VectorDatabase()._db    
    chunks_with_ids = calculate_chunk_ids(chunks)
    
    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            print(chunk.metadata["id"], "is new and will be added to the database.")
            new_chunks.append(chunk)

    if len(new_chunks):
        for i in range(0,int(len(new_chunks)/99)+1): #Para evitar el error de exceder la cuota (GEMINI)
            print(f"👉 Adding new documents: {[i*99,99*i+1]}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks[i*99:99*(i+1)]]
            db.add_documents(new_chunks[i*99:99*(i+1)], ids=new_chunk_ids)
            print(f"✅ Added {list(range(i*99,99*(i+1)))} new documents to the database")
            print("Esperando que se pase el minuto para no exceder la cuota")
            time.sleep(1)  # Detener la ejecución para volver a usar el modelo de embedding
            print("Listo")
    else:
        print("✅ No new documents to add")

def calculate_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

if __name__ == "__main__":
    main()