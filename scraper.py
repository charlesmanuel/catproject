import os
import sys
import csv
import schedule
import time
import urllib.request, json
from datetime import datetime

def write_csv(date, time, location, num_climbing):
	file_name = str(location) + '.csv'
	with open(file_name, mode='a+', newline='') as f:
		row_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		row_writer.writerow([date, time, num_climbing])

def check_open(day, time, location):
	time = int(time)
	day = str(day)
	weekend = ['Saturday', 'Sunday']
	if location == 'metrorock-littleton':
		if day in weekend:
			if time >= 9 and time < 21:
				return True
			else:
				return False
		else:
			if time >= 10 and time < 21:
				return True
			else:
				return False
	elif location == 'metrorock-newburyport':
		if day in weekend:
			if time >=10 and time < 18:
				return True
			else:
				return False
		else:
			if time >= 12 and time < 22:
				return True
			else:
				return False
	else:
		if time >= 22:
			return False
		elif day in weekend:
			if time >= 9:
				return True
			else:
				return False
		elif day == 'Monday' or day=='Wednesday' or day == 'Friday':
			if time >=10:
				return True
			else:
				return False
		else:
			if time >=7:
				return True
			else:
				return False

def scrape():
	today = datetime.today()
	date = today.strftime("%d/%m/%Y")
	now = datetime.now()
	time = now.strftime('%H:%M')
	timecheck = now.strftime('%H')
	daycheck = today.strftime('%A')
	locations = ['metrorock-newburyport', 'metrorock-everett', 'metrorock-littleton']
	with urllib.request.urlopen('https://api.capacity.fyi/store/metrorock/counters') as url:
		data = json.loads(url.read().decode())
		for loc in data['counters']:
			if str(loc['counter_slug']) in locations:
				location = str(loc['counter_slug'])
				num_climbing = int(loc['current_count'])
				if check_open(daycheck, timecheck, location):
					write_csv(date, time, location, num_climbing)

schedule.every().hour.do(scrape)

while True:
	schedule.run_pending()
	time.sleep(60)