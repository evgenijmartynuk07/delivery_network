# delivery_network


The "Food Top" delivery network has numerous points where orders are prepared for customers. Each customer wants to receive a receipt along with their order, which contains detailed information about the order. Kitchen staff also require receipts to ensure they don't forget anything during the preparation and packaging process. Our task is to assist both parties by developing a receipt generation service.

1. After sending the API to the server, we create Check models in the database.
2. Then, the generation of check files is queued for execution.
3. Next, the running Celery task searches for the generated checks and prints them (the task is executed every 10 seconds).

## Installation

Python3 must be already installed

The project runs local. 
Redis, PostgresSQL and wkhtmltopdf directly in Docker, all configurations will be automatically generated.

```shell
git clone https://github.com/evgenijmartynuk07/delivery_network.git
cd delivery_network
```

### Create virtualenv
```shell
python -m venv venv

Windows: venv\Scripts\activate
Linux, Unix: source venv/bin/activate
```

### Install requirements
```shell
pip install -r requirements.txt
```

### Create environment file
```shell
create .env based on .env.sample
```

### Run Docker-Compose for create Database
```shell
docker-compose up -d
```

### Create table in Database
```shell
python manage.py makemigrations
python manage.py migrate
```

### Create User and load data to Database
```shell
python manage.py createsuperuser (for use admin panel)
python manage.py loaddata printers.json
```

### Run Celery and Project togather
```shell
celery -A backend.delivery_network worker --beat --loglevel=info & python manage.py runserver
```

If You have any questions: https://t.me/eugen_martynuk