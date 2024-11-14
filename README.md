# Stock Trading App

This is a stock trading web application built using Django, Celery, Redis, and PostgreSQL. It provides functionality for users to register, buy/sell stocks, and track transactions. Celery is used for background task processing, such as handling transactions.

## Requirements

Before running the application, ensure you have the following installed:

- **Docker**: [Installation Guide](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Installation Guide](https://docs.docker.com/compose/install/)
- **Python**: Python 3.9 or later

## Getting Started

Follow these steps to set up and run the project locally:

### 1. Clone the repository

Clone the repository to your local machine:

```bash
git clone https://github.com/HassanRajpoot/Assignement_1.git
cd Assignement_1

also the venv are as follow
DEBUG=True
SECRET_KEY=your-secret-key

DB_ENGINE=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=

Start Celery Worker:
celery -A stock_trading worker -E -l info

Start Flower (Task Monitoring):
celery -A stock_trading.celery_app flower

