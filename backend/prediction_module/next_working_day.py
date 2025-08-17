import numpy as np
import datetime

def next_working_day(date):
    next_day = np.busday_offset(date, 1, roll='forward')
    next_working_day = np.datetime64(next_day).astype(datetime.date)
    return next_working_day

