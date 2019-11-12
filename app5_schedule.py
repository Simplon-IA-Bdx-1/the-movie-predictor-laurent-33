import schedule
import time
from app5_apirest import import_current_movies


def job():
    results = import_current_movies()
    print(results)


schedule.every().wednesday.at("13:15").do(job)

print("Starting scheduler")
while True:
    schedule.run_pending()
    time.sleep(1)
