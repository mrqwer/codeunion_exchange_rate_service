# Exchange Rate Tracking Service

## Table of Contents

1. [Project Description](#project-description)
2. [Features](#features)
3. [Database](#database)
4. [Regular Course Updates](#regular-course-updates)
5. [Console Command for Data Management](#console-command-for-data-management)
6. [REST API](#rest-api)
7. [Authorization](#authorization)
8. [Testing](#testing)
9. [Usage](#usage)

---

## Project Description

This Django-based project aims to provide real-time exchange rate information in relation to the Kazakhstani Tenge (KZT). The system fetches exchange rate data from an XML source and stores it in a PostgreSQL database. It offers various methods to access and manage exchange rate data, including a REST API with Bearer authorization.

---

## Features

- **Database**: Create a PostgreSQL database with a single table, 'currency', containing information about currency exchange rates to KZT.

- **Regular Course Updates**: Implement a CRON job to periodically fetch data from [http://www.nationalbank.kz/rss/rates_all.xml](http://www.nationalbank.kz/rss/rates_all.xml) and update the exchange rates in the database.

- **Console Command for Data Management**: Develop a CLI command to update and view exchange rate data in the 'currency' table. The command accepts parameters such as currency ID and value.

- **REST API**: Create a REST API with two endpoints:
    - **GET /currencies**: Retrieve a list of all currencies and their rates in relation to KZT, with support for pagination.
    - **GET /currency/{id}**: Retrieve the exchange rate for a specific currency by its identifier (id).

- **Authorization**: Secure access to the REST API by using Bearer authorization. Clients must provide an authorization token in the request header to access the API.

- **Testing**: Implement unit tests to ensure the reliability and accuracy of the code.

---

## Database

The project uses a PostgreSQL database with a 'currency' table. The 'currency' table has the following fields:
- `id` (primary key)
- `name` (currency name)
- `rate` (currency rate to KZT)

---

## Regular Course Updates

A CRON function periodically accesses the XML data source at [http://www.nationalbank.kz/rss/rates_all.xml](http://www.nationalbank.kz/rss/rates_all.xml) and updates the exchange rates in the database. This ensures that the exchange rates stay up-to-date.

---

## Console Command for Data Management

The project includes a CLI command that allows users to update and view exchange rate data in the 'currency' table. Users can provide parameters, including currency ID and value, to modify the data.
To use CLI exchange management tool run following:
This command will update exchange currency to up-to-date.
```bash
    docker-compose run --rm web python manage.py update_currency -s 
```

if you wanna store manually data with corresponding rate values, then make following:
```bash
    docker-compose run --rm web python manage.py update_currency -s --currency_name AUD AZN AMD --currency_value 3 2 1
```

if you wanna show all currency or some of them, you can make the following way:
```bash
    docker-compose run --rm web python manage.py update_currency -g 
```
or 

```bash
    docker-compose run --rm web python manage.py update_currency -g --currency_id 7 20 39
```
---

For more information you can run command without any arguments:
```bash
    docker-compose run --rm web python manage.py update_currency
```
## REST API

The REST API provides two endpoints:

- **GET /currencies**: Retrieves a list of all currencies and their rates in relation to KZT, with support for pagination using options such as `page` and `per_page`.

- **GET /currency/{id}**: Retrieves the exchange rate for a specific currency by providing its identifier (id).

---

## Authorization

Access to the REST API is secured with Bearer authorization. Clients must include an authorization token in the request header to access the API endpoints.

---

## Testing

Unit tests have been implemented to ensure the correctness and reliability of the code. These tests help maintain the quality of the service and ensure its smooth operation.

---

## Usage

This section should provide instructions on how to use the service, including details on how to access the REST API, perform updates using the CLI command, and navigate the system.
1. Clone the repo.
2. Go to the project root directory.
3. 
   - If you on Linux use Makefile
   - If you on Windows use auto.bat file

### Example:

- On Linux

To launch the web server inside container. 
```bash
  make up 
```
To make migrations and so on.
```bash
  make makemigrations
```

- On Windows

This command shows you the menu of actions. Make choice with numbers provided there.
```powershell
  .\auto.bat
```

---

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`
`DEBUG`
`ALLOWED_HOSTS`
`POSTGRES_ENGINE`
`POSTGRES_HOST`
`POSTGRES_DB`
`POSTGRES_USER`
`POSTGRES_PORT`
`POSTGRES_PASSWORD`
