from stockhelper.updateDatabase import updateDatabase
from chinese_calendar import is_workday
import pytz
import datetime
import schedule
import time
tz = pytz.timezone('Asia/Shanghai')
updater = updateDatabase()
updater.updateAllDatabase()


# pdb.set_trace()
def update_all_database():
    # This function do the updating and inintialization
    now = datetime.datetime.now(tz=tz)
    if is_workday(now):
        updater.updateAllDatabase()
        print("Dataset is updated")
    else:
        print("Today is holiday! Have a nice day!")


schedule.every().day.at("15:05").do(update_all_database)
while True:
    schedule.run_pending()
    time.sleep(1)
