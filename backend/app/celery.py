from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "smartops",
    broker="redis://:JFqSmnrkvuBpAsj1khkaePqumZUT3wET@redis-13080.c135.eu-central-1-1.ec2.redns.redis-cloud.com:13080/0", 
    backend="redis://:JFqSmnrkvuBpAsj1khkaePqumZUT3wET@redis-13080.c135.eu-central-1-1.ec2.redns.redis-cloud.com:13080/0")


celery.conf.beat_schedule = {
    'check_services_every_5_minutes': {
        'task': 'app.tasks.check_all_services',
        'schedule': crontab(minute='*/5'),
    },
}

celery.autodiscover_tasks(['app.tasks'])
