import random
import time

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)
   

    return time.strftime(format, time.localtime(ptime))


def strTime(start,format='%m/%d/%Y %I:%M %p'):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    #stime = time.mktime(time.strptime(start, format))
    
    return time.strftime(format, time.localtime(time.mktime(time.strptime(start, format))))


def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)


t1 = randomDate("1/1/2010 1:30 PM", "12/12/2010 4:50 AM", random.random())
t2 = strTime("6/1/2010 1:30 PM")
t3 = strTime("12/1/2010 1:30 PM")
print t1
print t2
print t3
print t2 <= t1 <= t3