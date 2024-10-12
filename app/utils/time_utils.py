from datetime import datetime
import time
import pytz

import ntplib


SAMARKAND_TZ = pytz.timezone("Asia/Samarkand")


async def get_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('uz.pool.ntp.org', version=3)
        uzb_time = time.localtime(response.tx_time)
        uzb_time = datetime.fromtimestamp(time.mktime(uzb_time))
        return uzb_time
    except Exception as e:
        print("Failed to get time from NTP server")
        return datetime.now(SAMARKAND_TZ).replace(tzinfo=None)


def get_time_sync():
    try:
        client = ntplib.NTPClient()
        response = client.request('uz.pool.ntp.org', version=3)
        uzb_time = time.localtime(response.tx_time)
        uzb_datetime = datetime.fromtimestamp(time.mktime(uzb_time))
        return uzb_datetime
    except Exception as e:
        print("Failed to get time from NTP server")
        return datetime.now(SAMARKAND_TZ).replace(tzinfo=None)
