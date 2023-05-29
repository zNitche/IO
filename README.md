## IO

Django powered files server, successor of [HomeDrive](https://github.com/zNitche/HomeDrive)


---

### Technologies
- Django 4.2
- redis
- bootstrap
- celery
- gunicorn
- nginx

### Features
- Accounts authentication.
- Storage space limits.
- AJAX files uploading.
- Celery powered background processes:
  - `.zip` archives extraction.
  - directories compression.
- Grouping files using directories.
- Sharing directories / files to other users.
- Downloading files / directories.
- Files preview.

### Setup
#### Dev
1. Generate `.env` config file
```
python3 generate_dotenv.py
```
2. Run dev docker services.
```
sudo docker compose -f docker-compose-dev.yml up
```
3. Run celery and celery beat workers
```
sh scripts/celery_entrypoint.sh
```
```
sh scripts/celery_beat_entrypoint.sh
```
#### Prod
1. Generate `.env` config file and change config values:
   - `DB_PATH` - database path.
   - `LOGS_PATH` - logs path.
   - `STORAGE_PATH` - storage path.
   - `ALLOWED_HOSTS` - comma separated host names.
```
python3 generate_dotenv.py
```
2. Run docker services.
```
sudo docker compose up -d
```

#### Accounts Management
Bash into web app container.
```
sudo docker container exec -it io_app bash
```
- Create superuser: `python3 manage.py createsuperuser`
- Create regular user: `python3 manage.py create_user`
- Change user storage space: `python3 manage.py set_user_private_storage_space`

#### Tests
App contains some example tests for available apps. To run them:
```
python3 manage.py test
```