from .models import crontab
def my_scheduled_job():
    obj = crontab(name="Allwin")
    obj.save()