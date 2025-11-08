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


# PROMPTS
## Option 4: User-Friendly Developer Assistant
        # prompt="You are a helpful coding assistant specializing in Vumatel's NMSG (Network Management System Gateway) API.\n\n"
        #        "When answering:\n"
        #        "✓ Be accurate and cite sources from the codebase\n"
        #        "✓ Use code examples when helpful\n"
        #        "✓ Explain technical concepts clearly\n"
        #        "✗ Don't guess if the information isn't in the context\n"
        #        "✗ Don't provide outdated or speculative information\n\n"
        #        "Context: {context}\n\n"
        #        "Question: {question}\n\n"
        #        "Answer:",
## Option 3: Concise & Direct (Recommended)

        # prompt="You are a technical expert on Vumatel's NMSG (Network Management System Gateway) API.\n\n"
        #        "Answer accurately and concisely using only the provided context. "
        #        "If the answer isn't in the context, say so clearly. Never speculate.\n\n"
        #        "Context: {context}\n\n"
        #        "Question: {question}\n\n"
        #        "Answer:",




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
        temperature=0.7,
        prompt="You are a helpful coding assistant specializing in Vumatel's NMSG (Network Management System Gateway) API.\n\n"
               "When answering:\n"
               "✓ Be accurate and cite sources from the codebase\n"
               "✓ Use code examples when helpful\n"
               "✓ Explain technical concepts clearly\n"
               "✗ Don't guess if the information isn't in the context\n"
               "✗ Don't provide outdated or speculative information\n\n"
               "Context: {context}\n\n"
               "Question: {question}\n\n"
               "Answer:",
        excluded_folders = ['.git', 'bin', 'obj', 'packages', 'node_modules', '.idea', 'NmsGateway.Tests']
    )

    # Initialize the system
    rag.initialize(force_refresh_db=True)

    # Option C: Launch Gradio interface
    rag.launch_gradio(inbrowser=True)

# With Prompting
# rag = RAGKnowledgeWorker(
#     kb_folder="./docs",
#     file_patterns={'md': '**/*.md'},
#     model_name="gpt-4o-mini",
#     prompt="You are an expert. Context: {context}\n\nQuestion: {question}\n\nAnswer:"
# )
# rag.initialize()

# rag = create_rag_worker(
#     kb_folder="./docs",
#     file_patterns={'md': '**/*.md'},
#     model_name="gpt-4o-mini",
#     prompt="Context: {context}\n\nQ: {question}\n\nA:"
# )
