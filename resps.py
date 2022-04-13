import netschoolapi
from preparation.preparation import run_main
from preparation.utils import pprint
import datetime as dt


async def day_homework(client: netschoolapi.NetSchoolAPI):
    week = await client.diary(start=dt.date(2022, 4, 18))
    pprint(week.schedule[0].lessons[0])

if __name__ == '__main__':
    pass
    # run_main(main)

