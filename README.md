In This milestone, you will be extending the functionality of the project we worked in the level.

The specification for this program is as follows,

## Specification

You are asked to build the same project we worked on in the level and add some new features to it.

1. You have to create another field in the model to store the priority of a task, no two tasks can have the same priority, the listing views must always be sorted by priority. Adding a task with an existing priority should increment the existing task's priority by 1 ( Cascading )
2. Ability to mark tasks as completed
3. Ability to view completed tasks

This milestone should be implemented with the Django ORM.

All views must be implemented using Django's Generic View classes.

## Boilerplate code

Use the following repository as a starting point for this project: https://github.com/vigneshhari/GDC-Level-6-Milestone

to install the requirements for this project, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Submission

Once all the required features are implemented, push the code to a GitHub repository and submit the link to the repo.

## Usage
__For Linux__:
```py
virtualenv .env
source .env/bin/activate
pip3 install -r requirements.txt

# on same terminal
python3 manage.py runserver

# on two different terminal
celery -A task_manager beat
celery -A task_manager worker --loglevel INFO
```
__For Window__:
In order to run redis, we have to first run the redis docker image:
```
# install docker desktop
# then run the following cmd in terminal
docker run --name gdc -p 6379:6379 -d redis
```

```py
# inside the code directory
python -m venv .env
.env/Scripts/activate
pip install -r requirements.txt

# on same terminal
python manage.py runserver

# on different terminals
celery -A task_manager beat
celery -A tasks_manager worker --loglevel=INFO -E --pool=solo
```
