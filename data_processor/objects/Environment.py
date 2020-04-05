class Environment:
    def __init__(self,dict):
        self.time_stamp = dict['DateTime']
        self.id = dict['dict_id']
        self.Temperature = float(dict['Temperature'])
        self.Humidity = float(dict['Humidity'])
        self.Pressure = float(dict['Pressure'])
        self.Proximity = float(dict['Proximity'])
        self.r = float(dict['r'])
        self.g = float(dict['g'])
        self.b = float(dict['b'])
        self.Inst_breathing_rate = float(dict['Inst_breathing_rate'])
        self.Ave_breathing_rate = float(dict['Ave_breathing_rate'])

