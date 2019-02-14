import time

def time_to_date(timestamp):
    """
    timestamp to date.
    :param timestamp :int,e.g.1537535021
    :return:Year-Month-Day Hour:Minute:Second
    """
    timearr = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timearr)
    return  otherStyleTime