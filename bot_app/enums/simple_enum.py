from enum import Enum

class AdresationGroups(str,Enum):
    Developers = "dev"
    SysAdmins = "sys"
    Analysts = "anal"
    MasterAnalysts = "Manal"

class TaskStates(str,Enum):
    inBacklog = "inBacklog" 
    Sprintfree = "inSprintfree"
    Urgentfree = "inUrgentfree"
    SprintinProgress = "SprintinProgress"
    UrgentinProgress = "UrgentinProgress"