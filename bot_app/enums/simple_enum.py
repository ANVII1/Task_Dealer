from enum import Enum

class AdresationGroups(str,Enum):
    Developers = "dev"
    SysAdmins = "sys"
    Analysts = "analysts"
    MasterAnalysts = "masteranalysts"

class TaskStates(str,Enum):
    inBacklog = "inBacklog" 
    Sprintfree = "inSprintfree"
    Urgentfree = "inUrgentfree"
    SprintinProgress = "SprintinProgress"
    UrgentinProgress = "UrgentinProgress"
    Closed = "ClosedTask"