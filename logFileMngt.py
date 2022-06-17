
dict_video2radar = {'highway.mp4':"Record_2021-12-05_11-31-31.someip.ars540.hex",
                    'bicycle.mp4':"Record_2021-10-14_16-43-39.someip.ars540.hex"}

radar_logfile_path = ""#"./"

class RadarLogFileInfo():
    def __init__(self, log_file_name):
        self.log_file_name = log_file_name
        self.log_full_file_path = radar_logfile_path + log_file_name
        file = open(self.log_full_file_path, "r")
        self.fileLines = file.readlines()
        self.log_file_size = len(self.fileLines)
        self.currLineNr = 0

    def getPrograss(self):
        return self.currLineNr/self.log_file_size

    def get_current_line(self):
        if self.currLineNr < self.log_file_size:
            return self.fileLines[self.currLineNr]


    def next_line(self):
        if self.currLineNr < self.log_file_size:
            self.currLineNr += 1

    def get_data_bytes(self):
        bytes_data = bytes.fromhex(self.get_current_line())
        line_len = len(bytes_data)

        if line_len > 10000:
            pcl_dataBytes = bytes_data
            while line_len > 10000:
                pcl_dataBytes = bytes_data
                self.currLineNr += 1
                bytes_data = bytes.fromhex(self.get_current_line())
                line_len = len(bytes_data)
            obj_dataBytes = bytes_data
        else:
            while line_len < 10000:
                self.currLineNr += 1
                pcl_dataBytes = bytes.fromhex(self.get_current_line())
                line_len = len(pcl_dataBytes)
            while line_len > 10000:
                self.currLineNr += 1
                obj_dataBytes = bytes.fromhex(self.get_current_line())
                line_len = len(obj_dataBytes)
        return pcl_dataBytes, obj_dataBytes




