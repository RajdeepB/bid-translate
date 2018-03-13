import calendar
import xml.etree.cElementTree as ET
import re
import time
import datetime
from datetime import timedelta
from datetime import date as d
from datetime import datetime as dt
from datetime import time as t
from datetime import timedelta as td

source_file = "D:/export_other_to_crew_bid_20FD_20180216_165528_baruar.xml"

source_xml = ET.parse(source_file)

def get_dates(s):
    """ input :
    output : """
    regex = r"wom:?\D+(\d+)"
    matches = re.findall(regex, s)
    s = calendar.monthcalendar(2017,)
    for match in range(0, len(matches)):
        print(str(s[match])+"Jan"+"2017")


def setPoints(points):
    """returns bid points as a string"""
    n = int(points)
    if n in [1, 49, 51, 99]:
        return str(n)+' '+'p'
    else:
        m = n % 10
        if n > 100:
            return str(100)+' '+'p'
        elif n < 10:
            return str(10)+' '+'p'
        elif m < 5:
            return str((n-m))+' '+'p'
        elif m >= 5:
            return str((n+(10-m)))+' '+'p'

def setPoints_lhcc(bidtype, preftype):
    """returns bid points as a string"""
    points=0
    if bidtype=='SPEC_PAIRING' and preftype=='BSD':
        points = 30
    elif bidtype=='SPEC_PAIRING' and preftype=='STOD':
        points = 100
    elif bidtype=='SPEC_DO':
        points = 99
    elif bidtype=='GOLDEN_DO':
        points = 10
    else:
        print('error translating lhcc bid points; bids outside of the type SPEC_PAIRING+BSD, SPEC_PAIRING+STOD, GOLDEN_DO, SPEC_DO')
    return (str(points)+' '+'p')


def setPairingLenMax(m):
    if int(m) == 99:
        return ''
    elif int(m) > 20:
        return str(20)
    else:
        return str(m)


def setMaxTimesRoster(n, d):  # returns max times roster as string
    if get_avoid(d) is True:
        return ''
    else:
        if str(n) in ['1', '2', '3', '4', '5', '6', '7']:
            return str(n)
        else:
            try:
                maxTimes = int(n)
                if maxTimes > 7:
                    return 'Max'
                elif maxTimes < 1:
                    return '1'
            except ValueError:
                return '1'


# input : '24-Jul-17' , '31JUL17 0955'
# output : date in a dd/mm/yy format
def conv_d(d):
    final_d = ''  # edited
    if d is not None:
        length = len((str(d).strip()))
        if (length >= 8) and (length <= 9):
            final_d = time.strptime(d, "%d-%b-%y")
        elif (length >= 10) and (length <= 12):
            final_d = time.strptime(d, "%d%b%y %H%M")
        elif (length >= 13) and (length <= 14):
            final_d = time.strptime(d, "%d%b%Y %H%M")
        return time.strftime("%d/%m/%y", final_d)
    else:
        return ''


def conv_d_2(bidtype, d):
    if d is not None:
        if bidtype in ['GEN_PAIRING', 'GEN_TIMEOFF', 'SPEC_DO', 'GOLDEN_DO']:
            final_d = time.strptime(d, "%d-%b-%y")
        elif bidtype in ['SPEC_TIMEOFF']:
            final_d = time.strptime(d, "%d%b%y %H%M")
        else:
            final_d = ''
        return time.strftime("%d/%m/%y", final_d)
    else:
        return ''


def conv_t(d):  # input : ;returns time in an hh:mm
    if d is not None:
        try:
            final_t = time.strptime(d, "%d%b%Y %H%M")
        except TypeError:
            final_t = time.strptime(d, "%d%b%y %H%M")
        finally:
            return time.strftime("%H:%M", final_t)
    else:
        return ''


def get_avoid(d):  # returns boolean
    av = str(d)
    if av in ['AGT', 'AST', 'ATDA']:
        return True
    else:
        return ''


