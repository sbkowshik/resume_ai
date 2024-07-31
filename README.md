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

### Steps for Local Hosting
```
1. Clone the repository - git clone https://github.com/sbkowshik/merchant_normalization_pipeline.git
2. Install dependencies - pip install -r requirements.txt
3. Create a .env file and paste your APIs
4. Starting the FastAPI application - uvicorn api_endpoint:app --reload
```
### Steps for Cloud Hosting (GCP)
```
1. Install Docker

2. Create a public repository (example - sbkowshik/merch-norm-pipeline)

3. CLI (Example) -
docker Login
docker build --build-arg SERVICE=api -t sbkowshik/merch-norm-pipeline:api-latest -f Dockerfile-api .
docker push sbkowshik/merch-norm-pipeline:api-latest
4. Get the container url from the repository (example - sbkowshik/merch-norm-pipeline:api-latest)

5. Put the Container URL in the Cloud Run service

6. Set the Port to the port in the code (8000)

7. Set up the environmental variables and choose appropriate configuration

8. Deploy the Application

9. Automate the Deployment
```

