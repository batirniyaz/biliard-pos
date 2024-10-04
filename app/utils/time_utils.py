from datetime import datetime
import time

import ntplib
from fastapi import HTTPException, status


async def get_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('uz.pool.ntp.org', version=3)
        uzb_time = time.localtime(response.tx_time)
        time_string = time.strftime("%H:%M:%S", uzb_time)
        date = time.strftime("%Y-%m-%d", uzb_time)
        return time_string, date, uzb_time
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get time from NTP server")


def get_time_sync():
    try:
        client = ntplib.NTPClient()
        response = client.request('uz.pool.ntp.org', version=3)
        uzb_time = time.localtime(response.tx_time)
        return uzb_time
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get time from NTP server")
