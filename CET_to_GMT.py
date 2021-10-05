from datetime import datetime, tzinfo, timedelta
now = datetime.now()
 
class CET(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1) + self.dst(dt)

    def dst(self, dt):
        dston = datetime(year=dt.year, month=3, day=20)
        dstoff = datetime(year=dt.year, month=10, day=20)
        if dston <= dt.replace(tzinfo=None) < dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return timedelta(0)

    def dst(self, dt):
        return timedelta(0)

def from_cet_to_gmt(year, month, day, hour, minute):
    cet = datetime(year, month, day, hour, minute, tzinfo=CET())
    utc = cet.astimezone(tz=UTC())
    #return '{:%Y-%m-%d:T%H:%MZ}'.format(utc)
    return '{:%m/%d/%Y %H:00:000}'.format(utc)


print(from_cet_to_gmt(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute))
# 2017-07-24:T08:30Z
