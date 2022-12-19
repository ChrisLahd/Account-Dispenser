# Manual timer
import asyncio

upTime = 0

async def upTimeUpdater():
    global upTime
    for _ in iter(int, 1):
        await asyncio.sleep(1)
        upTime += 1
        return upTime

def timeFormatter(size):
    for x in ['s', 'm', 'h', 'd', 'm']:
        if size < 60:
            SecMin = "%3.1f %s" % (size, x)
            return SecMin
        size /= 60

        if size < 24 and "Hr(s)" in SecMin:
            Hr = "%3.2f %s" % (size, x)
            return Hr
        size /= 24

        if size < 31 and "Day(s)" in Hr:
            Month = "%3.5f %s" % (size, x)
            return Month
        size /= 31

for _ in iter(int, 1):
    print(timeFormatter(asyncio.run(upTimeUpdater())))