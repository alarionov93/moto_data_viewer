import models
import sys
import argparse

DEFAULT_LOG_FILENAME = 'mdu.log'

parser = argparse.ArgumentParser(description='Options for log parser')

parser.add_argument('--force', action='store_true', help='Not running without this option (because of auto run with start.sh)')#, required=True)
parser.add_argument('--new', action='store_true', help='Create new measure id')
parser.add_argument('--update', action='store_true', help='Update data (truncate log file to store only new values into db)')
parser.add_argument('--host', action='store', help='Host (temporary)')
parser.add_argument('--port', action='store', help='Port (temporary)')
parser.add_argument('run', action='store', help='Run (temporary)')
# TODO: host, port and run arguments appears by unknown reason from invokation od start.sh. 
# ArgumentParser shows an error if these arguments are not added to it. That's why they are here.
args = parser.parse_args()

# get values of args here
args = vars(args)

cursor = models.db.execute_sql('SELECT MAX(measure_id) FROM measures;')
res = cursor.fetchone()
print(res)
new_measure_id = None
if res[0] is not None:
    last_measure_id = int(res[0])
    if args.get("new") == True:
        new_measure_id = last_measure_id + 1
    if args.get("update") == True:
        # TODO: truncate log file here
        pass
else:
    last_measure_id = 0
# this argument is strongly needed, because of strange error on production:
# when run ./start.sh parser.py is running, too.
if  args.get("force") == True:

    try:
        with open(DEFAULT_LOG_FILENAME, "r") as f:
            import pdb
            pure_data = f.read()
            splitted_data = pure_data.split('NA;')
            for data in splitted_data:
                # temp = models.TemperatureOut(value=float(d.split("=")[1].split(";")[0]))
                # temp.save()
                # print(data)
                p_idx = data.find("P=")
                # p_delimiter_idx = data.find(";", p_idx)
                v_idx = data.find("V=")
                # v_delimiter_idx = data.find(";", v_idx)
                t_out_idx = data.find("T2=")
                # t_out_delimiter_idx = data.find(";", t_out_idx)
                t_eng_idx = data.find("T1=")
                ch_stat_idx = data.find("CHG=")
                ch_val_idx = data.find("CH=")
                # t_eng_delimiter_idx = data.find(";", t_eng_idx)
                # TODO: tracker chg info may not be in this data !
                if all([p_idx, v_idx, t_eng_idx, t_out_idx]):
                    # p_val = data[p_idx + 2 : p_delimiter_idx]
                    # v_val = data[v_idx + 2 : v_delimiter_idx]
                    # t_out_val = data[t_out_idx + 3 : t_out_delimiter_idx]
                    # t_eng_val = data[t_eng_idx + 3 : t_eng_delimiter_idx]
                    #
                    # print(p_val)
                    # print(v_val)
                    # print(t_out_val)
                    # print(t_eng_val)
                    splitted = data.split("\n")
                    for s in splitted:
                        if len(s) < 1:
                            splitted.remove(s)
                    if len(splitted) < 4:
                        print("error in data!\n")
                    else:
                        # print(splitted)
                        # TODO: VERY IMPORTANT !!! SEND CHG DATA FROM GPS TRACKER AT THE END OF MAIN LOOP !!!
                        # p_val = splitted[0][2:len(splitted[0])-1]
                        # v_val = splitted[1][2:len(splitted[1])-1]
                        # t_eng_val = splitted[2][3:len(splitted[2])-1]
                        # t_out_val = splitted[3][3:len(splitted[3])-1]
                        # ch_stat_val = splitted[4][4:len(splitted[4])-1]
                        # ch_val = splitted[5][3:len(splitted[5])-1]
                        ch_stat_val = None
                        ch_val = None
                        for s in splitted:
                            
                            if s.find("P=") != -1:
                                p_val = s[2:len(s)-1]
                                # print(p_val)
                            elif s.find("V=") != -1:
                                v_val = s[2:len(s)-1]
                                # print(v_val)
                            elif s.find("CH=") != -1:
                                ch_val = s[3:len(s)-1]
                                print(ch_val)
                            elif s.find("CHG=") != -1:
                                ch_stat_val = s[4:len(s)-1]
                                # print(ch_stat_val)
                            elif s.find("T1=") != -1:
                                t_eng_val = s[3:len(s)-1]
                                # print(t_eng_val)
                            elif s.find("T2=") != -1:
                                t_out_val = s[3:len(s)-1]
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
                            measure.save()
                            print("stored to db")
                else:
                    print("missing data!\n")

    except Exception as e:
        print(e)
else:
    print("Not run without `--force` option")