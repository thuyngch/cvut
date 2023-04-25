# pip install ntplib, bs4
import datetime
import requests
from ntplib import NTPClient
from bs4 import BeautifulSoup
from datetime import date as localdate, timezone


# ------------------------------------------------------------------------------
#  utils
# ------------------------------------------------------------------------------
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}


def _website_1(is_visualize=False):
    # get time from website
    website = "https://www.worldtimeserver.com/current_time_in_VN.aspx"
    response = requests.get(website, headers=usr_agent)
    soup = BeautifulSoup(response.text, 'html.parser')
    website_datetime = soup.findAll(
        'div', {'class': 'local-time'})[0].contents[11].contents[0]
    week_date, month_date, year = website_datetime[1:].split(', ')
    month, date = month_date.split(' ')
    try:
        month = datetime.datetime.strptime(month, "%b").month
    except:
        month = datetime.datetime.strptime(month, "%B").month
    date = int(date)
    year = int(year)
    month = int(month)
    if is_visualize:
        print(f'data from {website} is: ', week_date, date, month, year)
    return week_date, date, month, year


def _website_2(is_visualize=False):
    # get time from website
    website = "https://www.timetemperature.com/asia/vietnam_time_zone.shtml"
    response = requests.get(website, headers=usr_agent)
    soup = BeautifulSoup(response.text, 'html.parser')
    website_datetime = soup.findAll('td', {'class': 'time-display'})[0]
    week_date = website_datetime.contents[6][1:]
    month, date, year = website_datetime.contents[8].split('/')
    date = int(date)
    month = int(month)
    year = int(year)
    if is_visualize:
        print(f'data from {website} is: ', week_date, date, month, year)
    return week_date, date, month, year


def _website_3(is_visualize=False):
    # try to take time from UTC
    client = NTPClient()
    response = client.request('europe.pool.ntp.org', version=3)
    c_time = datetime.datetime.fromtimestamp(
        response.tx_time, tz=timezone.utc).astimezone(tz=None)
    date, month, year = c_time.day, c_time.month, c_time.year
    if is_visualize:
        print(f'data from europe.pool.ntp.org is: ',  date, month, year)
    return (0, date, month, year)


def _check_online(start_date, valid_duration):
    return_dict = dict()
    # gettime from internet
    online_week_date, online_date, online_month, online_year = (
        None, None, None, None)
    temp_previous_online_time = None
    for idx, gettime in enumerate((_website_1, _website_2, _website_3)):
        try:
            _online_current_time = gettime()
            online_week_date, online_date, \
                online_month, online_year = _online_current_time
            if idx == 0:
                temp_previous_online_time = _online_current_time
                continue
            # ensure different websit have same time
            if _online_current_time[1:] != temp_previous_online_time[1:]:
                return_dict['valid'] = False
                return_dict['info'] = 'Online check | Times from websites are different'
                return return_dict
            temp_previous_online_time = _online_current_time
        except:
            continue

    if online_date is None:
        return_dict['valid'] = False
        return_dict['info'] = 'Online check | Cannot get time from websites'
        return return_dict

    online_release_date = datetime.datetime.strptime(
        start_date, "%Y-%m-%d")
    online_current_date = datetime.datetime.strptime(
        f'{online_year}-{online_month}-{online_date}', "%Y-%m-%d")

    # calculate valid time
    duration = (online_current_date-online_release_date).days
    if duration > valid_duration or duration < 0:
        return_dict['valid'] = False
        return_dict['info'] = f'Online check | Expired, current duration: {duration} ' \
            f'days which is less or exceed {valid_duration} days'
        return return_dict
    return_dict['valid'] = True
    return_dict['info'] = 'OK'
    return return_dict


def _check_local(start_date, valid_duration):
    return_dict = dict()
    # get time from local
    local_time = localdate.today()
    local_time = local_time.strftime("%Y-%m-%d")
    local_time = datetime.datetime.strptime(local_time, "%Y-%m-%d")
    # calculate valid time
    release_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    duration = (local_time-release_date).days
    if duration > valid_duration or duration < 0:
        return_dict['valid'] = False
        return_dict['info'] = f'Local check | Expired, current duration: {duration} '\
            f'days which is less or exceed {valid_duration} days'
        return return_dict
    # pass, ok
    return_dict['valid'] = True
    return_dict['info'] = 'OK'
    return return_dict


def check_expire(start_date, valid_duration, mode='local'):
    assert mode in ['local', 'web', 'both']
    if mode == 'web':
        return _check_online(start_date, valid_duration)
    elif mode == 'local':
        return _check_local(start_date, valid_duration)
    else:
        result_local = _check_local(start_date, valid_duration)
        result_online = _check_online(start_date, valid_duration)
        if not result_local['valid']:
            return result_local
        elif not result_online['valid']:
            return result_online
        else:
            return result_online


def validate_time_expire(start_date, duration, mode):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not check_expire(start_date, duration, mode)['valid']:
                raise ValueError("Time expiration")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ------------------------------------------------------------------------------
#  Main execution
# ------------------------------------------------------------------------------
def main():
    import argparse

    # ArgumentParser
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_date', type=str, default="2022-09-20")
    parser.add_argument('--valid_duration', type=int, default=3)
    parser.add_argument('--mode', type=str, default='local')
    args = parser.parse_args()

    print(check_expire(args.start_date, args.valid_duration, args.mode))


if __name__ == '__main__':
    main()
