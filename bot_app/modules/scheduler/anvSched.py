import datetime as dt
import asyncio
from modules.data import TaskCollection
import types
from modules.logging import logger as l
import dateutil.rrule as rr
from modules.scheduler.reglaments import *

_log_dir = "modules-scheduler " 

# helper func
def _reglament_to_next_date(reglament:dict) -> dt.datetime:
    """
    takes dict (reglament)
    exmample:
        {
            "time" : "10:10",
            "weekdays" : [1,6] # monday and saturday
        }
    another example:
        {
            "time" : "22:15",
            "on_date" : "12.11"
        }
    weekays and on_date in conflict, you can choose only one mode, weekly or on date
    late maybe add monthly (every month)

    """
    reg_keys = reglament.keys()

    list_of_dates:list = []

    now = dt.datetime.now()

    reglament_start_dt = dt.datetime(
        hour=int(str(reglament["time"]).split(":")[0]),
        minute=int(str(reglament["time"]).split(":")[1]),
        day= now.day,
        month = now.month,
        year = now.year
    )

    if "on_date" in reg_keys and "weekdays" in reg_keys:
        e = "reglament can by or dately or weekly"
        l.exc(_log_dir + f" {e}")
        raise ValueError(e)

    elif not ("on_date" in reg_keys) and not ("weekdays" in reg_keys):
        # on time only
        return reglament_start_dt if reglament_start_dt > now else reglament_start_dt + dt.timedelta(days=1)
    
    elif "on_date" in reg_keys:
        # dately
        split_date = str(reglament["on_date"]).split(".")
        reglament_start_dt = reglament_start_dt.replace(day=int(split_date[0]),month=int(split_date[1]))
        for date in rr.rrule(rr.MONTHLY,dtstart=reglament_start_dt,count=4):
            list_of_dates.append(date) 

    elif "weekdays" in reg_keys:
        # weekly
        for weekday in reglament["weekdays"]:
            startday = (reglament_start_dt - dt.timedelta(days=now.isoweekday())) + dt.timedelta(weekday)
            
            for date in rr.rrule(rr.WEEKLY,dtstart=startday,count=2):
                if date < now:
                    continue
                list_of_dates.append(date)

    list_of_dates.sort()
    return list_of_dates[0]

    
async def _loop() -> None:
    while True:
        await asyncio.sleep(1)
        
        tasklist = TaskCollection.get_for_execute()
        if tasklist is None:
            continue

        for task in tasklist:
            try:
                func = globals()[task["func_name"]]
                            
                if type(task["args"]) is list or tuple:
                    await func(*task["args"]) 
                elif task["args"] is None:
                    await func()
                else:
                    await func(task["args"][0])                       
            except Exception as e:
                l.exc(f"{_log_dir} {e}")
                TaskCollection.remove(task)                        
            
            else:    
                # update next date
                if "reglament" in task.keys():
                    next_time = _reglament_to_next_date(task["reglament"])
                    TaskCollection.update_exec_time(task, next_time)
                else:
                    TaskCollection.remove(task)
                 

async def newTask(target:types.FunctionType|str, time:str=None, reglament:dict=None,args:list[str]|tuple[str]|str=()):
    """
    target - is function, takes func's only from global and only from reglament tasks module
    """
    if not isinstance(target,types.FunctionType) and not isinstance(target,str):
        l.exc(_log_dir +  "Scheduler ::: sended unreachable target")
        return
    
    if isinstance(target,types.FunctionType):
        target :str = target.__name__
    
    reglament_for_calc_next:dict = {}

    if (time is None) and reglament is None:
        l.err(_log_dir + "time is not defined")
        raise ValueError(" you must define time explicitly as parametr or in reglament dict")

    if (time is None) and reglament is not None:
        reglament_for_calc_next["time"] = reglament["time"]
    else:
        reglament_for_calc_next["time"] = time
        
    if reglament is not None: 
        for val in reglament.keys():                
            reglament_for_calc_next[val] = reglament[val]
    
    next_time = _reglament_to_next_date(reglament_for_calc_next)                    
    TaskCollection.new(target,next_time,reglament,[*args])

    l.inf(_log_dir + f"Planned new task ::: target - {target}")


async def init() -> None:
    asyncio.ensure_future(_loop(),loop=asyncio.get_running_loop())
    l.inf(_log_dir + "schedule loop is runing async")