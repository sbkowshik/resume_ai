# Merchant Normalization Pipeline 
Implementation of a prototype for a merchant name normalization pipeline that will generate embeddings from merchant names by crawling the internet to scrape merchant names from various sources, transform these names, and then store the resulting embeddings in Qdrant.

### Required APIs
```
1. HUGGINGFACEHUB_API_TOKEN
2. QDRANT_URL
3. QDRANT_API_KEY
4. REDIS_URL
5. REDIS_PASSWORD
6. GOOGLE_API_KEY
7. SERPER_API_KEY
8. EXA_API_KEY
```

### Steps 
```
1. Clone the repository - git clone https://github.com/sbkowshik/merchant_normalization_pipeline.git
2. Install dependencies - pip install -r requirements.txt
3. Create a .env file - and past your APIs
4. Starting the FastAPI application - vicorn api_endpoint:app --reload
```
