# GET DATA FROM LOGS

## From 1st step - if there is new measures / else go to step 4
1. `cd Work/Electronics/dataViewer` and get `mdu.log` file
2. If no db exists, run `python migrate.py`
    Alternatively the SQL statement `INSERT INTO measures (measure_id,temp_out,temp_eng,pressure,voltage,fuel,gps_charge_stat,gps_charge_val,created_at) VALUES (1,10,10,10,10,10,0,10, NOW());`
    could be used after creating db.
3. Put data into db with `python parser.py run [other args]`
    - view the log file name in parser.py
    - `--force` option is required
    	(because of ./start.sh script invokes parser.py by inexplicable reason)
    - add option `--new` if new measure_id needed to divide this new data from other
    	(this option tells the parser to create rows in db with last_measure_id + 1)
    - `--truncate` option tells the parser to truncate log file to store only new values from it into db and exit script
    ## Important: only one of options (`--new` and `--truncate`) could be passed !!!
4. Start app with `./start.sh`
#### Don't forget about virtual env

To initiate getting data from BT execute `cat /dev/tty.HC-05-DevB >> ~/Work/Electronics/dataViewer/mdu.log`
