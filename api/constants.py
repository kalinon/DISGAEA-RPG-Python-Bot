from enum import IntEnum


class Constants:
    Current_Raid_ID = 89
    Current_Raid_Event_Point_Gacha = 28
    Current_Raid_Innocent_Regular_Roulette = 29
    Current_Raid_Innocent_Special_Roulette = 30
    Current_Raid_Normal_Boss_ID = 891
    Current_Raid_Badass_Boss_ID = 892
    Current_Story_Event_ID = 866
    Current_Bingo_ID = 2
    Current_Sugoroku_Event_ID = 0
    Item_Survey_Deposit_Size = 10
    Weapon_Full_Error = 'Weapon Slot is full\nPlease expand slot or sell weapons'
    Armor_Full_Error = 'Armor Slot is full\nPlease expand slot or sell armor'
    Shop_Max_Free_Refresh = 5
    Highest_Tower_Level = 50
    Alchemy_Alchemize_Cost = 6000
    Alchemy_Realchemize_Cost = 12000
    Unique_Innocent_Character_ID = 0
    Equipment_Alchemy_Effects = [10001, 20003, 20004, 20005, 30035, 30047, 30048, 30049, 30050, 30051, 30052, 30053,
                                 30054]
    Weapon_Alchemy_Effects = [10001, 20001, 20002, 30001, 30002, 30003, 30004, 30005, 30006, 30007, 30019, 30020, 30022,
                              30023]
    Place_1_Effects = [10001]
    Place_2_Effects = [20001, 20002, 20003, 20004, 20005]

    session_id = ''  # FILL SESSION_ID HERE
    user_id = ''  # FILL USER_ID HERE
    ticket = ''  # FILL TICKET FOR STEAM LOGIN


class Raid_Gacha_ID(IntEnum):
    SUMMER_PRINNY_EVENT_POINT = 49
    SUMMER_PRINNY_INNOCENT_REGULAR_ROULETTE = 50
    SUMMER_PRINNY_INNOCENT_SPECIAL_ROULETTE = 51
    MAKAI_KINGDOM_EVENT_POINT = 52
    MAKAI_KINGDOM_INNOCENT_REGULAR_ROULETTE = 53
    MAKAI_KINGDOM_INNOCENT_SPECIAL_ROULETTE = 54
    SEVEN_DEADLY_SINS_EVENT_POINT = 55
    SEVEN_DEADLY_SINS_INNOCENT_REGULAR_ROULETTE = 56
    SEVEN_DEADLY_SINS_INNOCENT_SPECIAL_ROULETTE = 57
    KAGEMARU_EVENT_POINT = 58
    KAGEMARU_KINNOCENT_REGULAR_ROULETTE = 59
    KAGEMARU_INNOCENT_SPECIAL_ROULETTE = 60
    MADOKA_EVENT_POINT = 61
    MADOKA_INNOCENT_REGULAR_ROULETTE = 62
    MADOKA_INNOCENT_SPECIAL_ROULETTE = 63
    PLEINAIR_EVENT_POINT = 64
    PLEINAIR_INNOCENT_REGULAR_ROULETTE = 65
    PLEINAIR_INNOCENT_SPECIAL_ROULETTE = 66
    SANTA_TORACHIYO_EVENT_POINT = 67
    SANTA_TORACHIYO_INNOCENT_REGULAR_ROULETTE = 68
    SANTA_TORACHIYO_INNOCENT_SPECIAL_ROULETTE = 69


class Raid_ID(IntEnum):
    SUMMER_PRINNY_RAID_ID = 135
    MAKAI_KINGDOM_RAID_ID = 143
    SEVEN_DEADLY_SINS_RAID_ID = 151
    KAGEMARU_RAID_ID = 156
    MADOKA_RAID_ID = 165
    FW_PLEINAIR_RAID_ID = 182
    SANTA_TORACHIYO_RAID_ID = 195
    SAKUYA_RAID_ID = 209
    OVERLORD_PRIERE_RAID_ID = 220
    METALLIA_RAID_ID = 233


