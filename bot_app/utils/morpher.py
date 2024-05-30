from enums.simple_enum import AdresationGroups 

def adresationGroupToName(adresationGroup:AdresationGroups):
    name = ""
    match adresationGroup:
        case AdresationGroups.Developers:
            name = "Разработчик"
        case AdresationGroups.Analysts:
            name = "Аналитик"
        case AdresationGroups.MasterAnalysts:
            name = "Ведущий аналитик"        
        case AdresationGroups.SysAdmins:
            name = "Ситемный Администртор"

    return name
            
