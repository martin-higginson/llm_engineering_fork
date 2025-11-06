"""
Example usage of the RAG Knowledge Worker module.

This demonstrates how to use the reusable module instead of the scratch implementation.
"""

from libs.rag_knowledge_worker import RAGKnowledgeWorker, create_rag_worker

# Configuration
KB_FOLDER = r"C:\repos\nms-gateway"
FILE_PATTERNS = {
    'cs': '**/*.cs',
    'md': '**/*.md',
    'csproj': '**/*.csproj',
    'sln': '**/*.sln'
}
MODEL = "gpt-4o-mini"  # or "llama3.2" for Ollama
DB_NAME = "nmsg_vector_db"

# # Method 1: Using the convenience function (simplest)
# if __name__ == "__main__":
#     # Quick setup with defaults
#     rag = create_rag_worker(
#         kb_folder=KB_FOLDER,
#         file_patterns=FILE_PATTERNS,
#         model_name=MODEL,
#         db_name=DB_NAME,
#         use_openai_embeddings=True,
#         retriever_k=25
#     )
#
#     # Launch Gradio interface
#     rag.launch_gradio(inbrowser=True)

# Method 2: Manual configuration (more control)

if __name__ == "__main__":
    # Create instance with custom configuration
    rag = RAGKnowledgeWorker(
        kb_folder=KB_FOLDER,
        file_patterns=FILE_PATTERNS,
        model_name=MODEL,
        db_name=DB_NAME,
        use_openai_embeddings=True,
        chunk_size=2000,
        chunk_overlap=500,
        retriever_k=25,
        temperature=0.7
    )

    # Initialize the system
    rag.initialize(force_refresh_db=True)

    # Option C: Launch Gradio interface
    rag.launch_gradio(inbrowser=True)
