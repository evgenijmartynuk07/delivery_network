# delivery_network


## Installation

Python3 must be already installed

The project runs local. 
Redis, PostgresSQL and wkhtmltopdf directly in Docker, all configurations will be automatically generated.

```shell
git clone https://github.com/evgenijmartynuk07/delivery_network.git
cd delivery_network

python -m venv venv

Windows: venv\Scripts\activate
Linux, Unix: source venv/bin/activate

pip install -r requirements.txt

1. create .env based on .env.sample
2. docker-compose up -d
3. python manage.py migrate
4. python manage.py createsuperuser (for use admin panel)
5. celery -A delivery_network worker --beat --loglevel=info & python manage.py runserver
```
