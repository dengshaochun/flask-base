# flask-base
A basic flask rest api web demo, support celery async task and docker image.

Main depends:
- `python3`
- `flask`
- `flask-restful`
- `celery`
- `docker`
  
-----------------
### Start Command
```bash
# start flask web
$ python manage.py run server -h 0.0.0.0 -p 5000

# start celery worker
$ celery -A demo.celery_app.celery_worker worker -l info

# start celery beat
$ celery -A demo.celery_app.celery_worker beat -l info

# start celery flower
$ celery flower --broker=redis://localhost:6379/0 --port=5555
# or
$ celery -A demo.celery_app.celery_worker flower --port=5555
```

-----------------
### Url Map
```bash
$ python manage.py urlmap
Endpoint                                           Methods                                  Route
api.hellotaskresource                              GET,HEAD,OPTIONS                         /api/v1/tasks/func/hello/
api.addtaskresource                                POST,OPTIONS                             /api/v1/tasks/func/add/
api.taskdetailresource                             GET,HEAD,OPTIONS                         /api/v1/tasks/<task_id>/
static                                             GET,HEAD,OPTIONS                         /static/<path:filename>
```

-----------------
### Paginate And Filter
Support request params:
- `page`
- `page_size`
- `order_by`
- `{columns}`
- `{columns__like}`

Query examples:
- `http://api.example.com/api/v1/tasks/?page=1&page_size=10&task_id=xxxx-xxx-xxx`
- `http://api.example.com/api/v1/tasks/?page=1&page_size=10&task_id__like=xxxx&order_by=-task_id` 

-----------------
### Docker Support
- `Dockerfile`
- `docker-compose.yml`

-----------------
### Project Structure
```bash
$ tree -I '__pycache__|*venv*|*.pyc|*migrations*|*.sqlite|.idea*|.git*' -a
.
├── demo
│   ├── api
│   │   ├── __init__.py
│   │   └── task.py
│   ├── celery_app
│   │   ├── celeryconfig.py
│   │   ├── celery_worker.py
│   │   ├── custom_task.py
│   │   ├── __init__.py
│   │   └── tasks
│   │       ├── examples.py
│   │       └── __init__.py
│   ├── databases.py
│   ├── errors.py
│   ├── extensions.py
│   ├── helpers.py
│   ├── __init__.py
│   ├── models
│   │   └── __init__.py
│   ├── settings.py
│   └── utils
│       ├── common.py
│       └── __init__.py
├── docker-compose.yml
├── docker-entrypoint.sh
├── Dockerfile
├── .dockerignore
├── .env_example
├── .gitignore
├── manage.py
├── pip.conf
├── README.md
├── requirement.txt
├── static
└── templates
```