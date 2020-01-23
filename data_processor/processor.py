from interface.Serial_Receiver import Serial_Receiver
from data_processor.objects.PPG import PPG
from data_processor.objects.Environment import Environment
from data_processor.objects.REM import REM
from data_processor.objects.position import Position
from modules.position_detection import PositionDetection
from modules.REM_analysis import REM_analysis as ra
import heartpy as hp
import numpy as np
import sqlite3
from interface.Lithic_Receiver import Lithic_Receiver
import json
from threading import Thread
'''
to view l_data in db:
	sqlite3 sleep_lab.db
	SELECT * FROM heart_info;
	.quit
'''


class Processor_lithic:

    def __init__(self):
        self.lithic_receiver = Lithic_Receiver()

        self.ppg_list = list()

        self.position_x = list()
        self.position_y = list()
        self.position_z = list()
        self.REM_list = list()

        # set up for database
        self.conn = sqlite3.connect('sleep_lab.db')
        self.c1 = self.conn.cursor()




        # if table exists, delete and recreate
        self.c1.execute(''' SELECT count(name) FROM sqlite_master WHERE \
        type='table' AND name='heart_info' ''')
        
        if self.c1.fetchone()[0] == 1:
            print('Table exists, delete first')
            self.c1.execute('''
            DROP TABLE heart_info
            ''')
            self.conn.commit()
        
        self.c1.execute(''' SELECT count(name) FROM sqlite_master WHERE \
        type='table' AND name='position_info' ''')
        
        if self.c1.fetchone()[0] == 1:
            print('Table exists, delete first')
            self.c1.execute('''
            DROP TABLE position_info
            ''')
            self.conn.commit()

        self.c1.execute(''' SELECT count(name) FROM sqlite_master WHERE \
        type='table' AND name='rem_info' ''')

        if self.c1.fetchone()[0] == 1:
            print('Table exists, delete first')
            self.c1.execute('''
            DROP TABLE rem_info
            ''')
            self.conn.commit()


        # create heart_info table
        self.c1.execute('''CREATE TABLE heart_info(
            bpm FLOAT,
            time_stamp text,
            id INTEGER,
            ibi FLOAT,
            sdnn FLOAT,
            sdsd FLOAT,
            rmssd FLOAT,
            pnn20 FLOAT,
            pnn50 FLOAT,
            hr_mad FLOAT,
            breathingrate FLOAT
        )''')
        self.conn.commit()
        '''            
            
        '''

        # create motion info table
        self.c1.execute('''CREATE TABLE position_info(
            position text,
            time_stamp text,
            id INTEGER
        )''')
        self.conn.commit()

        # create motion info table
        self.c1.execute('''CREATE TABLE rem_info(
            eye_movement text,
            time_stamp text,
            id INTEGER
        )''')
        self.conn.commit()

        
        # set up position
        order = 6
        fs = 500.0  # sample rate, Hz
        cutoff = 1  # desired cutoff frequency of the filter, Hz
        self.posi = PositionDetection(order, fs, cutoff)
    

    def insert_position_info(self, position):
        with self.conn:
            self.c1.execute("INSERT INTO position_info VALUES (:position, :time_stamp, :id)", {'position': position.position,
                                                                                    'time_stamp': position.time_stamp,
                                                                                    'id': position.id})
    


    def insert_heart_info(self, PPG):
        with self.conn:
            self.c1.execute("INSERT INTO heart_info VALUES (:bpm, :time_stamp, :id, :ibi, :sdnn, :sdsd, :rmssd,\
                             :pnn20,:pnn50,:hr_mad,:breathingrate)",
                                    {'bpm': PPG.bpm,
                                  'time_stamp': PPG.time_stamp,
                                    'id': PPG.id,
                                     'ibi': PPG.ibi,
                                  'sdnn': PPG.sdnn,
                                  'sdsd': PPG.sdsd,
                                  'rmssd': PPG.rmssd,
                                  'pnn20': PPG.pnn20,
                                  'pnn50': PPG.pnn50,
                                  'hr_mad': PPG.hr_mad,
                                  'breathingrate': PPG.breathingrate})

    def insert_rem_info(self, REM):
        with self.conn:
            self.c1.execute("INSERT INTO rem_info VALUES (:eye_movement, :time_stamp, :id)", {'eye_movement': REM.eye_movement,
                                                                                              'time_stamp': REM.time_stamp,
                                                                                 'id':REM.id})

    
    
    def get_position_info(self, acc_x_data, acc_y_data, acc_z_data,time, id):
        # 5000*4 = 20 seconds
        seconds = 5
        points = seconds / 0.004

        if len(self.position_x) >= points:
            filtered_x, filtered_y, filtered_z =  self.posi.filter( self.position_x,
                                                                    self.position_y,
                                                                    self.position_z)
            measures = self.posi.get_posture(filtered_x, filtered_y, filtered_z, 5)
    
            position_obj = Position(measures, time, id)
            self.insert_position_info(position_obj)
            print(measures)
            self.position_x.clear()
            self.position_y.clear()
            self.position_z.clear()
            return measures
    
        self.position_x.append(acc_x_data)
        self.position_y.append(acc_y_data)
        self.position_z.append(acc_z_data)
        return 0
    
    
    def get_ppg_info(self, ppg_data,time, id):
        # 5000*4 = 20 seconds
        seconds = 15
        points = seconds / 0.004
        bpm = 0
        measures = {}
        ppg = {}
        if len(self.ppg_list) >= points:
            try:
                working_data, measures = hp.process(np.array(self.ppg_list), 250.0)
                bpm = measures['bpm']
                print(measures)
            except:
                print('bad signal, continue')
            self.ppg_list.clear()
            if measures != {}:
                ppg = PPG(bpm, time,id,measures)
                self.insert_heart_info(ppg)
                print(ppg.bpm)
            return ppg
    
        self.ppg_list.append(float(ppg_data))
        return 0


    def get_REM_info(self, rem_data, time, id):
        R = ra()
        if len(self.REM_list) >= 500:
            prediction = R.classify(self.REM_list, "D:\\4th_year\sleep_lab\sleep_lab\modules\SVM_model.sav")
            if prediction[0] == 0:
                move = 'steady'
            else:
                move = 'moving'
            print('prediction',move)
            this_REM = REM(move, time, id )
            self.insert_rem_info(this_REM)
            self.REM_list.clear()
        self.REM_list.append(float(rem_data))
        return 0



    def update_lithic(self):
        live_id = 0
        data_json = {'id': [0], 'heart_raw': [0]}

        while 1:
            lithic_data_list = self.lithic_receiver.get_data()
            # for l_data, s_data in zip(lithic_data_list,serial_data_list):
            for l_data in lithic_data_list:
                #print(l_data)
                '''
                # process live
                if live_id == 0:
                    data_json = {'id': [0], 'heart_raw': [0]}
                    with open('live.txt', 'w') as outfile:
                        json.dump(data_json, outfile)
                    live_id = 1
                elif live_id > 1000:
                    data_json['id'] = []
                    data_json['heart_raw'] = []
                    if 'id' not in data_json.keys():
                        continue
                    with open('live.txt', 'a') as outfile:
                        json.dump(data_json, outfile)
                        outfile.write('\n')
                    live_id = 1
                else:
                    data_json['id'].append(live_id)
                    data_json['heart_raw'].append(float(l_data['Analog1_chA']))
                    if 'id' not in data_json.keys():
                        continue
                    with open('live.txt', 'a') as outfile:
                        json.dump(data_json, outfile)
                        outfile.write('\n')
                    live_id = live_id + 1
                '''

                REM = self.get_REM_info(l_data['Analog1_chA'], l_data['DateTime'], l_data['Timestamp'])


                # process position
                position = self.get_position_info(float(l_data['IMU1_acc_x']), float(l_data['IMU1_acc_y']),
                                               float(l_data['IMU1_acc_z'])
                                               , l_data['DateTime'], l_data['Timestamp'])
                ppg = self.get_ppg_info(l_data['Analog2_chA'], l_data['DateTime'], l_data['Timestamp'])





