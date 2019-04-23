#
# (c) 2019 NCC Group Plc
# Ollie Whitehouse - ollie [.] whitehouse @ nccgroup [.] com
# released under AGPL
# https://github.com/olliencc/Speed-of-light-test-data
#

from ipaddress import IPv4Address, IPv6Address
import random
from random import getrandbits
import time
from datetime import datetime
import pandas
from io import StringIO

# Global defines
strUserPrefix = "user"
lstEvents = ['AUTHSUCCESS']

# thank you stackoverflow - https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
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

# thank you stackoverflow - https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%d %H:%M', prop)


# thank you stackexchange - https://codereview.stackexchange.com/questions/200337/random-ip-address-generator
def randomIP(v):
    if v == 4:
        bits = getrandbits(32) # generates an integer with 32 random bits
        addr = IPv4Address(bits) # instances an IPv4Address object from those bits
        addr_str = str(addr) # get the IPv4Address object's string representation
    elif v == 6:
        bits = getrandbits(128) # generates an integer with 128 random bits
        addr = IPv6Address(bits) # instances an IPv6Address object from those bits
        # .compressed contains the short version of the IPv6 address
        # str(addr) always returns the short address
        # .exploded is the opposite of this, always returning the full address with all-zero groups and so on
        addr_str = addr.compressed 
    
    return addr_str

# format that it generates is as such
# 
def GenerateLogs(intEntries, strOutFile):

    lstLog = []

    lstLog.append("When,User,Event,IP")


    # event
    strEvent= lstEvents[0]

    
    intCount=0
    # generate some noise in the log
    print("[i] Generating " + str(intEntries) + " events")
    while intCount < intEntries:
        intCount+=1

        # generate a date
        strDateGen = randomDate("2019-04-09 0:00", "2019-12-01 23:59", random.random())

        # user
        strUserGen = strUserPrefix + str(random.randint(1,9999))

        # IP address
        strIPAddr = randomIP(4)
    
        lstLog.append(str(strDateGen) + "," + strUserGen + "," + strEvent + "," + str(strIPAddr))

    # generate some specific events for a user within 30 minute windows

    # random month
    strMon=str(random.randint(4,12))
    # random day
    strDay=str(random.randint(1,28))
    # random hour
    strHour=str(random.randint(0,23))
    # user who has been pwned
    strUserHax = strUserPrefix + str(random.randint(1,9999))

    print("[i] Peppering Event Logs for " + strUserHax + " on 2019-"+strMon+"-"+strDay+" @ " + strHour+":00 for an hour")
    intCount=0
    while intCount < 100:
        intCount+=1      

        # generate a date
        strDateGen = randomDate("2019-"+strMon+"-"+strDay+" "+strHour+":00", "2019-"+strMon+"-"+strDay+" "+strHour+":59", random.random())

        # IP address
        strIPAddr = randomIP(4)
    
        lstLog.append(str(strDateGen) + "," + strUserHax + "," + strEvent + "," + str(strIPAddr))

    # Convert to file like object
    fLike = StringIO("\n".join(lstLog))

    # Now sort the list
    print("[i] Sorting event log by date time")
    dateparse = lambda x: pandas.datetime.strptime(x, '%Y-%m-%d %H:%M')
    data = pandas.read_csv(fLike, header=0,parse_dates=['When'],date_parser=dateparse)
    data.sort_values(['When'], ascending= True,inplace=True)

    # Write it out
    data.to_csv(strOutFile,index=False)
    print("[i] Wrote " + strOutFile)

###############################
# Main entry point
###############################

if __name__ == "__main__":
    
    lstLog = GenerateLogs(100000,"sampledata.csv")

 