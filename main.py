import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import sqlite3

#pull dataset from database
def dataset():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(""" SELECT * FROM vaccinations_clean1 """)
    r = cur.fetchall()
    
    return r

#get moving averages
def movAveArr(dataset, window):
    movAve = []
    for i in range(len(dataset)):
        if not i < window - 1:
            sum = 0
            for j in range(0, window):
                sum += dataset[i-j]
            movAve.append(sum/window)

    return movAve

#data prep
dataset = dataset()

dates = [record['date'] for record in dataset]

daily_vax = [record['daily_vaccinations'] for record in dataset]

total_vax_dates = [record['date'] for record in dataset if record['total_vaccinations'] != 0] 
total_vax = [record['total_vaccinations'] for record in dataset if record['total_vaccinations'] != 0]

vax_rate_arr = movAveArr(daily_vax, 7)
vax_rate_dates = dates[6:]

days_before_hImmunity = (140000000 - dataset[-1]['total_vaccinations']) / vax_rate_arr[-1]

goal_date = datetime.datetime(2022, 1, 1)
date_now = datetime.datetime.now()
days_before_goal = (goal_date - date_now).days
optimal_rate = (140000000 - dataset[-1]['total_vaccinations']) / days_before_goal

print(f"Total Vaccines Administered: {'{:,}'.format(dataset[-1]['total_vaccinations'])}")
print(f"Current daily vaccination rate: {'{:,.2f}'.format(vax_rate_arr[-1])}")
print(f"Years before herd immunity is achieved: {'{:,.2f}'.format(days_before_hImmunity/365)}")
print(f"Optimal rate to achieve herd immunity before 2022: {'{:,.2f}'.format(optimal_rate)}")

#format dates
x_dates = [datetime.datetime.strptime(d, "%Y-%m-%d") for d in dates]
total_vax_dates = [datetime.datetime.strptime(d, "%Y-%m-%d") for d in total_vax_dates]
vax_rate_dates = [datetime.datetime.strptime(d, "%Y-%m-%d") for d in vax_rate_dates]

formatter = mdates.DateFormatter("%Y-%m-%d")
locator = mdates.DayLocator(interval=7)

#plotting
#line graphs
figDailyVax = plt.figure()
figTotalVax = plt.figure()
figVaxRate = plt.figure()

axDailyVax = figDailyVax.add_subplot(111)
axTotalVax = figTotalVax.add_subplot(111)
axVaxRate = figVaxRate.add_subplot(111)

axDailyVax.xaxis.set_major_locator(locator)
axDailyVax.xaxis.set_major_formatter(formatter)
axTotalVax.xaxis.set_major_formatter(formatter)
axTotalVax.xaxis.set_major_locator(locator)
axVaxRate.xaxis.set_major_formatter(formatter)
axVaxRate.xaxis.set_major_locator(locator)

axDailyVax.set_title('Daily Vaccinations')
axDailyVax.set_xlabel("Date")
axDailyVax.set_ylabel("Vaccines administered")

axTotalVax.set_title('Total Vaccinations')
axTotalVax.set_xlabel("Date")
axTotalVax.set_ylabel("Total vaccines administered (in millions)")

axVaxRate.set_title('Daily Vaccination Rate')
axVaxRate.set_xlabel("Date")
axVaxRate.set_ylabel("Vaccination rate (7 day moving average")

axDailyVax.plot(x_dates, daily_vax)
axTotalVax.plot(total_vax_dates, total_vax)
axVaxRate.plot(vax_rate_dates, vax_rate_arr)

figVaxRate.autofmt_xdate()
figTotalVax.autofmt_xdate()
figDailyVax.autofmt_xdate()

plt.show()