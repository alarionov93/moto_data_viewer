import const
import models


class LogParser(object):
    """docstring for LogParser
       Parser for log files for MDU (try to use it not only in this project)
    """
    def __init__(self, log_file_name=const.DEFAULT_LOG_FILENAME):
        super(LogParser, self).__init__()
        self.log_file_name = log_file_name

    def parse(self, new_measure=False, truncate_log=False):
        cursor = models.db.execute_sql('SELECT MAX(measure_id) FROM measures;')
        res = cursor.fetchone()

        new_measure_id = None
        if res[0] is not None:
            print('Current measure id: %s' % res[0])
            last_measure_id = int(res[0])
            if new_measure:
                new_measure_id = last_measure_id + 1
        else:
            last_measure_id = 0
        try:
            with open(self.log_file_name, "r") as f:
                import pdb
                pure_data = f.read()
                splitted_data = pure_data.split('NA;')
                for data in splitted_data:
                    p_idx = data.find("P=")
                    v_idx = data.find("V=")
                    t_out_idx = data.find("T2=")
                    t_eng_idx = data.find("T1=")
                    ch_stat_idx = data.find("CHG=")
                    ch_val_idx = data.find("CH=")
                    # TODO: tracker chg info may not be in this data !
                    if all([p_idx, v_idx, t_eng_idx, t_out_idx]):
                        splitted = data.split("\n")
                        for s in splitted:
                            if len(s) < 1:
                                splitted.remove(s)
                        if len(splitted) < 4:
                            print("error in data!\n")
                        else:
                            ch_stat_val = None
                            ch_val = None
                            p_val = None
                            v_val = None
                            t_eng_val = None
                            t_out_val = None
                            fuel_val = None
                            for s in splitted:

                                if s.find("P=") != -1:
                                    p_val = s[2:len(s) - 1]
                                # print(p_val)
                                elif s.find("V=") != -1:
                                    v_val = s[2:len(s) - 1]
                                # print(v_val)
                                elif s.find("CH=") != -1:
                                    ch_val = s[3:len(s) - 1]
                                    print(ch_val)
                                elif s.find("CHG=") != -1:
                                    ch_stat_val = s[4:len(s) - 1]
                                # print(ch_stat_val)
                                elif s.find("T1=") != -1:
                                    t_eng_val = s[3:len(s) - 1]
                                # print(t_eng_val)
                                elif s.find("T2=") != -1:
                                    t_out_val = s[3:len(s) - 1]
                                elif s.find("F=") != -1:
                                    fuel_val = s[2:len(s) - 1]
                                # print(t_out_val)
                                else:
                                    print("no data found")
                            if all([p_val, v_val, t_eng_val, t_out_val]):
                                # print("all values catched")
                                measure = models.Measures(temp_out=float(t_out_val))
                                if new_measure_id:
                                    measure.measure_id = new_measure_id
                                elif last_measure_id:
                                    measure.measure_id = last_measure_id
                                else:
                                    print("last or new measure id is not defined")
                                measure.temp_eng = float(t_eng_val)
                                measure.voltage = float(v_val)
                                measure.pressure = float(p_val)
                                if ch_stat_val:
                                    measure.gps_charge_stat = int(ch_stat_val)
                                if ch_val:
                                    measure.gps_charge_val = int(ch_val)
                                if fuel_val:
                                    measure.fuel = int(fuel_val)
                                measure.save()
                                print("stored to db")
                    else:
                        print("missing data!\n")

            if truncate_log == True and new_measure == False:
                # TODO: truncate log file here
                with open(self.log_file_name, "w") as f:
                    f.truncate()
                    print("logs truncated!")
        except Exception as e:
            print(e)
