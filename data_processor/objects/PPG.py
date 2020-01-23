class PPG:
    """A sample Employee class"""

    def __init__(self, bpm, time_stamp,id, dict):
        self.bpm = bpm
        self.time_stamp = time_stamp
        self.id = id
        self.ibi = dict['ibi']
        self.sdnn = dict['sdnn']
        self.sdsd = dict['sdsd']
        self.rmssd = dict['rmssd']
        self.pnn20 = dict['pnn20']
        self.pnn50 = dict['pnn50']
        self.hr_mad = dict['hr_mad']
        self.breathingrate = dict['breathingrate']