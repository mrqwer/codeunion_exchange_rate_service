migrate:
	docker-compose run --rm web python manage.py migrate
makemigrations:
	docker-compose run --rm web python manage.py makemigrations
up:
	docker-compose up --build
down:
	docker-compose down
superuser:
	docker-compose run --rm web python manage.py createsuperuser
test:
	docker-compose run --rm web python manage.py test src.exchange_rates.tests
.PHONY: migrate makemigrations up down superuser