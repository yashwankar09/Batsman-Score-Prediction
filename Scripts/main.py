from web_scapper import Extactor
import sys
import batting_data_clean as batrun
import bowling_data_clean as bowlrun

path = sys.argv
ext = Extactor(path[1])

try:
    ext.run()
    batrun.run()
    bowlrun.run()
    print('Data Loaded.')
except Exception as e:
    print('Failed',e)
    