def get_region(r):  # returns region
    regions = {'AUS': 'AUSTRALIA',
               'NAM': 'AMERICA',
               'ORI': 'ASIA',
               'NZ': 'NEW ZEALAND',
               'PAC': 'PACIFIC',
               'SAM': 'AMERICA'}
    if r is not None:
        return regions.get(r)
    else:
        return ''


# returns layover ports present in the JCR JCB export file in a list
def get_layoverData(tree):
    layovers = []
    for node in tree.iterfind(".//destinationdata/destinations"):
        destinationData = node.findall('destination')
        for node2 in destinationData:
            if node2.attrib['layover'] == "true":
                layovers.append(node2.attrib['airport'])
    return layovers


# returns transit ports present in the JCR JCB export file in a list;
# tree is the element tree created from xml file
def get_transitData(tree):
    transits = []
    for node in tree.iterfind(".//destinationdata/destinations"):
        destinationData = node.findall('destination')
        for node2 in destinationData:
            if node2.attrib['stop'] == "true":
                transits.append(node2.attrib['airport'])
    return transits


# checks for transit returns transit
def get_transit(t):
    transits = get_transitData(source_xml)
    if t is not None:
        if str(t).strip() in transits:
            return t
    else:
        return ''


# checks for transit returns transit
def get_layover(l):
    layovers = get_layoverData(source_xml)
    if l is not None:
        if str(l).strip() in layovers:
            return l
    else:
        return ''


def get_pax(s):
    px = str(s).strip()
    if px == "ON":
        return "PAX to home base"
    else:
        return ''


def group(L):
    if len(L) == 0:
        return (0, 0)
    else:
        first = last = L[0]
        for n in L[1:]:
            if (n - 1) == last:  # Part of the group, bump the end
                last = n
            else:  # Not part of the group, yield current group and start a new
                yield first, last
                first = last = n
        yield first, last  # Yield the last group


# returns dow in 3 letter day initials eg. 1 - Mon
def get_days_from_dow(s):
    s_stripped = "".join(s.split())
    if 'dow' in s_stripped:
        # print("I'm in")
        regex = r"dow:?\D+(\d+)"
        dow = re.findall(regex, s_stripped)  # returns array but for this case,
        # array will have 1 element only i.e at index 0
        dow_list = []
        for i in dow[0]:
            dow_list.append(int(i))
        return dow_list
    else:
        return []


# input : dow:67, wom:1234
# returns [1,2,3,4]
def get_weeks_from_wom(s):
    regex = r"\w+"
    dow_wom = re.findall(regex, s)
    s_stripped = "".join(dow_wom)
    if 'wom' in s_stripped:
        regex = r"wom:?(\d+)"
        wom = re.findall(regex, s_stripped)  # returns array but for this case,
        # array will have 1 element only i.e at index 0
        wom_list = []
        for i in wom[0]:
            wom_list.append(int(i))
        return wom_list
    else:
        return []


def get_end_date_time_from_duration(start, durn):
    duration = int(durn)
    stripped_time = time.strptime(start, '%d%b%Y %H%M')  # returns tuple
    start_date = datetime.datetime(stripped_time.tm_year,
                                   stripped_time.tm_mon,
                                   stripped_time.tm_mday,
                                   stripped_time.tm_hour,
                                   stripped_time.tm_min,
                                   stripped_time.tm_sec)

    end_date_time = start_date + timedelta(hours=duration)

    end_date_time_stripped = time.strptime(str(end_date_time),
                                           '%Y-%m-%d %H:%M:%S')

    end_date = time.strftime('%d/%m/%y', end_date_time_stripped)
    end_time = time.strftime('%H:%M', end_date_time_stripped)
    return [end_date, end_time]


