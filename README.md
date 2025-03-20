# Campaign Data Processing API

## Overview

This project is a **FastAPI-based RESTful API** designed to fetch, process, and return campaign-related data from a **MySQL** database. It merges data from two tables based on query parameters and returns results in JSON format.

The implementation ensures efficiency, modularity, and scalability, following best practices in API design and database interaction.

## Features

- **Fetch & Merge Data**: Joins campaign metrics and scores from two database tables using a common campaign ID.
- **Dynamic Query Parameters**:
  - `campaign_id` (Optional): Retrieve data for a specific campaign.
  - `start_date` (Required): Define the start of the data range.
  - `end_date` (Required): Define the end of the data range.
- **FastAPI & SQLAlchemy** for high-performance API development.
- **Deployed on AWS** with a containerized approach using **Docker**.
- **Optimized Query Performance**: Efficient SQL joins and filtering for large datasets.

## Project Structure

```
campaign_api/
│── app/
│   ├── __init__.py
│   ├── database.py      # Manages database connection using SQLAlchemy
│   ├── main.py          # FastAPI app with route definitions
│   ├── models.py        # Defines ORM models for database tables
│   ├── schemas.py       # Pydantic models for request validation
│
│── tests/
│   ├── __init__.py
│   ├── test_api.py      # Unit tests for API functionality
│
│── .env                 # Environment variables (excluded from Git)
│── .dockerignore        # Ignore files for Docker builds
│── .gitignore           # Ignore unnecessary files
│── Dockerfile           # Containerization for deployment
│── requirements.txt     # Project dependencies
```

## Setup & Deployment

### **1. Install Dependencies**
Ensure you have Python 3.9+ and a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### **2. Configure Environment Variables**
Create a `.env` file and add:
```
DATABASE_URL=mysql://username:password@localhost/db_name
```

### **3. Run the API Locally**
```bash
uvicorn app.main:app --reload
```

### **4. Docker Deployment**
```bash
docker build -t campaign-api .
docker run -p 8000:8000 --env-file .env campaign-api
```

### **5. Deploy on AWS (Optional)**
- Use **EC2** or **ECS with Fargate** for scalable deployment.
- Configure **Amazon RDS** for MySQL database hosting.
- Use **Elastic Load Balancer (ALB)** for traffic distribution.

## API Endpoints

### **GET /campaigns/**
Fetch campaign data based on query parameters.

**Example Request:**
```bash
curl "http://localhost:8000/campaigns/?campaign_id=123&start_date=2023-01-01&end_date=2023-12-31"
```

**Response:**
```json
{
  "campaign_id": "123",
  "campaign_name": "Winter Promo",
  "metrics": {
    "impressions": 10000,
    "clicks": 500
  },
  "daily_trends": [
    {"date": "2023-01-01", "impressions": 2000, "cpm": 5.0}
  ]
}
```

## Future Improvements

- **Authentication & Security**: Implement OAuth or API key-based authentication.
- **Query Optimization**: Introduce caching mechanisms like Redis.
- **Observability**: Add logging and monitoring tools.

## License

This project is open-source and available under the **MIT License**.
