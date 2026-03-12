
# ETEC2104 – Trading Exchange (Django Template)

This project is the starting point for the **Exchange backend** used in the ETEC2104 trading system project.

Students will extend this system by adding validation, matching logic, and trader bots that interact with the exchange via HTTP.

---

# Project Architecture

This project uses:

- Django
- Django REST Framework
- SQLite (development database)

Apps:

| App | Purpose |
|----|----|
| exchange | Market data (symbols, prices) |
| trading | Traders, positions, orders, trades |

---

# Setup Instructions

## 1. Clone the repository

git clone git@github.com:ssucsmathprof/etec2104-51.git
git clone git@github.com:ssucsmathprof/etec2104-52.git
cd etec2104-5?

## 2. Create virtual environment

Mac/Linux

python3 -m venv env
source env/bin/activate

Windows

python -m venv env
env\Scripts\activate

## 3. Install dependencies

pip install -r requirements.txt

## 4. Run migrations

python manage.py migrate

## 5. Create admin user

python manage.py createsuperuser

Example:
username: admin
password: admin

## 6. Run the server

python manage.py runserver

Server will run at:
http://127.0.0.1:8000

Admin panel:
http://127.0.0.1:8000/admin

---

# Initial Setup

Use the admin interface to create:

Symbols:
BEAR
BULL

Traders:
Each Django user should have a corresponding Trader record.

---

# API Endpoints

GET /api/orders

POST /api/orders

Example JSON:

{
  "symbol": "BEAR",
  "price": 101,
  "side": "SELL",
  "quantity": 100
}

Authentication: Basic Auth (username/password)

---

# TradeBot Testing Script

Use Postman for simple tests, but the tradebot.py we can adjust for more robust testing
Run:

python tradebot.py

This will send a sample order to the exchange API.

---

# Git Workflow

We follow a simplified Git Flow model.

Branches:

master
develop
ftr/*
bug/*

More details are in TEAM_WORKFLOW.md.

---

# Learning Goals

Students will learn:

- REST API development
- Django ORM
- collaborative Git workflows
- automated trading systems
- backend validation and business logic
