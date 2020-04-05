from datetime import datetime
import sqlite3
import statistics
from scipy.signal import find_peaks
import pandas as pd
import csv

# Average heart rate = sum (heart rate)/n
# Average heart rate variation = sum (heart rate variation/n)
# REM sleep latency = time atf first REM - time at last lights off
# REM sleep efficiency = time of REM sleep/ time of total sleep
# Intermittent awaking = number of lights on after first lights off
# Average room temperature =  sum(temperature)/n
# Average room humidity = sum(humidity)/n
# Number of body movement = total count of body flip


def get_rem_effeciency():

        conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')

        moving = pd.read_sql("SELECT count(*) FROM rem_info WHERE eye_movement = 'moving' ", conn)
        steady = pd.read_sql("SELECT count(*) FROM rem_info WHERE eye_movement = 'steady'", conn)
        percentage = 100*moving.at[0,'count(*)'] /(steady.at[0,'count(*)']+moving.at[0,'count(*)'] )
        return '{0:.2f}%'.format(percentage)





def get_ave_HR_variation():

    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
    df = pd.read_sql("SELECT * FROM heart_info ORDER BY id DESC", conn)

    bpm = df['bpm'].tolist()
    vari_bpm = [abs(j - i) for i, j in zip(bpm, bpm[1:])]
    vari_bpm_ave = statistics.mean(vari_bpm)
    return '{0:.2f}'.format(vari_bpm_ave)



def get_ave_HR():

    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
    df = pd.read_sql("SELECT avg(bpm) FROM heart_info ORDER BY id", conn)
    HR = df['avg(bpm)'][0]
    return '{0:.2f}'.format(HR)

def get_rem_latency():
    # you can not distinguish rem and actual eye movement
    # here use first rem - first light off
    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
    df_first_light_off = pd.read_sql("SELECT * FROM env_info WHERE r < 10 LIMIT 1", conn)
    time_first = df_first_light_off['time_stamp'][0]
    time_first_time = datetime.strptime(time_first, "%m-%d-%Y %H:%M:%S")

    conn_rem = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
    df_first_rem = pd.read_sql("SELECT * FROM rem_info WHERE eye_movement = 'moving' LIMIT 1", conn_rem)
    time_last = df_first_rem['time_stamp'][0]
    time_first_time = datetime.strptime(time_first, "%m-%d-%Y %H:%M:%S")

    time_last_time = datetime.strptime(time_last, "%m-%d-%Y %H:%M:%S")
    time_diff = time_last_time - time_first_time

    return str(time_diff)



# def get_time_in_bed(n):
#
#     conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
#     df_first = pd.read_sql("SELECT * FROM env_info WHERE r < 10 LIMIT 1", conn)
#     df_last = pd.read_sql("SELECT * FROM env_info ORDER BY id DESC LIMIT 1", conn)
#
#     time_first = df_first['time_stamp'][0]
#     time_last = df_last['time_stamp'][0]
#     time_first_time = datetime.strptime(time_first, "%m-%d-%Y %H:%M:%S")
#     time_last_time = datetime.strptime(time_last, "%m-%d-%Y %H:%M:%S")
#     time_diff = time_last_time - time_first_time
#     return 'Time in bed after light off: ' + str(time_diff)

def get_flip_number():

    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
    df = pd.read_sql("SELECT * FROM position_info ORDER BY id", conn)
    positions = df['position'].tolist()
    counter = 0
    for index,pos in enumerate(positions):
        if index == len(positions)-1:
            break
        if positions[index] != positions[index+1]:
            counter += 1
    return counter

# Intermittent awaking = number of lights on after first lights off
# not a accurate way
def get_n_intermitten_awake():
    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
    df = pd.read_sql("SELECT * FROM env_info ", conn)
    g = df['b'].tolist()
    counter = 0
    peaks, _ = find_peaks(g, height=0)

    for i in peaks:
        if g[i] > 100:
            counter += 1


    return counter






# Average room temperature =  sum(temperature)/n
def get_avg_temp():
    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
    df = pd.read_sql("SELECT * FROM env_info ", conn)
    temp = df['Temperature'].tolist()
    ave_temp = statistics.mean(temp)
    return '{0:.2f}'.format(ave_temp)



# Average room humidity = sum(humidity)/n
def get_avg_humi():
    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
    df = pd.read_sql("SELECT * FROM env_info ", conn)
    humi = df['Humidity'].tolist()
    ave_humi = statistics.mean(humi)
    return '{0:.2f}'.format(ave_humi)


def get_avg_breathing():
    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')

    df = pd.read_sql("SELECT * FROM env_info ORDER BY id DESC LIMIT 1", conn)

    avg_breathing = df['Ave_breathing_rate'].tolist()[0]
    return '{0:.2f}'.format(avg_breathing)



# REM sleep latency = time atf first REM - time at last lights off
# REM sleep efficiency = time of REM sleep/ time of total sleep
# Intermittent awaking = number of lights on after first lights off
# Number of body movement = total count of body flip
# Average room temperature =  sum(temperature)/n
# Average room humidity = sum(humidity)/n
# Average heart rate = sum (heart rate)/n
# Average heart rate variation = sum (heart rate variation/n)
if __name__ == '__main__':
    rem_eff = get_rem_effeciency()
    ave_hr_vari = get_ave_HR_variation()
    ave_hr = get_ave_HR()
    rem_latency =  get_rem_latency()
    n_flip =  get_flip_number()
    n_intermitten_wake = get_n_intermitten_awake()
    ave_temp =  get_avg_temp()
    ave_humi =  get_avg_humi()
    avg_breathing = get_avg_breathing()
    report_dict = {
        "REM sleep latency":rem_latency,
        "REM sleep efficiency":rem_eff,
        "Intermittent awaking":n_intermitten_wake,
        "Number of body movement":n_flip,
        "Average room temperature":ave_temp,
        "Average room humidity":ave_humi,
        "Average heart rate":ave_hr,
        "Average heart rate variation":ave_hr_vari,
        "Average breathing rate":avg_breathing
    }
    print(rem_eff,ave_hr_vari,ave_hr,rem_latency,n_flip, n_intermitten_wake, ave_temp, ave_humi)
    with open('report.csv', 'w') as f:
        for key in report_dict.keys():
            f.write("%s,%s\n" % (key, report_dict[key]))