# input '07JUL2017 0700', 1, 3
# output ['07/07/17', '27/07/17']
def get_start_end_date_from_wom(start_dt, x, y):
    stripped_time = time.strptime(start_dt, '%d%b%Y %H%M')  # returns tuple
    start_date = datetime.datetime(stripped_time.tm_year,
                                   stripped_time.tm_mon,
                                   stripped_time.tm_mday,
                                   stripped_time.tm_hour,
                                   stripped_time.tm_min,
                                   stripped_time.tm_sec)

    start_date_time = start_date + timedelta(days=x-1)*7
    end_date_time = start_date + timedelta(days=y)*7 - timedelta(days=1)

    start_date_time_stripped = time.strptime(str(start_date_time),
                                             '%Y-%m-%d %H:%M:%S')
    end_date_time_stripped = time.strptime(str(end_date_time),
                                           '%Y-%m-%d %H:%M:%S')

    start_date = time.strftime('%d/%m/%y', start_date_time_stripped)
    end_date = time.strftime('%d/%m/%y', end_date_time_stripped)

    return [start_date, end_date]


def get_start_end_date_2(start, x, y):
    stripped_time = time.strptime(start, '%d/%m/%y')  # returns tuple
    start_date = datetime.datetime(stripped_time.tm_year,
                                   stripped_time.tm_mon,
                                   stripped_time.tm_mday,
                                   stripped_time.tm_hour,
                                   stripped_time.tm_min,
                                   stripped_time.tm_sec)

    start_date_time = start_date + timedelta(days=x-1)*7
    end_date_time = start_date + timedelta(days=y)*7 - timedelta(days=1)

    start_date_time_stripped = time.strptime(str(start_date_time),
                                             '%Y-%m-%d %H:%M:%S')
    end_date_time_stripped = time.strptime(str(end_date_time),
                                           '%Y-%m-%d %H:%M:%S')

    start_date = time.strftime('%d/%m/%y', start_date_time_stripped)
    end_date = time.strftime('%d/%m/%y', end_date_time_stripped)

    return [start_date, end_date]


# generic timeoff
def get_time_off_params(bidtype, start_dt, duration, dow_wom):
    daydict = {"": "",
               1: "Mon", 2: "Tue", 3: "Wed",
               4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}
    data = []
    start_date = conv_d_2(bidtype, start_dt)
    # start_time = '00:00'
    end_time = duration[:-2]+':'+duration[-2:]

    dow_list = get_days_from_dow(dow_wom)
    dow_grp_list = list(group(dow_list))

    wom_list = get_weeks_from_wom(dow_wom)
    wom_grp_list = list(group(wom_list))

    for i in range(0, len(wom_grp_list)):
        for j in range(0, len(dow_grp_list)):
            start_end_date = get_start_end_date_2(start_date,
                                                  wom_grp_list[i][0],
                                                  wom_grp_list[i][1])
            day_from = dow_grp_list[j][0]
            day_to = dow_grp_list[j][1]

            data.append((start_end_date[0], start_end_date[1],
                         end_time, daydict[day_from], daydict[day_to]))

    return data


def get_port_spec_pair(s):
    port = str(s)
    return port[0:3]


def get_start_time_gen_timeoff(id, gen_timeoff_start_dict):
    start_time = gen_timeoff_start_dict[id]
    start_time_fr = start_time[0:2]+':'+start_time[2:4]
    return start_time_fr


def get_start_end_signon_signoff(from_dt, until_dt):
    """ returns from date, to date, sign-on from, sign-on to for SPEC_PAIRING bids
    with the 'from', 'until' fields from the Ventra file as args"""

    from_strp = time.strptime(from_dt, '%d%b%y %H%M')
    to_strp = time.strptime(until_dt, '%d%b%y %H%M')

    start_date = datetime.datetime(from_strp.tm_year, from_strp.tm_mon,
                                   from_strp.tm_mday, from_strp.tm_hour,
                                   from_strp.tm_min, from_strp.tm_sec)
    to_date = datetime.datetime(to_strp.tm_year, to_strp.tm_mon,
                                to_strp.tm_mday, to_strp.tm_hour,
                                to_strp.tm_min, to_strp.tm_sec)

    signon_from_datetime = start_date - timedelta(minutes=5)
    signon_to_datetime = start_date + timedelta(minutes=5)

    signon_from_datetime_strp = time.strptime(str(signon_from_datetime),
                                              '%Y-%m-%d %H:%M:%S')
    signon_to_datetime_strp = time.strptime(str(signon_to_datetime),
                                            '%Y-%m-%d %H:%M:%S')
    to_date_strp = time.strptime(str(to_date), '%Y-%m-%d %H:%M:%S')

    from_date = time.strftime('%d/%m/%y', signon_from_datetime_strp)
    to_date = time.strftime('%d/%m/%y', signon_to_datetime_strp)

    signon_from_time = time.strftime('%H:%M', signon_from_datetime_strp)
    signon_to_time = time.strftime('%H:%M', signon_to_datetime_strp)

    return [from_date, to_date, signon_from_time, signon_to_time]


