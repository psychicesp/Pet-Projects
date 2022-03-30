#%%
import pandas as pd
from datetime import datetime as dt, timedelta as td
## Analysis:

# So many columns are strings formatted like "3 mins" or "5.5 oz"
#   This should numberize pretty much any of them:
birthday = dt(year = 2021, month = 12, day = 21, hour = 11, minute = 15)
numberizer = lambda x: float(x.split(' ')[0])

def get_timeslot(fed_time, sensitivity = 90):
    today = dt.today()
    time_list = ['02:30', '07:00', '10:00', '13:00', '16:00', '19:00', '22:30']
    # time_list_dt = [dt.strptime(x+':00', '%X').time() for x in time_list_str]
    for time_str in time_list:
        time_slot = dt.strptime(time_str+':00', '%X').time()
        minutes = dt.combine(today, time_slot)-dt.combine(today, fed_time)
        minutes = minutes.total_seconds() / 60
        minutes = abs(minutes)
        if minutes < sensitivity:
            return time_str

def streighten_df(df):
    df['Datetime'] = df['Time'].apply(lambda x: dt.strptime(x, "%m/%d/%y %I:%M %p"))
    try:
        df['Bottle'] = df['Amount'].apply(numberizer)
    except:
        df['Minutes Nursed']= df['Left duration'].fillna('0 min').apply(numberizer) + df['Right Duration'].fillna('0 min').apply(numberizer)
    df['Day'] = df['Datetime'].apply(day_get)
    df['Week'] = df['Datetime'].apply(week_get)
    df['Time'] = df['Datetime'].apply(lambda x: x.time())
    df['Timeslot'] = df['Time'].apply(get_timeslot)
    return df

def day_get(datetime):
    duration = datetime - birthday
    return duration.days + 1

def week_get(datetime):
    duration = datetime -birthday
    return round(duration.days/7, 0) +1

express_df = pd.read_csv('data/Minnie_pumped.csv')[['Time','Amount']]
formula_df= pd.read_csv('data/Minnie_formula.csv')[['Time','Amount']]

express_df = streighten_df(express_df)
formula_df = streighten_df(formula_df)

nursing_df = pd.read_csv('data/Minnie_nursing.csv')
nursing_df = streighten_df(nursing_df)

# nc stands for need-corrected

bottle_df = pd.concat([express_df, formula_df])
bottle_average = bottle_df[['Day','Bottle']].groupby('Day').sum().to_dict()['Bottle']
bottle_df['Bottle Day Total'] = bottle_df['Day'].apply(lambda x: bottle_average.get(x, 0.0))

bottle_times = bottle_df.groupby(['Timeslot', 'Day']).agg({
    'Week': 'mean',
    'Bottle': 'sum'
}).reset_index()

nurse_times = nursing_df[['Day','Minutes Nursed', 'Timeslot']].groupby(['Day','Timeslot']).sum().reset_index()

feeding_df = pd.concat([bottle_df, nursing_df])
feeding_df['nc_feeding_time'] = feeding_df['Minutes Nursed']/70
feeding_df = feeding_df.groupby(['Day','Timeslot', 'Week']).sum().reset_index()

feeding_average = feeding_df[['Day','Minutes Nursed']].groupby('Day').sum().to_dict()['Minutes Nursed']
feeding_df['Nursing Day Total'] = feeding_df['Day'].apply(lambda x: feeding_average.get(x, 0.0))

feeding_df = feeding_df[feeding_df['Bottle Day Total'] > 10]
feeding_df = feeding_df[feeding_df['Nursing Day Total'] == 0]
feeding_df['controlled feed'] = feeding_df['Bottle']/feeding_df['Bottle Day Total']
feeding_means = feeding_df[['controlled feed', 'Timeslot']].groupby('Timeslot').mean()
relevant_day_total = bottle_df[bottle_df['Day'] == bottle_df['Day'].max()-1]['Bottle'].sum()
feeding_means['corrected volume'] = feeding_means['controlled feed'] * relevant_day_total
y_min = feeding_means['corrected volume'].min()*0.95
y_max = feeding_means['corrected volume'].max()*1.05
feeding_means[['corrected volume', 'Timeslot']].plot(ylim = (y_min, y_max))
# %%