class Processor_serial:

    def __init__(self):
        self.serial_receiver = Serial_Receiver('COM9')

        # set up for database
        self.conn = sqlite3.connect('sleep_lab_serial.db')
        self.c2 = self.conn.cursor()



        self.c2.execute(''' SELECT count(name) FROM sqlite_master WHERE \
        type='table' AND name='env_info' ''')

        if self.c2.fetchone()[0] == 1:
            print('Table exists, delete first')
            self.c2.execute('''
            DROP TABLE env_info
            ''')
            self.conn.commit()


        # create temp table
        self.c2.execute('''CREATE TABLE env_info(
            Temperature FLOAT,
            time_stamp text,
            Humidity FLOAT,
            Proximity FLOAT,
            Pressure FLOAT,
            r FLOAT,
            g FLOAT,
            b FLOAT,
            id INTEGER
        )''')
        self.conn.commit()

    def insert_env_info(self, env):
        with self.conn:
            self.c2.execute("INSERT INTO env_info VALUES (:Temperature, :time_stamp, :Humidity, \
                            :Proximity, :Pressure, :r, :g, :b,:id)",
                            {'Temperature': env.Temperature,
                             'time_stamp': env.time_stamp,
                             'Humidity': env.Humidity,
                             'Proximity': env.Proximity,
                             'Pressure': env.Pressure,
                             'r': env.r,
                             'g': env.g,
                             'b': env.b,
                             'id': env.id})

    def get_env_info(self, env_dict):
        temp = Environment(env_dict)
        self.insert_env_info(temp)
        return temp


    def update_serial(self):
        while 1:
            serial_data_list = self.serial_receiver.get_data()
            # for l_data, s_data in zip(lithic_data_list,serial_data_list):
            for s_data in serial_data_list:
                env = self.get_env_info(s_data)



if __name__ == '__main__':
    def p1():
        P1 = Processor_lithic()
        P1.update_lithic()
    Thread(target=p1).start()


    def p2():
        P2 = Processor_serial()
        P2.update_serial()

    Thread(target=p1).start()
    Thread(target=p2).start()
