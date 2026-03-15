from embedder import generate_embedding
from vector_store import store_resume
import sys

try:
    print("Generating embedding...")
    emb = generate_embedding("Hello world")
    print("Embedding generated. Storing in Endee...")
    store_resume("test1", "Hello world", emb)
    print("Success!")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
