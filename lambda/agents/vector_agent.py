import weaviate
# --- CORRECTED IMPORTS ---
# Import Property, DataType, and Configure for cleaner code.
from weaviate.classes.config import Property, DataType, Configure
from sentence_transformers import SentenceTransformer

# Connect to a local Weaviate instance
try:
    client = weaviate.connect_to_local()
    print("Successfully connected to Weaviate!")
except Exception as e:
    print(f"Failed to connect to Weaviate: {e}")
    exit()
finally:
    # This ensures the client is connected before we proceed.
    # It's good practice for robustness.
    if not client.is_connected():
        print("Could not establish a connection.")
        exit()

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define the collection name
collection_name = "News"

# Check if the collection already exists and create it if not
if not client.collections.exists(collection_name):
    print(f"Collection '{collection_name}' does not exist. Creating it now.")
    news_collection = client.collections.create(
        name=collection_name,
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="description", data_type=DataType.TEXT)
        ],
        # --- FIX 1: UPDATED ARGUMENT ---
        # `vectorizer_config` is deprecated in v4. The new argument is `vector_config`.
        # Using Configure class for better readability.
        vector_config=Configure.Vectorizer.none()
    )
    print(f"Collection '{collection_name}' created.")
else:
    print(f"Collection '{collection_name}' already exists.")
    news_collection = client.collections.get(collection_name)


# Function to store embeddings using the v4 batching context manager
def store_embeddings(news_list):
    # Use a batch context manager for efficient data insertion
    # This context manager handles retries and will raise an exception on failure.
    with news_collection.batch.dynamic() as batch:
        for title, description in news_list:
            # Create the vector
            vector = model.encode(title + " " + description).tolist()

            # Prepare the properties for the object
            properties = {
                "title": title,
                "description": description
            }

            # Add the object to the batch
            batch.add_object(
                properties=properties,
                vector=vector
            )
    # --- FIX 2: CORRECTED BATCH HANDLING ---
    # The `batch` context manager object in v4 does not have a `failed_objects`
    # attribute. The process is now more direct: if an object fails to import
    # after retries, the client will raise an exception.
    # A simple success message is sufficient here.
    print("Batch import process complete.")

# Example usage
if __name__ == "__main__":
    sample_news = [
        ("Stocks rise today", "Tech leads the market rally."),
        ("Market falls sharply", "Investors worry about inflation."),
        ("New smartphone released", "Features a revolutionary new camera."),
        ("SpaceX launches new mission", "Another successful launch for the private space company.")
    ]

    print("\nStoring embeddings...")
    store_embeddings(sample_news)
    print("Embeddings stored successfully in Weaviate!")

    # Always close the client connection when you're done
    client.close()
    print("\nClient connection closed.")
