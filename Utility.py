import datetime
from datetime import datetime as dt


def show_limits(limit, remaining, seconds_to_reset):
    print ("*")*100
    print 'limit               = ' + str(limit)
    print 'remaining requests  = ' + str(remaining)
    tt = str(datetime.datetime.fromtimestamp(seconds_to_reset).time())
    n = dt.now().time()
    now = ('%s:%s:%s'%(n.hour, n.minute,n.second))[:8]
    now_time = dt.strptime(now, '%H:%M:%S')
    reset_time =  dt.strptime(tt, '%H:%M:%S')
    print 'time to reset limit = ' + str(reset_time - now_time)
    print ("*")*100
