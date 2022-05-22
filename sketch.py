from datetime import datetime,timedelta

today = datetime.now()
test = today + timedelta(days=7)

print(test)