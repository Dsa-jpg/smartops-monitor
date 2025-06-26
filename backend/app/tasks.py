from celery import shared_task
import requests
from app.db import SessionLocal
from app import crud, models
from app.webhook.hook_discord import send 
from app.config import WEBHOOK
from app.schemas import AlertCreated

@shared_task
def check_all_services():
    db = SessionLocal()
    services = db.query(models.Service).all()
    print(services)

    for service in services:
        try:
            response = requests.get(service.url, timeout=5)
            status_code = response.status_code
        except Exception:
            status_code = 0  # timeout nebo jiná chyba

        previous_status = service.status
        crud.update_service_status(db, service.id, status_code)
        crud.add_service_status_history(db, service.id, status_code)

        if status_code != previous_status:
            message = f"Service *{service.name}* ({service.url} return code `{service.status}`)"
            alert_data = AlertCreated(message=message, level="warning", service_id=service.id)
            crud.create_alert(db, alert_data)
            send(service.name, status_code, service.url, WEBHOOK)


    db.commit()
    db.close()

