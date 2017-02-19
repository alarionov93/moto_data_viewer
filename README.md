# GET DATA FROM LOGS

## From 1st step - if there is new measures / else go to step 4
1. `cd Work/Electronics/dataViewer` and get `mdu.log` file
2. If no db exists, run `python migrate.py`
3. Put data into db with `python parser.py`
    - view the log file name in parser.py
    - `--force` option should be on 1st place (!)
    - add option `--new` if new measure_id needed (to divide this data from other, can be on the 2nd place)
    (adding this option tells the parser to create rows in db with next measure_id)
4. Start app with `./start.sh`
#### Don't forget about virtual env