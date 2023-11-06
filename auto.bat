@echo off

:menu
echo Auto Script Menu
echo 1. Create Superuser
echo 2. Migrate
echo 3. Make Migrations
echo 4. Up (Build and Start)
echo 5. Down
echo 6. Test
echo 7. Exit
set /p choice=Enter your choice:

if "%choice%"=="1" goto superuser
if "%choice%"=="2" goto migrate
if "%choice%"=="3" goto makemigrations
if "%choice%"=="4" goto up
if "%choice%"=="5" goto down
if "%choice%"=="6" goto test
if "%choice%"=="7" goto exit

:superuser
docker-compose run --rm web python manage.py createsuperuser
goto menu

:migrate
docker-compose run --rm web python manage.py migrate
goto menu

:makemigrations
docker-compose run --rm web python manage.py makemigrations
goto menu

:up
docker-compose up --build
goto menu

:down
docker-compose down
goto menu

:test
docker-compose run --rm web python manage.py test src.exchange_rates.tests
goto menu

:exit
exit /b
