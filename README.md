### Dental Products Scraper
A FastAPI-based web scraper for dental products that extracts product information, downloads images locally, and implements caching.

#### Requirements
- Python 3.11
- Redis 7.0+
- Docker (optional, for Redis)

#### Installation
1. Clone the repository:
```bash
git clone https://github.com/brijeshshah13/atlys
cd atlys
```


2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix/MacOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start Redis:
```bash
docker run --name redis -p 6379:6379 -d redis
```

Or use local Redis installation:

```bash
brew install redis    # MacOS
brew services start redis
```

5. Create .env file:
```bash
API_TOKEN=your-secure-token
REDIS_URL=redis://localhost:6379
```

#### Running the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload --port 8000
```

#### API Usage
Scrape Products Endpoint
```bash
curl -X 'POST' \
  'http://localhost:8000/api/scrape' \
  -H 'accept: application/json' \
  -H 'X-API-Token: your-secure-token' \
  -H 'Content-Type: application/json' \
  -d '{
  "page_limit": 2,
  "proxy": "http://proxy-url:port" // Optional
}'
```

Optional parameters:

- page_limit: Number of pages to scrape
- proxy: Proxy server URL

#### Features
- Product information scraping
- Local image storage
- Redis caching
- Proxy support
- Retry mechanism
- Authentication
- Configurable page limits

#### Output
Scraped data is stored in:

- products.json: Product information
- images/: Downloaded product images

#### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc