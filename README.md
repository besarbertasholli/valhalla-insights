# Valhalla Insights  

## Overview  

This repository contains the code and data for the Valhalla Insights web application, which aggregates and presents information about historical characters. The project involves web scraping, data processing, and a deployed web interface for browsing the collected data.  

## Deployment  

The application is deployed on a personal dedicated server I had available and can be accessed here:  
🔗 [http://68.183.215.78:8080/](http://68.183.215.78:8080/)  

## End-to-End Pipeline  

The project follows a structured pipeline to ensure data accuracy and reliability:  

1. **Web Scraping**  
   - Data is scraped from multiple sources using Scrapy.  
   - Headers, and user-agent rotation are used to prevent blocking.  
   - The scraper handles redirects and retries on failure.  
   - The pipeline handles missing data from the sites and has cases of fallback options.  

2. **Data Processing & Storage**  
   - Raw scraped data is cleaned, structured, and stored in a PostgreSQL database through the Django ORM.  
   - Django Migrations are included to recreate database tables.
   - If a record already exists, it is updated instead of duplicated.

3. **Web Application**  
   - A Django-based web application provides an interface for browsing and searching characters.  
   - Bootstrap is used for quick and responsive design.  

4. **Scheduling & Updates**  
   - Scraping jobs are scheduled via `cron`  
   - Data updates periodically to ensure freshness.  

5. **Error Handling & Robustness**  
   - Logging and monitoring track scraping failures and data inconsistencies.  
   - Failed requests are retried  

## Repository Contents  

🔹 **Scraped Data:** Sample output files containing extracted information, put in the data folder.  
🔹 **Scraping Pipeline:** Scraping classes and data pipelines.  
🔹 **Database Migrations:** Django migration files to recreate database tables.  
🔹 **Web Application Code:** A frontend with list and detail pages for Characters and Players 
🔹 **Django Admin:** Django project with all required dependencies.  
🔹 **Setup Instructions:** A detailed README to guide deployment and usage.  
🔹 **CI/CD Pipeline:** A simple pipeline to deploy the project to live server on every push.  
🔹 **Cron setup:** The setup that schedules the scrapers on specific timelines.  

## Setup & Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/besarbertasholli/valhalla-insights.git
   cd valhalla-insights
   ```

2. Create the Docker setup, which sets up 3 containers: valhalla_database, valhalla_django_app and scrapy_scheduler:  
   ```bash
   docker compose up --build -d
   ```

3. Create an admin user if you need Django admin access through the django app, and follow the instructions:
   ```bash
   docker exec -it valhalla_django_app /bin/bash
   ```
   ```bash
   python manage.py createsuperuser
   ```

4. The scrapy scheduler is now already started for 3 spiders:
    - [Vikings](https://www.history.com/shows/vikings/cast) scheduler running every day at midnight
    - [Norsemen](https://www.imdb.com/title/tt5905354/)  scheduler running every day at 1 AM
    - [Vikings NFL](https://www.vikings.com/team/players-roster/) scheduler running every day at 2 AM
