from datetime import datetime, timezone

import ntplib
from fastapi import HTTPException, status


async def get_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('uz.pool.ntp.org')
        uzb_time = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
        return uzb_time
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to get time from NTP server")
