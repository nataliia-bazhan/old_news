# old_news
Django project simple news board API

Run code:
- download code
- connect code to virtual environment
- install requirements.txt
- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py runserver

Lunch recurring job running once a day to reset post upvotes count:
- the job is done by django-background-task
- function 'clear_votes()' in content/views
The recurring job can be launched by command:
- python3 manage.py process_tasks