class Raid_Boss_Level_Step(IntEnum):
    NOT_SET = 0
    LEVEL_50 = 1
    LEVEL_9999 = 51
    LEVEL_2000 = 100


class Raid_Badass_Boss_Level_Step(IntEnum):
    NOT_SET = 0
    LEVEL_100 = 1


class Fish_Fleet_Index(IntEnum):
    CHARACTER_EXP_FLEET = 1
    SKILL_EXP_FLEET = 2
    WM_EXP_FLEET = 3


class Fish_Fleet_Result_type(IntEnum):
    HARVEST_1 = 1
    NORMAL_HARVEST = 2
    SUPER_HARVEST = 3


class Fish_Fleet_Survey_Duration(IntEnum):
    HOURS_6 = 6
    HOURS_12 = 12
    HOURS_18 = 18
    HOURS_24 = 24


class Fish_Fleet_Area_Bribe_Status(IntEnum):
    VERY_FEW = 1
    FEW = 2
    COMMON = 3
    MANY = 4
    VERY_MANY = 5


class Innocent_Status(IntEnum):
    NOT_SUBDUED = 0
    SUBDUED = 1
    ESCAPED = 2


class Innocent_Training_Result(IntEnum):
    NORMAL = 1
    NOT_BAD = 2
    DREAMLIKE = 3


# There's innocent type and innocent id. The Glasses INT inno has the same type as the regular INT inno, but different ID
class Innocent_ID(IntEnum):
    HP = 1
    ATK = 2
    DEF = 3
    INT = 4
    RES = 5
    SPD = 6
    EXP = 7
    HL = 8


class EquipmentType(IntEnum):
    WEAPON = 1
    ARMOR = 2


class Battle_Finish_Type(IntEnum):
    Normal_Attack = 1
    Special_Move = 2
    Team_Attack = 3
    Tower_Attack = 5
    Prinny_Explosion = 6


class Items(IntEnum):
    HL = 101
    Prinny_Steel = 3201
    PriPrism = 4101
    Prilixir = 4201


class Item_World_Mode(IntEnum):
    Run_Weapons_Only = 1
    Run_Equipment_Only = 2
    Run_All_Items = 3


class Item_World_Drop_Mode(IntEnum):
    Drop_Weapons_Only = 1
    Drop_All_Items = 2


class Alchemy_Effect_Type(IntEnum):
    Innocent_Effect = 10001
    CritRate = 20001
    CritDmg = 20002
    HP = 20003
    DEF = 20004
    RES = 20005
    Water_Damage = 30001
    Fire_Damage = 30002
    Wind_Damage = 30003
    Star_Damage = 30004
    Non_Elemental_Damage = 30005
    Normal_Attack_Damage = 30006
    Skill_Damage = 30007
    DmgDealtMon = 30019
    DmgDealtHuman = 30020
    SP_Per_Turn = 30022
    Action_Gauge = 30023
    Skill_Damage_Taken = 30035
    DmgTakenMon = 30047
    DmgTakenHuman = 30048
    Restore_HP = 30049
    PoisonRes = 30050
    ParalysisRes = 30051
    SleepRes = 30052
    ForgetRes = 30053
    AGRR = 30054

class Mission_Status (IntEnum):
    Not_Completed = 0
    Cleared = 1
    Claimed = 2
    
class Character_Type (IntEnum):
    Human = 1
    Monster = 2

class Character_Gender (IntEnum):
    Male = 1
    Female = 2

class Weapon_Type (IntEnum):
    Sword = 1
    Fist = 2
    Spear = 3
    Bow = 4
    Gun = 5
    Axe = 6
    Wand = 7
    Monster_Physical = 8
    Monster_Magical = 9

class Battle_Finish_Mode(IntEnum):
    Random_Finish = 1 # killing blows will be randomly split
    Tower_Finish = 2 # Use tower finishes to share exp
    Single_Character = 3 # Character on leader slot will kill all enemies to get all bonus exp