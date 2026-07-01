USER          = os.getenv("USER", "rodie916")

CLUSTER_NAME  = "Cluster0"

MONGO_URI     = os.getenv("MONGO_URI",
    "mongodb+srv://rodie916:rodie916@cluster0.idqgg3d.mongodb.net/?retryWrites=true&w=majority")
DB_NAME       = "examenfinal"
COLLECTION    = "documentos"

COHERE_API_KEY = os.getenv("COHERE_API_KEY", "1OtvRa4xQit2OZj2ZB6DqUFOqEd90hGu37s2fCkMSLQqTZ2pYEqfJQQJ99CGACZoyfiEqg7NAAACAZCRmd1h")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "5gsIG6McVSDCa8Z7ZRb8j6eZbJNbGUBDIYneI3iITl8sFfEqZj9eJQQJ99CGACZoyfiEqg7NAAACAZCRD5l1")

EMBED_MODEL   = "embed-multilingual-v3.0"
CHAT_MODEL    = "gemini-1.5-flash"
TOP_K         = 3
