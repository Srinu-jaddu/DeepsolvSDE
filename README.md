# Facebook Insights Microservice

A microservice for scraping and analyzing Facebook Page insights, built with FastAPI and MongoDB.

## Features

### Core Features
- Facebook Page scraping with Selenium
- Data storage in MongoDB with relationships
- RESTful API endpoints with pagination
- Caching with Redis
- Asynchronous operations
- AI-powered page analysis using OpenAI
- AWS S3 integration for media storage

### API Endpoints
- `GET /api/v1/pages/{username}` - Get page details
- `GET /api/v1/pages/search` - Search pages with filters
- `GET /api/v1/pages/{username}/posts` - Get page posts
- `GET /api/v1/pages/{username}/followers` - Get page followers
- `GET /api/v1/pages/{username}/summary` - Get AI-generated summary

## Tech Stack

- FastAPI
- MongoDB
- Redis
- Selenium
- AWS S3
- OpenAI
- Docker
- Poetry

## Project Structure

```
facebook-insights/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── pages.py
│   │   │   │   └── analytics.py
│   │   │   └── router.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── mongodb.py
│   │   └── redis.py
│   ├── models/
│   │   ├── page.py
│   │   ├── post.py
│   │   └── user.py
│   ├── schemas/
│   │   └── page.py
│   ├── services/
│   │   ├── facebook.py
│   │   ├── storage.py
│   │   └── ai.py
│   └── main.py
├── tests/
│   └── test_api.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/facebook-insights.git
cd facebook-insights
```

2. Install dependencies:
```bash
poetry install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations
```

4. Start services with Docker:
```bash
docker-compose up -d
```

5. Run the application:
```bash
poetry run uvicorn app.main:app --reload
```

## API Documentation

Access the interactive API documentation at `http://localhost:8000/docs`

## Configuration

Required environment variables:
```
MONGODB_URL=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket_name
OPENAI_API_KEY=your_openai_key
```

## Testing

Run tests with:
```bash
poetry run pytest
```

## License

MIT
