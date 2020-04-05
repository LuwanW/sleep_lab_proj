class PPG:
    """A sample Employee class"""

    def __init__(self, bpm, time_stamp,id, dict):
        self.bpm = bpm
        self.time_stamp = time_stamp
        self.id = id
        if dict == {}:
            self.ibi = 0
            self.sdnn = 0
            self.sdsd =0
            self.rmssd =0
            self.pnn20 = 0
            self.pnn50 =0
            self.hr_mad = 0
            self.breathingrate = 0
        else:
            self.ibi = dict['ibi']
            self.sdnn = dict['sdnn']
            self.sdsd = dict['sdsd']
            self.rmssd = dict['rmssd']
            self.pnn20 = dict['pnn20']
            self.pnn50 = dict['pnn50']
            self.hr_mad = dict['hr_mad']
            self.breathingrate = dict['breathingrate']