def get_layover_transit(tod, lay):
    transit_list = get_transitData(source_xml)
    layover_list = get_layoverData(source_xml)
    port = str.strip(tod)
    lo = str.strip(lay)
    layover = ''
    transit = ''

    if (port != '') and (lo != ''):
        if (port in transit_list) and (lo in layover_list):
            if port == lo:
                transit = ''
                layover = lo
            else:
                transit = port
                layover = lo
        elif (port not in transit_list) and (lo in layover_list):
            if port == lo:
                transit = ''
                layover = lo
            else:
                transit = port
                layover = lo
        elif (port in transit_list) and (lo not in layover_list):
            if port == lo:
                transit = port
                layover = ''
            else:
                transit = port
                layover = lo
        elif (port not in transit_list) and (lo not in layover_list):
            transit = 'error'
            layover = 'error'
    elif (port != '') and (lo == ''):
        if (port in transit_list):
            transit = port
            layover = ''
        elif (port in layover_list):
            transit = ''
            layover = port
        elif (port not in transit_list) and (port not in layover_list):
            transit = 'error'
            layover = 'error'
    elif (port == '') and (lo != ''):
        if (lo in layover_list):
            transit = ''
            layover = lo
        elif (lo in transit_list):
            transit = lo
            layover = ''
        elif (lo not in transit_list) and (lo not in layover_list):
            transit = 'error'
            layover = 'error'
    elif (port == '') and (lo == ''):
        transit = ''
        layover = ''

    return [layover, transit]


def get_end_time(s, durn):
    # stripped_time = time.strptime(start, '%H%M') #returns tuple
    start = str(s)
    start_time = t(int(start[:-2]), int(start[-2:]))

    end_time = dt.combine(d.today(), start_time) + td(hours=int(durn))

    end_time_fr = str(end_time.time())[0:5]
    start_time_fr = str(start_time)[0:5]

    return [start_time_fr, end_time_fr]


def get_layover_min_max(min, max):
    mn = int(min)
    mx = int(max)
    if mn < 1:
        mn = 1
    elif mn > 20:
        mx = 20
    return[str(mn), str(mx)]


def get_dow_list(date1, date2, dow):
    "for MHCC generic bids "
    start_date = dt.strptime(date1, '%d-%b-%y').date()
    end_date = dt.strptime(date2, '%d-%b-%y').date()
    a = []
    b = get_days_from_dow(dow)

    date_range = [
        d.fromordinal(ordinal)
        for ordinal in range(
            start_date.toordinal(),
            end_date.toordinal()+1,
        )
    ]
    for i in range(len(date_range)):
        a.append(date_range[i].isoweekday())

    set_a= set(a)
    set_b = set(b)
    set_c = set_a.intersection(set_b)
    list_d = list(group(list(set_c)))
    return list_d


def getSpecRuleRelax(x):
    if x=='TRUE':
        return 'Yes'

# def conv_d_3(d):
#     final_d = ''  # edited
#     if d is not None:
#         if time.strptime(d, "%d-%b-%y"):
#
#         length = len((str(d).strip()))
#         if (length >= 8) and (length <= 9):
#             final_d = time.strptime(d, "%d-%b-%y")
#         elif (length >= 10) and (length <= 12):
#             final_d = time.strptime(d, "%d%b%y %H%M")
#         elif (length >= 13) and (length <= 14):
#             final_d = time.strptime(d, "%d%b%Y %H%M")
#         return time.strftime("%d/%m/%y", final_d)
#     else:
#         return ''

