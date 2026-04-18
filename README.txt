PROJECT TITLE: Hotel Management System

DESCRIPTION:
This project is a Django-based web application designed to manage hotel operations such as user management, room booking, and services. The system is structured into multiple apps based on the Entity-Relationship Diagram (ERD). Each app represents a specific module of the system.The project is uses Workbench as the database backend.

PROJECT STRUCTURE:

* users: Handles user-related data including User, Customer, Staff, and Admin.
* booking: Manages room types, rooms, reservations, and bookings.
* services: Handles payments, services, and service requests.
* templates: Contains HTML files such as index.html and login.html.
* hotel_system: Main Django project configuration (settings, URLs, views).
* manage.py: Django command-line utility.

FEATURES IMPLEMENTED:

* Multi-app Django project based on ERD
* Models with relationships (ForeignKey, OneToOneField)
* MySQL database integration
* Index page with navigation to system modules
* Login page with authentication using Django’s built-in authentication system
* Admin panel for managing data

HOW TO RUN THE PROJECT:

1. Install required packages:
   pip install django mysqlclient

2. Create a MySQL database:
   CREATE DATABASE hotel_db;

3. Configure database in settings.py:
   Update DATABASES section with your MySQL credentials.

4. Apply migrations:
   python manage.py makemigrations
   python manage.py migrate

5. Create admin user:
   python manage.py createsuperuser

6. Run the development server:
   python manage.py runserver 8080

7. Access the system:
   Main page: http://127.0.0.1:8080/
   Login page: http://127.0.0.1:8080/login/
   Admin panel: http://127.0.0.1:8080/admin/