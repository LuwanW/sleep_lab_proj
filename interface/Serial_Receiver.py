import serial
import datetime
class Serial_Receiver:
    def __init__(self, com):
        self.usbport =com
        self.ser = serial.Serial(self.usbport, 9600)
        self.data_dict = {
            'DateTime': 0,
            id:0
        }

    def get_data(self):
        dict_id = 0
        while 1:
            dict_id += 1
            RawData = self.ser.readline().decode(encoding='UTF-8')
            #temp = RawData.splitlines()[0]
            #self.data_dict['temp'] = temp
            datas = RawData.splitlines()[0].split(",")
            self.data_dict['Temperature'] = datas[1]
            self.data_dict['Humidity'] = datas[2]
            self.data_dict['Pressure'] = datas[3]
            self.data_dict['Proximity'] = datas[4]
            self.data_dict['r'] = datas[5]
            self.data_dict['g'] = datas[6]
            self.data_dict['b'] = datas[7]
            this_data_time =datetime.datetime.now()
            self.data_dict['DateTime'] = this_data_time.strftime("%m-%d-%Y %H:%M:%S")
            self.data_dict['dict_id'] = dict_id
            yield self.data_dict

if __name__ == '__main__':
    s = Serial_Receiver('COM9')
    # COM3 for the temp sensor one
    for data in s.get_data():
        print(data)