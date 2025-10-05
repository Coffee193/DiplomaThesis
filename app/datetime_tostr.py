import datetime

datebj = datetime.datetime.now(datetime.timezone.utc)
datestr = datebj.strftime("%Y/%m/%d, %H:%M:%S, %Z")
date_str = str(datebj)

print(datebj)
print(datestr)
print(date_str)
print(str(datebj.replace(microsecond=0)))