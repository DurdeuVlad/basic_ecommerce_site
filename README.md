# Basic E-Commerce Site

## Introduction

This was my first real web app, the project that kickstarted my web development career. I wasn't chasing perfection; I wanted to build something functional and learn the ropes. Django was my framework of choice, and an e-commerce site felt like the right challenge: user accounts, product listings, carts, orders—the whole stack.

No tutorials, no shortcuts, just me, the Django docs, and a lot of trial and error. The result? A basic but fully functional e-commerce platform.

## Project Overview

A full-stack Django web application featuring:

User registration and authentication\
Product catalog with detail pages\
Shopping cart functionality\
Order processing\
Admin interface for managing products and orders

## Tech Stack

Backend: Python, Django\
Frontend: HTML, CSS, JavaScript\
Database: SQLite (for development)

## Setup & Installation

To run the project locally:

```bash
git clone https://github.com/DurdeuVlad/basic_ecommerce_site.git
cd basic_ecommerce_site
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

## Admin Access

Create a superuser to manage products and orders:

```bash
python manage.py createsuperuser
```

Then navigate to `http://127.0.0.1:8000/admin/` to log in.

## Why This Project Mattered

This wasn't just about learning Django. It was about understanding the full web development process. Routing, models, sessions, static files, templates—each component taught me something new.

I made mistakes, broke things, and rewrote large portions of code. But through it all, this project taught me how web development *really* works and gave me the confidence to keep building.

## License

MIT, do whatever you want with it.

