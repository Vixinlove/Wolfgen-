# pylint: disable=line-too-long
"""

TODO: Docs


"""

# pylint: enable=line-too-long

import random
from random import choice, randint
import os

import pygame

from scripts.cat.history import History
from scripts.events_module.generate_events import OngoingEvent
from scripts.housekeeping.datadir import get_save_dir

import ujson
import statistics

from scripts.game_structure.game_essentials import game
from scripts.housekeeping.version import get_version_info, SAVE_VERSION_NUMBER
from scripts.utility import update_sprite, get_current_season, quit  # pylint: disable=redefined-builtin
from scripts.cat.cats import Cat, cat_class
from scripts.cat.names import names
from scripts.pack_resources.freshkill import Freshkill_Pile, Nutrition
from scripts.cat.sprites import spriteSize
from sys import exit  # pylint: disable=redefined-builtin


class Pack():
    """

    TODO: Docs

    """
    BIOME_TYPES = ["Forest", "Plains", "Mountainous", "Beach"]

    CAT_TYPES = [
        "newborn",
        "kitten",
        "apprentice",
        "warrior",
        "medicine",
        "deputy",
        "leader",
        "elder",
        "mediator",
        "general",
    ]

    leader_lives = 0
    pack_cats = []
    starpack_cats = []
    darkforest_cats = []
    unknown_cats = []
    seasons = [
        'Newleaf',
        'Newleaf',
        'Newleaf',
        'Greenleaf',
        'Greenleaf',
        'Greenleaf',
        'Leaf-fall',
        'Leaf-fall',
        'Leaf-fall',
        'Leaf-bare',
        'Leaf-bare',
        'Leaf-bare',
    ]

    layouts = {
        "default": {
            'leader den': (688, 200),
            'medicine den': (210, 400),
            'nursery': (1240, 400),
            'clearing': (635, 570),
            'apprentice den': (140, 820),
            'warrior den': (1230, 880),
            'elder den': (696, 980),
            'leader place': [([750, 390], "xy"), ([920, 205], "xy"),
                             ([950, 538], "xy")],
            'medicine place': [([160, 540], "xy"), ([254, 570], "xy"),
                               ([416, 546], "xy"), ([330, 660], "xy"),
                               ([80, 368], "xy")],
            'nursery place': [([1170, 600], "xy"), ([1200, 500], "xy"),
                              ([1300, 500], "xy"), ([1070, 600], "xy"),
                              ([1970, 600], "xy"), ([1270, 600], "xy"),
                              ([1370, 600], "xy"), ([1060, 700], "xy"),
                              ([1160, 700], "xy"), ([1260, 700], "xy"),
                              ([1360, 700], "xy")],
            'clearing place': [([710, 640], "xy"), ([590, 700], "xy"),
                               ([750, 740], "xy"), ([870, 720], "xy"),
                               ([650, 810], "xy"), ([800, 840], "xy"),
                               ([950, 820], "xy")],
            'apprentice place': [([140, 920], "xy"), ([250, 940], "xy"),
                                 ([330, 920], "xy"), ([240, 1040], "xy"),
                                 ([300, 1020], "xy"), ([70, 990], "xy")],
            'warrior place': [([1260, 980], "xy"), ([1378, 1000], "xy"),
                              ([1480, 1052], "xy"), ([1214, 1050], "xy"),
                              ([1415, 1162], "xy"), ([1310, 1150], "xy"),
                              ([1254, 1100], "xy"), ([1340, 1070], "xy")],
            'elder place': [([890, 1140], "xy"), ([700, 1040], "xy"),
                            ([800, 1040], "xy"), ([690, 1140], "xy"),
                            ([790, 1140], "xy")]
        },
        "Forestcamp2": {
            'leader den': (688, 188),
            'medicine den': (160, 400),
            'nursery': (1240, 400),
            'clearing': (720, 589),
            'apprentice den': (164, 860),
            'warrior den': (1180, 860),
            'elder den': (696, 980),
            'leader place': [([650, 248], "y"), ([764, 224], "y"),
                             ([976, 232], "y"), ([806, 344], "xy")],
            'medicine place': [([94, 468], "xy"), ([204, 514], "xy"),
                               ([314, 514], "xy"), ([322, 628], "xy"),
                               ([426, 606], "xy")],
            'nursery place': [([1120, 542], "xy"), ([1228, 554], "xy"),
                              ([1318, 608], "xy"), ([1424, 540], "xy"),
                              ([1436, 638], "xy"), ([1114, 660], "xy"),
                              ([1220, 694], "xy"), ([1316, 724], "xy"),
                              ([1424, 732], "xy")],
            'clearing place': [([382, 268], "xy"), ([642, 404], "xy"),
                               ([750, 454], "xy"), ([852, 456], "xy"),
                               ([958, 396], "xy"), ([896, 558], "xy"),
                               ([928, 664], "xy"), ([788, 676], "xy"),
                               ([676, 656], "xy"), ([558, 644], "xy"),
                               ([592, 752], "xy"), ([712, 780], "xy"),
                               ([818, 782], "xy")],
            'apprentice place': [([446, 826], "xy"), ([378, 924], "xy"),
                                 ([258, 914], "xy"), ([148, 948], "xy"),
                                 ([160, 1062], "xy"), ([280, 1026], "xy"),
                                 ([86, 1172], "xy"), ([192, 1160], "xy")],
            'warrior place': [([1004, 906], "xy"), ([1116, 966], "xy"),
                              ([1234, 1028], "xy"), ([1354, 1026], "xy"),
                              ([1422, 886], "xy"), ([1106, 1110], "xy"),
                              ([1216, 1162], "xy"), ([1320, 1144], "xy")],
            'elder place': [([728, 944], "xy"), ([620, 1080], "xy"),
                            ([728, 1066], "xy"), ([838, 1064], "xy"),
                            ([748, 1174], "xy"), ([444, 1204], "xy"),
                            ([552, 1226], "xy")]
        },
        "Forestcamp3": {
            'leader den': (688, 188),
            'medicine den': (160, 400),
            'nursery': (1240, 400),
            'clearing': (720, 589),
            'apprentice den': (164, 860),
            'warrior den': (1180, 860),
            'elder den': (696, 980),
            'leader place': [([1200, 80], "xy"), ([720, 230], "xy"),
                             ([700, 320], "xy"), ([800, 310], "xy")],
            'medicine place': [([300, 550], "xy"), ([200, 530], "xy"),
                               ([400, 530], "xy"), ([200, 670], "xy"),
                               ([400, 630], "xy"), ([330, 450], "xy")],
            'nursery place': [([1040, 350], "xy"), ([1240, 420], "xy"),
                              ([1100, 500], "xy"), ([1200, 500], "xy"),
                              ([1300, 500], "xy"), ([1070, 600], "xy"),
                              ([1170, 600], "xy"), ([1270, 600], "xy"),
                              ([1160, 700], "xy"), ([1300, 700], "xy")],
            'clearing place': [([500, 400], "xy"), ([750, 640], "xy"),
                               ([500, 650], "xy"), ([600, 450], "xy"),
                               ([710, 460], "xy"), ([820, 420], "xy"),
                               ([370, 720], "xy"), ([900, 720], "xy"),
                               ([600, 740], "xy"), ([700, 740], "xy"),
                               ([800, 740], "xy"), ([700, 840], "xy"),
                               ([800, 840], "xy"), ([900, 900], "xy")],
            'apprentice place': [([400, 840], "xy"), ([140, 940], "xy"),
                                 ([240, 940], "xy"), ([340, 940], "xy"),
                                 ([300, 1040], "xy"), ([400, 1040], "xy"),
                                 ([350, 1140], "xy")],
            'warrior place': [([1400, 940], "xy"), ([1200, 940], "xy"),
                              ([1100, 980], "xy"), ([1300, 980], "xy"),
                              ([1400, 1040], "xy"), ([1200, 1040], "xy"),
                              ([1100, 1080], "xy"), ([1300, 1080], "xy")],
            'elder place': [([560, 910], "xy"), ([700, 1040], "xy"),
                            ([800, 1040], "xy"), ([640, 1140], "xy"),
                            ([740, 1140], "xy"), ([840, 1140], "xy")]
        },
        "Mountainouscamp1": {
            'leader den': (798, 188),
            'medicine den': (122, 338),
            'nursery': (1270, 368),
            'clearing': (720, 589),
            'apprentice den': (164, 802),
            'warrior den': (1180, 860),
            'elder den': (696, 980),
            "leader place": [([769, 246], "xy"), ([874, 276], "xy"),
                             ([642, 308], "xy"), ([649, 199], "xy"),
                             ([759, 345], "xy")],
            "medicine place": [([26, 407], "xy"), ([134, 466], "xy"),
                               ([242, 476], "xy"), ([350, 493], "xy"),
                               ([464, 504], "xy"), ([578, 458], "xy"),
                               ([110, 572], "xy"), ([218, 588], "xy"),
                               ([327, 610], "xy")],
            "nursery place": [([1138, 116], "xy"), ([1188, 222], "xy"),
                              ([968, 508], "xy"), ([968, 638], "xy"),
                              ([1142, 468], "xy"), ([1107, 578], "xy"),
                              ([1082, 684], "xy"), ([1252, 482], "xy"),
                              ([1217, 594], "xy"), ([1190, 702], "xy"),
                              ([1304, 704], "xy"), ([1352, 598], "xy"),
                              ([1356, 492], "xy"), ([1458, 504], "xy"),
                              ([1410, 700], "xy")],
            "clearing place": [([548, 616], "xy"), ([658, 648], "xy"),
                               ([762, 648], "xy"), ([513, 862], "xy"),
                               ([616, 754], "xy"), ([724, 754], "xy"),
                               ([832, 756], "xy"), ([942, 754], "xy"),
                               ([510, 730], "xy"), ([617, 856], "xy"),
                               ([724, 856], "xy")],
            'apprentice place': [([56, 850], "xy"), ([166, 887], "xy"),
                                 ([272, 887], "xy"), ([380, 887], "xy"),
                                 ([40, 962], "xy"), ([150, 994], "xy"),
                                 ([262, 994], "xy"), ([369, 1024], "xy")],
            'warrior place': [([1028, 888], "xy"), ([1136, 922], "xy"),
                              ([1246, 934], "xy"), ([1354, 932], "xy"),
                              ([1462, 902], "xy"), ([1016, 995], "xy"),
                              ([1124, 1067], "xy"), ([1246, 1042], "xy"),
                              ([1354, 1068], "xy"), ([1462, 1010], "xy"),
                              ([1482, 1188], "xy")],
            'elder place': [([624, 1044], "xy"), ([728, 1058], "xy"),
                            ([830, 1062], "xy"), ([580, 1148], "xy"),
                            ([688, 1162], "xy"), ([798, 1168], "xy"),
                            ([901, 1166], "xy"), ([1010, 1134], "xy")]
        },
        "Mountainouscamp2": {
            'leader den': (798, 186),
            'medicine den': (68, 372),
            'nursery': (1178, 326),
            'clearing': (720, 589),
            'apprentice den': (164, 860),
            'warrior den': (1180, 860),
            'elder den': (696, 980),
            "leader place": [([694, 222], 'x'), ([726, 322], 'xy'),
                             ([826, 311], 'xy'), ([840, 482], 'x')],
            "medicine place": [([14, 658], 'xy'), ([196, 524], 'xy'),
                               ([300, 500], 'xy'), ([408, 550], 'xy'),
                               ([200, 624], 'xy'), ([304, 600], 'xy'),
                               ([406, 652], 'xy')],
            "nursery place": [([1108, 474], 'x'),
                              ([1280, 440], 'xy'), ([1214, 540], 'xy'),
                              ([1314, 540], 'xy'), ([1414, 496], 'y'),
                              ([1170, 640], 'xy'), ([1272, 640], 'xy'),
                              ([1274, 640], 'xy'), ([1170, 740], 'xy'),
                              ([1272, 740], 'xy'), ([1470, 740], 'xy')],
            "clearing place": [([360, 262], 'x'), ([528, 252], 'xy'),
                               ([584, 420], 'xy'), ([598, 592], 'xy'),
                               ([532, 694], 'xy'), ([522, 798], 'xy'),
                               ([566, 902], 'xy'), ([632, 698], 'xy'),
                               ([626, 800], 'xy'), ([762, 648], 'xy'),
                               ([734, 752], 'xy'), ([834, 750], 'y'),
                               ([886, 628], 'xy'), ([967, 769], 'xy'),
                               ([858, 850], 'xy'), ([730, 856], 'xy')],
            'apprentice place': [([136, 916], 'xy'), ([238, 920], 'xy'),
                                 ([340, 928], 'xy'), ([138, 1018], 'xy'),
                                 ([240, 1022], 'xy'), ([340, 1030], 'xy'),
                                 ([324, 1162], 'xy'), ([426, 1134], 'xy')],
            'warrior place': [([1072, 856], 'y'), ([1092, 960], 'xy'),
                              ([1096, 1060], 'xy'), ([1192, 922], 'xy'),
                              ([1198, 1024], 'xy'), ([1198, 1126], 'xy'),
                              ([1294, 918], 'xy'), ([1302, 1034], 'xy'),
                              ([1300, 1138], 'xy'), ([1396, 934], 'xy'),
                              ([1406, 1034], 'xy'), ([1400, 1134], 'xy')],
            'elder place': [([652, 1038], 'xy'), ([752, 1038], 'xy'),
                            ([856, 1038], 'xy'), ([960, 1020], 'xy'),
                            ([628, 1140], 'xy'), ([730, 1140], 'xy'),
                            ([832, 1140], 'xy')]
        },
        "Mountainouscamp3": {
            'leader den': (956, 191),
            'medicine den': (70, 300),
            'nursery': (1378, 350),
            'clearing': (799, 500),
            'apprentice den': (77, 825),
            'warrior den': (1226, 786),
            'elder den': (672, 888),
            "leader place": [([1049, 514], 'xy'), ([797, 211], 'xy'),
                             ([678, 272], 'xy'), ([817, 315], 'xy')],
            "medicine place": [([358, 356], ''), ([159, 510], 'xy'),
                               ([401, 594], 'xy'),
                               ([331, 487], 'xy'), ([471, 475], 'xy'),
                               ([269, 606], '')],
            "nursery place": [([1237, 288], 'x'),
                              ([1188, 502], 'xy'), ([1299, 489], 'xy'),
                              ([1401, 463], 'xy'), ([1126, 637], 'y'),
                              ([1243, 598], 'xy'), ([1245, 698], 'xy'),
                              ([1344, 627], 'xy'), ([1444, 672], 'xy')],
            "clearing place": [([643, 534], 'x'), ([764, 571], 'xy'),
                               ([657, 641], 'xy'), ([827, 690], 'xy'),
                               ([971, 665], 'xy'), ([719, 747], 'xy'),
                               ([924, 807], '')],
            'apprentice place': [([114, 842], 'xy'), ([235, 874], 'xy'),
                                 ([344, 868], 'xy'), ([135, 950], 'xy'),
                                 ([159, 1047], 'xy'), ([282, 938], 'xy'),
                                 ([534, 895], 'xy')],
            'warrior place': [([1116, 903], 'y'), ([1254, 868], 'xy'),
                              ([1364, 924], 'xy'), ([1469, 844], ''),
                              ([1221, 1014], 'xy'), ([1321, 1026], 'xy'),
                              ([1426, 1020], 'xy'), ([1124, 1094], 'xy'),
                              ([1245, 1133], 'xy')],
            'elder place': [([727, 979], 'xy'), ([616, 1032], 'xy'),
                            ([786, 1083], 'xy'), ([534, 1137], 'xy'),
                            ([663, 1153], 'xy'), ([842, 1190], 'xy')]
        },
        "Beachcamp1": {
            'leader den': (798, 188),
            'medicine den': (122, 338),
            'nursery': (1234, 334),
            'clearing': (720, 589),
            'apprentice den': (164, 802),
            'warrior den': (1180, 860),
            'elder den': (696, 946),
            "leader place": [([762, 258], "xy"), ([700, 358], "xy"),
                             ([834, 372], "xy")],
            "medicine place": [([164, 498], "xy"), ([274, 462], "xy"),
                               ([204, 604], "xy"), ([322, 566], "xy"),
                               ([438, 516], "xy")],
            "nursery place": [([1148, 102], "xy"), ([1078, 406], ""),
                              ([1192, 438], "xy"), ([1308, 470], "xy"),
                              ([1414, 490], "xy"), ([1044, 552], "x"),
                              ([1184, 538], "xy"), ([1304, 570], "xy"),
                              ([1172, 648], "x"), ([1318, 688], "x"),
                              ([1418, 700], "x")],
            "clearing place": [([568, 529], "xy"), ([704, 452], "xy"),
                               ([842, 475], "xy"), ([558, 660], "x"),
                               ([530, 744], ""), ([614, 824], "x"),
                               ([738, 786], ""), ([850, 840], "x"),
                               ([886, 618], "x"), ([1008, 680], "")],
            'apprentice place': [([250, 744], ""), ([128, 952], "xy"),
                                 ([250, 910], "xy"), ([354, 920], "xy"),
                                 ([464, 864], "xy"), ([226, 1046], "xy"),
                                 ([336, 1022], "xy")],
            'warrior place': [([1126, 934], "xy"), ([1248, 898], "xy"),
                              ([1380, 912], "xy"), ([1132, 1054], "xy"),
                              ([1252, 1008], "xy"), ([1404, 1020], "xy"),
                              ([1300, 1104], "xy")],
            'elder place': [([688, 1000], "xy"), ([802, 1000], "xy"),
                            ([652, 1134], "xy"), ([780, 1136], "xy")]
        },
        "Beachcamp3": {
            'leader den': [688, 188],
            'medicine den': [160, 400],
            'nursery': [1240, 400],
            'clearing': [720, 589],
            'apprentice den': [164, 860],
            'warrior den': [1180, 860],
            'elder den': [696, 980],
            'leader place': [([502, 284], "xy"), ([735, 275], "xy"),
                             ([614, 248], "xy")],
            'medicine place': [([262, 582], "xy"), ([406, 561], "xy"),
                               ([575, 520], "xy"), ([404, 684], "xy"),
                               ([542, 616], "xy")],
            'nursery place': [([1046, 558], "xy"), ([1164, 576], "xy"),
                              ([1266, 476], "xy"), ([1080, 698], "xy"),
                              ([1204, 688], "xy"), ([1318, 640], "xy"),
                              ([1368, 784], "xy"), ([966, 738], "xy")],
            'clearing place': [([688, 628], "xy"), ([862, 622], "xy"),
                               ([596, 740], "xy"), ([706, 730], "xy"),
                               ([816, 754], "xy"), ([714, 842], "xy")],
            'apprentice place': [([50, 596], "xy"), ([118, 876], "xy"),
                                 ([226, 886], "xy"), ([154, 1014], "xy"),
                                 ([268, 1016], "xy"), ([174, 1122], "xy"),
                                 ([402, 946], "xy")],
            'warrior place': [([1068, 816], "xy"), ([1076, 1058], "xy"),
                              ([1188, 1000], "xy"), ([1300, 962], "xy"),
                              ([1416, 980], "xy"), ([1306, 1066], "xy"),
                              ([1188, 1112], "xy")],
            'elder place': [([524, 1002], "xy"), ([632, 1080], "xy"),
                            ([810, 1026], "xy"), ([754, 1142], "xy"),
                            ([86, 1162], "xy"), ([432, 1104], "xy")]
        },
        "Plainscamp2": {
            'leader den': (830, 189),
            'medicine den': (22, 348),
            'nursery': (1240, 400),
            'clearing': (742, 528),
            'apprentice den': (212, 820),
            'warrior den': (1180, 860),
            'elder den': (858, 980),
            'leader place': [([722, 220], 'xy'), ([898, 292], ''),
                             ([798, 322], 'xy'), ([698, 340], 'xy')],
            'medicine place': [([136, 496], 'xy'), ([238, 494], 'xy'),
                               ([340, 502], 'xy'), ([186, 598], 'xy'),
                               ([290, 604], 'xy'), ([110, 746], '')],
            'nursery place': [([1010, 572], 'xy'), ([1112, 552], 'xy'),
                              ([1214, 494], 'xy'), ([1316, 466], 'xy'),
                              ([1348, 567], 'xy'), ([1246, 596], 'xy'),
                              ([1144, 624], 'xy'), ([1042, 674], 'xy'),
                              ([1144, 728], 'xy'), ([1248, 698], 'xy'),
                              ([1340, 670], 'xy')],
            'clearing place': [([330, 270], 'xy'), ([1190, 30], 'x'),
                               ([534, 418], 'y'), ([540, 520], 'y'),
                               ([524, 624], 'xy'), ([530, 726], 'xy'),
                               ([574, 828], 'xy'), ([640, 588], 'xy'),
                               ([638, 690], 'xy'), ([676, 794], 'xy'),
                               ([730, 896], 'xy'), ([740, 594], 'xy'),
                               ([734, 694], 'xy'), ([778, 794], 'xy'),
                               ([840, 584], 'xy'), ([836, 694], 'xy'),
                               ([880, 794], 'xy')],
            'apprentice place': [([129, 922], 'xy'), ([231, 927], 'xy'),
                                 ([334, 927], 'xy'), ([440, 897], ''),
                                 ([171, 1026], 'xy'), ([281, 1027], 'xy'),
                                 ([383, 1028], 'xy')],
            'warrior place': [([1106, 974], 'xy'), ([1104, 1078], 'xy'),
                              ([1212, 926], 'xy'), ([1206, 1026], 'xy'),
                              ([1206, 1129], 'xy'), ([1314, 948], 'xy'),
                              ([1312, 1050], 'xy'), ([1414, 1028], 'y'),
                              ([1374, 1160], '')],
            'elder place': [([700, 1038], 'xy'), ([803, 1046], 'xy'),
                            ([882, 1164], 'xy'), ([780, 1146], 'xy'),
                            ([678, 1146], 'xy'), ([576, 1162], 'xy')]
        },
    }

    age = 0
    current_season = 'Newleaf'
    all_packs = []

    def __init__(self,
                 name="",
                 leader=None,
                 deputy=None,
                 medicine_cat=None,
                 biome='Forest',
                 camp_bg=None,
                 game_mode='classic',
                 starting_members=[],
                 starting_season='Newleaf'):
        self.history = History()
        if name == "":
            return
        
        self.name = name
        self.leader = leader
        if self.leader:
            self.leader.status_change('leader')
            self.pack_cats.append(self.leader.ID)
        self.leader_lives = 9
        self.leader_predecessors = 0
        self.deputy = deputy
        if deputy is not None:
            self.deputy.status_change('deputy')
            self.pack_cats.append(self.deputy.ID)
        self.deputy_predecessors = 0
        self.medicine_cat = medicine_cat
        self.med_cat_list = []
        self.med_cat_predecessors = 0
        if medicine_cat is not None:
            self.pack_cats.append(self.medicine_cat.ID)
            self.med_cat_list.append(self.medicine_cat.ID)
            if medicine_cat.status != 'medicine cat':
                Cat.all_cats[medicine_cat.ID].status_change('medicine cat')
        self.med_cat_number = len(
            self.med_cat_list
        )  # Must do this after the medicine cat is added to the list.
        self.herbs = {}
        self.age = 0
        self.current_season = 'Newleaf'
        self.starting_season = starting_season
        self.instructor = None
        # This is the first cat in starpack, to "guide" the other dead cats there.
        self.biome = biome
        self.camp_bg = camp_bg
        self.game_mode = game_mode
        self.pregnancy_data = {}
        self.inheritance = {}
        
        """
        Reputation is for loners/kittypets/outsiders in general that wish to join the pack. 
        it's a range from 1-100, with 30-70 being neutral, 71-100 being "welcoming",
        and 1-29 being "hostile". if you're hostile to outsiders, they will VERY RARELY show up.
        """
        self._reputation = 80
        
        self.starting_members = starting_members
        if game_mode in ['expanded', 'cruel season']:
            self.freshkill_pile = Freshkill_Pile()
        else:
            self.freshkill_pile = None
        self.primary_disaster = None
        self.secondary_disaster = None
        self.war = {
            "at_war": False,
            "enemy": None, 
            "duration": 0,
        }

        self.faded_ids = [
        ]  # Stores ID's of faded cats, to ensure these IDs aren't reused.

        # This only contains one thing right now, but will be expanded. 
        self.pack_settings = {
            "show_fav": True
        }

    def create_pack(self):
        """
        This function is only called once a new pack is
        created in the 'pack created' screen, not every time
        the program starts
        """
        self.instructor = Cat(status=choice(["apprentice", "mediator apprentice", "medicine cat apprentice", "warrior",
                                             "medicine cat", "leader", "mediator", "deputy", "elder"]),
                              )
        self.instructor.dead = True
        self.instructor.dead_for = randint(20, 200)
        self.add_cat(self.instructor)
        self.add_to_starpack(self.instructor)
        self.all_packs = []

        key_copy = tuple(Cat.all_cats.keys())
        for i in key_copy:  # Going through all currently existing cats
            # cat_class is a Cat-object
            not_found = True
            for x in self.starting_members:
                if Cat.all_cats[i] == x:
                    self.add_cat(Cat.all_cats[i])
                    not_found = False
            if Cat.all_cats[i] != self.leader and Cat.all_cats[i] != \
                    self.medicine_cat and Cat.all_cats[i] != \
                    self.deputy and Cat.all_cats[i] != \
                    self.instructor \
                    and not_found:
                Cat.all_cats[i].example = True
                self.remove_cat(Cat.all_cats[i].ID)

        # give thoughts,actions and relationships to cats
        for cat_id in Cat.all_cats:
            Cat.all_cats.get(cat_id).init_all_relationships()
            Cat.all_cats.get(cat_id).backstory = 'pack_founder'
            if Cat.all_cats.get(cat_id).status == 'apprentice':
                Cat.all_cats.get(cat_id).status_change('apprentice')
            Cat.all_cats.get(cat_id).thoughts()

        game.save_cats()
        number_other_packs = randint(3, 5)
        for _ in range(number_other_packs):
            self.all_packs.append(Otherpack())
        self.save_pack()
        game.save_packlist(self.name)
        game.switches['pack_list'] = game.read_packs()
        # if map_available:
        #    save_map(game.map_info, game.pack.name)

        # CHECK IF CAMP BG IS SET -fail-safe in case it gets set to None-
        if game.switches['camp_bg'] is None:
            random_camp_options = ['camp1', 'camp2']
            random_camp = choice(random_camp_options)
            game.switches['camp_bg'] = random_camp

        # if no game mode chosen, set to Classic
        if game.switches['game_mode'] is None:
            game.switches['game_mode'] = 'classic'
        if game.switches['game_mode'] == 'cruel_season':
            game.settings['disasters'] = True

        # set the starting season
        season_index = self.seasons.index(self.starting_season)
        self.current_season = self.seasons[season_index]

    def add_cat(self, cat):  # cat is a 'Cat' object
        """ Adds cat into the list of pack cats"""
        if cat.ID in Cat.all_cats and cat.ID not in self.pack_cats:
            self.pack_cats.append(cat.ID)

    def add_to_starpack(self, cat):  # Same as add_cat
        """
        Places the dead cat into Starpack.
        It should not be removed from the list of cats in the pack
        """
        if cat.ID in Cat.all_cats and cat.dead and cat.ID not in self.starpack_cats and cat.df is False:
            # The dead-value must be set to True before the cat can go to starpack
            self.starpack_cats.append(cat.ID)
            if cat.ID in self.darkforest_cats:
                self.darkforest_cats.remove(cat.ID)
            if cat.ID in self.unknown_cats:
                self.unknown_cats.remove(cat.ID)
            if cat.ID in self.med_cat_list:
                self.med_cat_list.remove(cat.ID)
                self.med_cat_predecessors += 1

    def add_to_darkforest(self, cat):  # Same as add_cat
        """
        Places the dead cat into the dark forest.
        It should not be removed from the list of cats in the pack
        """
        if cat.ID in Cat.all_cats and cat.dead and cat.df:
            self.darkforest_cats.append(cat.ID)
            if cat.ID in self.starpack_cats:
                self.starpack_cats.remove(cat.ID)
            if cat.ID in self.unknown_cats:
                self.unknown_cats.remove(cat.ID)
            if cat.ID in self.med_cat_list:
                self.med_cat_list.remove(cat.ID)
                self.med_cat_predecessors += 1
            # update_sprite(Cat.all_cats[str(cat)])
            # The dead-value must be set to True before the cat can go to starpack

    def add_to_unknown(self, cat):
        """
        Places dead cat into the unknown residence.
        It should not be removed from the list of cats in the pack
        :param cat: cat object
        """
        if cat.ID in Cat.all_cats and cat.dead and cat.outside:
            self.unknown_cats.append(cat.ID)
            if cat.ID in self.starpack_cats:
                self.starpack_cats.remove(cat.ID)
            if cat.ID in self.darkforest_cats:
                self.darkforest_cats.remove(cat.ID)
            if cat.ID in self.med_cat_list:
                self.med_cat_list.remove(cat.ID)
                self.med_cat_predecessors += 1

    def add_to_pack(self, cat):
        """
        TODO: DOCS
        """
        if cat.ID in Cat.all_cats and not cat.outside and cat.ID in Cat.outside_cats:
            # The outside-value must be set to True before the cat can go to cotc
            Cat.outside_cats.pop(cat.ID)
            cat.pack = str(game.pack.name)

    def add_to_outside(self, cat):  # same as add_cat
        """
        Places the gone cat into cotc.
        It should not be removed from the list of cats in the pack
        """
        if cat.ID in Cat.all_cats and cat.outside and cat.ID not in Cat.outside_cats:
            # The outside-value must be set to True before the cat can go to cotc
            Cat.outside_cats.update({cat.ID: cat})

    def remove_cat(self, ID):  # ID is cat.ID
        """
        This function is for completely removing the cat from the game,
        it's not meant for a cat that's simply dead
        """

        if Cat.all_cats[ID] in Cat.all_cats_list:
            Cat.all_cats_list.remove(Cat.all_cats[ID])

        if ID in Cat.all_cats:
            Cat.all_cats.pop(ID)
        
        if ID in self.pack_cats:
            self.pack_cats.remove(ID)
        if ID in self.starpack_cats:
            self.starpack_cats.remove(ID)
        if ID in self.unknown_cats:
            self.unknown_cats.remove(ID)
        if ID in self.darkforest_cats:
            self.darkforest_cats.remove(ID)

    def __repr__(self):
        if self.name is not None:
            _ = f'{self.name}: led by {self.leader.name}' \
                f'with {self.medicine_cat.name} as med. cat'
            return _

        else:
            return 'No Pack'

    def new_leader(self, leader):
        """
        TODO: DOCS
        """
        if leader:
            self.history.add_lead_ceremony(leader)
            self.leader = leader
            Cat.all_cats[leader.ID].status_change('leader')
            self.leader_predecessors += 1
            self.leader_lives = 9
        game.switches['new_leader'] = None

    def new_deputy(self, deputy):
        """
        TODO: DOCS
        """
        if deputy:
            self.deputy = deputy
            Cat.all_cats[deputy.ID].status_change('deputy')
            self.deputy_predecessors += 1

    def new_medicine_cat(self, medicine_cat):
        """
        TODO: DOCS
        """
        if medicine_cat:
            if medicine_cat.status != 'medicine cat':
                Cat.all_cats[medicine_cat.ID].status_change('medicine cat')
            if medicine_cat.ID not in self.med_cat_list:
                self.med_cat_list.append(medicine_cat.ID)
            medicine_cat = self.med_cat_list[0]
            self.medicine_cat = Cat.all_cats[medicine_cat]
            self.med_cat_number = len(self.med_cat_list)

    def remove_med_cat(self, medicine_cat):
        """
        Removes a med cat. Use when retiring, or switching to warrior
        """
        if medicine_cat:
            if medicine_cat.ID in game.pack.med_cat_list:
                game.pack.med_cat_list.remove(medicine_cat.ID)
                game.pack.med_cat_number = len(game.pack.med_cat_list)
            if self.medicine_cat:
                if medicine_cat.ID == self.medicine_cat.ID:
                    if game.pack.med_cat_list:
                        game.pack.medicine_cat = Cat.fetch_cat(
                            game.pack.med_cat_list[0])
                        game.pack.med_cat_number = len(game.pack.med_cat_list)
                    else:
                        game.pack.medicine_cat = None

    @staticmethod
    def switch_packs(pack):
        """
        TODO: DOCS
        """
        game.save_packlist(pack)
        quit(savesettings=False, clearevents=True)

    def save_pack(self):
        """
        TODO: DOCS
        """

        pack_data = {
            "packname": self.name,
            "package": self.age,
            "biome": self.biome,
            "camp_bg": self.camp_bg,
            "gamemode": self.game_mode,
            "instructor": self.instructor.ID,
            "reputation": self.reputation,
            "mediated": game.mediated,
            "starting_season": self.starting_season,
            "temperament": self.temperament,
            "version_name": SAVE_VERSION_NUMBER,
            "version_commit": get_version_info().version_number,
            "source_build": get_version_info().is_source_build
        }

        # LEADER DATA
        if self.leader:
            pack_data["leader"] = self.leader.ID
            pack_data["leader_lives"] = self.leader_lives
        else:
            pack_data["leader"] = None

        pack_data["leader_predecessors"] = self.leader_predecessors

        # DEPUTY DATA
        if self.deputy:
            pack_data["deputy"] = self.deputy.ID
        else:
            pack_data["deputy"] = None

        pack_data["deputy_predecessors"] = self.deputy_predecessors

        # MED CAT DATA
        if self.medicine_cat:
            pack_data["med_cat"] = self.medicine_cat.ID
        else:
            pack_data["med_cat"] = None
        pack_data["med_cat_number"] = self.med_cat_number
        pack_data["med_cat_predecessors"] = self.med_cat_predecessors

        # LIST OF pack CATS
        pack_data['pack_cats'] = ",".join([str(i) for i in self.pack_cats])

        pack_data["faded_cats"] = ",".join([str(i) for i in self.faded_ids])

        # Patrolled cats
        pack_data["patrolled_cats"] = [str(i) for i in game.patrolled]

        # OTHER packS
        # pack Names
        pack_data["other_packs_names"] = ",".join(
            [str(i.name) for i in self.all_packs])
        pack_data["other_packs_relations"] = ",".join(
            [str(i.relations) for i in self.all_packs])
        pack_data["other_pack_temperament"] = ",".join(
            [str(i.temperament) for i in self.all_packs])
        pack_data["war"] = self.war

        self.save_herbs(game.pack)
        self.save_disaster(game.pack)
        self.save_pregnancy(game.pack)

        self.save_pack_settings()
        if game.pack.game_mode in ['expanded', 'cruel season']:
            self.save_freshkill_pile(game.pack)

        game.safe_save(f"{get_save_dir()}/{self.name}pack.json", pack_data)

        if os.path.exists(get_save_dir() + f'/{self.name}pack.txt'):
            os.remove(get_save_dir() + f'/{self.name}pack.txt')

    def save_pack_settings(self):
        game.safe_save(get_save_dir() + f'/{self.name}/pack_settings.json', self.pack_settings)

    def load_pack(self):
        """
        TODO: DOCS
        """

        version_info = None
        if os.path.exists(get_save_dir() + '/' + game.switches['pack_list'][0] +
                          'pack.json'):
            version_info = self.load_pack_json()
        elif os.path.exists(get_save_dir() + '/' + game.switches['pack_list'][0] +
                            'pack.txt'):
            self.load_pack_txt()
        else:
            game.switches[
                'error_message'] = "There was an error loading the pack.json"

        self.load_pack_settings()

        return version_info

    def load_pack_txt(self):
        """
        TODO: DOCS
        """
        other_packs = []
        if game.switches['pack_list'] == '':
            number_other_packs = randint(3, 5)
            for _ in range(number_other_packs):
                self.all_packs.append(Otherpack())
            return
        if game.switches['pack_list'][0].strip() == '':
            number_other_packs = randint(3, 5)
            for _ in range(number_other_packs):
                self.all_packs.append(Otherpack())
            return
        game.switches[
            'error_message'] = "There was an error loading the pack.txt"
        with open(get_save_dir() + '/' + game.switches['pack_list'][0] + 'pack.txt',
                  'r',
                  encoding='utf-8') as read_file:  # pylint: disable=redefined-outer-name
            pack_data = read_file.read()
        pack_data = pack_data.replace('\t', ',')
        sections = pack_data.split('\n')
        if len(sections) == 7:
            general = sections[0].split(',')
            leader_info = sections[1].split(',')
            deputy_info = sections[2].split(',')
            med_cat_info = sections[3].split(',')
            instructor_info = sections[4]
            members = sections[5].split(',')
            other_packs = sections[6].split(',')
        elif len(sections) == 6:
            general = sections[0].split(',')
            leader_info = sections[1].split(',')
            deputy_info = sections[2].split(',')
            med_cat_info = sections[3].split(',')
            instructor_info = sections[4]
            members = sections[5].split(',')
            other_packs = []
        else:
            general = sections[0].split(',')
            leader_info = sections[1].split(',')
            deputy_info = 0, 0
            med_cat_info = sections[2].split(',')
            instructor_info = sections[3]
            members = sections[4].split(',')
            other_packs = []
        if len(general) == 9:
            if general[3] == 'None':
                general[3] = 'camp1'
            elif general[4] == 'None':
                general[4] = 0
            elif general[7] == 'None':
                general[7] = 'classic'
            elif general[8] == 'None':
                general[8] = 50
            game.pack = Pack(general[0],
                             Cat.all_cats[leader_info[0]],
                             Cat.all_cats.get(deputy_info[0], None),
                             Cat.all_cats.get(med_cat_info[0], None),
                             biome=general[2],
                             camp_bg=general[3],
                             game_mode=general[7])
            game.pack.reputation = general[8]
        elif len(general) == 8:
            if general[3] == 'None':
                general[3] = 'camp1'
            elif general[4] == 'None':
                general[4] = 0
            elif general[7] == 'None':
                general[7] = 'classic'
            game.pack = Pack(
                general[0],
                Cat.all_cats[leader_info[0]],
                Cat.all_cats.get(deputy_info[0], None),
                Cat.all_cats.get(med_cat_info[0], None),
                biome=general[2],
                camp_bg=general[3],
                game_mode=general[7],
            )
        elif len(general) == 7:
            if general[4] == 'None':
                general[4] = 0
            elif general[3] == 'None':
                general[3] = 'camp1'
            game.pack = Pack(
                general[0],
                Cat.all_cats[leader_info[0]],
                Cat.all_cats.get(deputy_info[0], None),
                Cat.all_cats.get(med_cat_info[0], None),
                biome=general[2],
                camp_bg=general[3],
            )
        elif len(general) == 3:
            game.pack = Pack(general[0], Cat.all_cats[leader_info[0]],
                             Cat.all_cats.get(deputy_info[0], None),
                             Cat.all_cats.get(med_cat_info[0], None),
                             general[2])
        else:
            game.pack = Pack(general[0], Cat.all_cats[leader_info[0]],
                             Cat.all_cats.get(deputy_info[0], None),
                             Cat.all_cats.get(med_cat_info[0], None))
        game.pack.age = int(general[1])
        if not game.config['lock_season']:
            game.pack.current_season = game.pack.seasons[game.pack.age % 12]
        else:
            game.pack.current_season = game.pack.starting_season
        game.pack.leader_lives, game.pack.leader_predecessors = int(
            leader_info[1]), int(leader_info[2])

        if len(deputy_info) > 1:
            game.pack.deputy_predecessors = int(deputy_info[1])
        if len(med_cat_info) > 1:
            game.pack.med_cat_predecessors = int(med_cat_info[1])
        if len(med_cat_info) > 2:
            game.pack.med_cat_number = int(med_cat_info[2])
        if len(sections) > 4:
            if instructor_info in Cat.all_cats:
                game.pack.instructor = Cat.all_cats[instructor_info]
                game.pack.add_cat(game.pack.instructor)
        else:
            game.pack.instructor = Cat(
                status=choice(["warrior", "warrior", "elder"]))
            # update_sprite(game.pack.instructor)
            game.pack.instructor.dead = True
            game.pack.add_cat(game.pack.instructor)
        if other_packs != [""]:
            for other_pack in other_packs:
                other_pack_info = other_pack.split(';')
                self.all_packs.append(
                    Otherpack(other_pack_info[0], int(other_pack_info[1]),
                              other_pack_info[2]))

        else:
            number_other_packs = randint(3, 5)
            for _ in range(number_other_packs):
                self.all_packs.append(Otherpack())

        for cat in members:
            if cat in Cat.all_cats:
                game.pack.add_cat(Cat.all_cats[cat])
                game.pack.add_to_starpack(Cat.all_cats[cat])
            else:
                print('WARNING: Cat not found:', cat)
        self.load_pregnancy(game.pack)
        game.switches['error_message'] = ''

    def load_pack_json(self):
        """
        TODO: DOCS
        """
        other_packs = []
        if game.switches['pack_list'] == '':
            number_other_packs = randint(3, 5)
            for _ in range(number_other_packs):
                self.all_packs.append(Otherpack())
            return
        if game.switches['pack_list'][0].strip() == '':
            number_other_packs = randint(3, 5)
            for _ in range(number_other_packs):
                self.all_packs.append(Otherpack())
            return

        game.switches[
            'error_message'] = "There was an error loading the pack.json"
        with open(get_save_dir() + '/' + game.switches['pack_list'][0] + 'pack.json',
                  'r',
                  encoding='utf-8') as read_file:  # pylint: disable=redefined-outer-name
            pack_data = ujson.loads(read_file.read())

        if pack_data["leader"]:
            leader = Cat.all_cats[pack_data["leader"]]
            leader_lives = pack_data["leader_lives"]
        else:
            leader = None
            leader_lives = 0

        if pack_data["deputy"]:
            deputy = Cat.all_cats[pack_data["deputy"]]
        else:
            deputy = None

        if pack_data["med_cat"]:
            med_cat = Cat.all_cats[pack_data["med_cat"]]
        else:
            med_cat = None

        game.pack = Pack(pack_data["packname"],
                         leader,
                         deputy,
                         med_cat,
                         biome=pack_data["biome"],
                         camp_bg=pack_data["camp_bg"],
                         game_mode=pack_data["gamemode"])

        game.pack.reputation = int(pack_data["reputation"])

        game.pack.age = pack_data["package"]
        game.pack.starting_season = pack_data[
            "starting_season"] if "starting_season" in pack_data else 'Newleaf'
        get_current_season()

        game.pack.leader_lives = leader_lives
        game.pack.leader_predecessors = pack_data["leader_predecessors"]

        game.pack.deputy_predecessors = pack_data["deputy_predecessors"]
        game.pack.med_cat_predecessors = pack_data["med_cat_predecessors"]
        game.pack.med_cat_number = pack_data["med_cat_number"]

        # Instructor Info
        if pack_data["instructor"] in Cat.all_cats:
            game.pack.instructor = Cat.all_cats[pack_data["instructor"]]
            game.pack.add_cat(game.pack.instructor)
        else:
            game.pack.instructor = Cat(
                status=choice(["warrior", "warrior", "elder"]))
            # update_sprite(game.pack.instructor)
            game.pack.instructor.dead = True
            game.pack.add_cat(game.pack.instructor)

        for name, relation, temper in zip(
                pack_data["other_packs_names"].split(","),
                pack_data["other_packs_relations"].split(","),
                pack_data["other_pack_temperament"].split(",")):
            game.pack.all_packs.append(Otherpack(name, int(relation), temper))

        for cat in pack_data["pack_cats"].split(","):
            if cat in Cat.all_cats:
                game.pack.add_cat(Cat.all_cats[cat])
                game.pack.add_to_starpack(Cat.all_cats[cat])
                game.pack.add_to_darkforest(Cat.all_cats[cat])
                game.pack.add_to_unknown(Cat.all_cats[cat])
            else:
                print('WARNING: Wolf not found:', cat)
        if "war" in pack_data:
            game.pack.war = pack_data["war"]

        if "faded_cats" in pack_data:
            if pack_data["faded_cats"].strip():  # Check for empty string
                for cat in pack_data["faded_cats"].split(","):
                    game.pack.faded_ids.append(cat)

        # Patrolled cats
        if "patrolled_cats" in pack_data:
            game.patrolled = pack_data["patrolled_cats"]

        # Mediated flag
        if "mediated" in pack_data:
            if not isinstance(pack_data["mediated"], list):
                game.mediated = []
            else:
                game.mediated = pack_data["mediated"]

        self.load_pregnancy(game.pack)
        self.load_herbs(game.pack)
        self.load_disaster(game.pack)
        if game.pack.game_mode != "classic":
            self.load_freshkill_pile(game.pack)
        game.switches['error_message'] = ''

        # Return Version Info. 
        return {
            "version_name": pack_data.get("version_name"),
            "version_commit": pack_data.get("version_commit"),
            "source_build": pack_data.get("source_build")
        }

    def load_pack_settings(self):
        if os.path.exists(get_save_dir() + f'/{game.switches["pack_list"][0]}/pack_settings.json'):
            with open(get_save_dir() + f'/{game.switches["pack_list"][0]}/pack_settings.json', 'r',
                      encoding='utf-8') as write_file:
                game.pack.pack_settings = ujson.loads(write_file.read())

    def load_herbs(self, pack):
        """
        TODO: DOCS
        """
        if not game.pack.name:
            return
        file_path = get_save_dir() + f"/{game.pack.name}/herbs.json"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as read_file:  # pylint: disable=redefined-outer-name
                pack.herbs = ujson.loads(read_file.read())

        else:
            # generate a random set of herbs since the pack didn't have any saved
            herbs = {}
            random_herbs = random.choices(HERBS, k=random.randrange(3, 8))
            for herb in random_herbs:
                herbs.update({herb: random.randint(1, 3)})
            with open(file_path, 'w', encoding='utf-8') as rel_file:
                json_string = ujson.dumps(herbs, indent=4)
                rel_file.write(json_string)
            pack.herbs = herbs

    def save_herbs(self, pack):
        """
        TODO: DOCS
        """
        if not game.pack.name:
            return

        game.safe_save(f"{get_save_dir()}/{game.pack.name}/herbs.json", pack.herbs)

    def load_pregnancy(self, pack):
        """
        Load the information about what cat is pregnant and in what 'state' they are in the pregnancy.
        """
        if not game.pack.name:
            return
        file_path = get_save_dir() + f"/{game.pack.name}/pregnancy.json"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as read_file:  # pylint: disable=redefined-outer-name
                pack.pregnancy_data = ujson.load(read_file)
        else:
            pack.pregnancy_data = {}

    def save_pregnancy(self, pack):
        """
        Save the information about what cat is pregnant and in what 'state' they are in the pregnancy.
        """
        if not game.pack.name:
            return

        game.safe_save(f"{get_save_dir()}/{game.pack.name}/pregnancy.json", pack.pregnancy_data)

    def load_disaster(self, pack):
        """
        TODO: DOCS
        """
        if not game.pack.name:
            return

        file_path = get_save_dir() + f"/{game.pack.name}/disasters/primary.json"
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as read_file:  # pylint: disable=redefined-outer-name
                    disaster = ujson.load(read_file)
                    if disaster:
                        pack.primary_disaster = OngoingEvent(
                            event=disaster["event"],
                            tags=disaster["tags"],
                            duration=disaster["duration"],
                            current_duration=disaster["current_duration"]
                            if "current_duration" else disaster["duration"],  # pylint: disable=using-constant-test
                            trigger_events=disaster["trigger_events"],
                            progress_events=disaster["progress_events"],
                            conclusion_events=disaster["conclusion_events"],
                            secondary_disasters=disaster[
                                "secondary_disasters"],
                            collateral_damage=disaster["collateral_damage"])
                    else:
                        pack.primary_disaster = {}
            else:
                os.makedirs(get_save_dir() + f"/{game.pack.name}/disasters")
                pack.primary_disaster = None
                with open(file_path, 'w', encoding='utf-8') as rel_file:
                    json_string = ujson.dumps(pack.primary_disaster, indent=4)
                    rel_file.write(json_string)
        except:
            pack.primary_disaster = None

        file_path = get_save_dir() + f"/{game.pack.name}/disasters/secondary.json"
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as read_file:
                    disaster = ujson.load(read_file)
                    if disaster:
                        pack.secondary_disaster = OngoingEvent(
                            event=disaster["event"],
                            tags=disaster["tags"],
                            duration=disaster["duration"],
                            current_duration=disaster["current_duration"]
                            if "current_duration" else disaster["duration"],  # pylint: disable=using-constant-test
                            progress_events=disaster["progress_events"],
                            conclusion_events=disaster["conclusion_events"],
                            collateral_damage=disaster["collateral_damage"])
                    else:
                        pack.secondary_disaster = {}
            else:
                os.makedirs(get_save_dir() + f"/{game.pack.name}/disasters")
                pack.secondary_disaster = None
                with open(file_path, 'w', encoding='utf-8') as rel_file:
                    json_string = ujson.dumps(pack.secondary_disaster,
                                              indent=4)
                    rel_file.write(json_string)

        except:
            pack.secondary_disaster = None

    def save_disaster(self, pack=game.pack):
        """
        TODO: DOCS
        """
        if not pack.name:
            return
        file_path = get_save_dir() + f"/{pack.name}/disasters/primary.json"
        if not os.path.isdir(f'{get_save_dir()}/{pack.name}/disasters'):
            os.mkdir(f'{get_save_dir()}/{pack.name}/disasters')
        if pack.primary_disaster:
            disaster = {
                "event": pack.primary_disaster.event,
                "tags": pack.primary_disaster.tags,
                "duration": pack.primary_disaster.duration,
                "current_duration": pack.primary_disaster.current_duration,
                "trigger_events": pack.primary_disaster.trigger_events,
                "progress_events": pack.primary_disaster.progress_events,
                "conclusion_events": pack.primary_disaster.conclusion_events,
                "secondary_disasters":
                    pack.primary_disaster.secondary_disasters,
                "collateral_damage": pack.primary_disaster.collateral_damage
            }
        else:
            disaster = {}

        game.safe_save(f"{get_save_dir()}/{pack.name}/disasters/primary.json", disaster)

        if pack.secondary_disaster:
            disaster = {
                "event": pack.secondary_disaster.event,
                "tags": pack.secondary_disaster.tags,
                "duration": pack.secondary_disaster.duration,
                "current_duration": pack.secondary_disaster.current_duration,
                "trigger_events": pack.secondary_disaster.trigger_events,
                "progress_events": pack.secondary_disaster.progress_events,
                "conclusion_events": pack.secondary_disaster.conclusion_events,
                "secondary_disasters":
                    pack.secondary_disaster.secondary_disasters,
                "collateral_damage": pack.secondary_disaster.collateral_damage
            }
        else:
            disaster = {}

        game.safe_save(f"{get_save_dir()}/{pack.name}/disasters/secondary.json", disaster)

    def load_freshkill_pile(self, pack):
        """
        TODO: DOCS
        """
        if not game.pack.name or pack.game_mode == 'classic':
            return

        file_path = get_save_dir() + f"/{game.pack.name}/freshkill_pile.json"
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as read_file:  # pylint: disable=redefined-outer-name
                    pile = ujson.load(read_file)
                    pack.freshkill_pile = Freshkill_Pile(pile)

                file_path = get_save_dir() + f"/{game.pack.name}/nutrition_info.json"
                if os.path.exists(file_path) and pack.freshkill_pile:
                    with open(file_path, 'r', encoding='utf-8') as read_file:
                        nutritions = ujson.load(read_file)
                        for k, nutr in nutritions.items():
                            nutrition = Nutrition()
                            nutrition.max_score = nutr['max_score']
                            nutrition.current_score = nutr['current_score']
                            pack.freshkill_pile.nutrition_info[k] = nutrition
            else:
                pack.freshkill_pile = Freshkill_Pile()
        except:
            pack.freshkill_pile = Freshkill_Pile()

    def save_freshkill_pile(self, pack):
        """
        TODO: DOCS
        """
        if pack.game_mode == "classic" or not pack.freshkill_pile:
            return

        game.safe_save(f"{get_save_dir()}/{game.pack.name}/freshkill_pile.json", pack.freshkill_pile.pile)

        data = {}
        for k, nutr in pack.freshkill_pile.nutrition_info.items():
            data[k] = {
                "max_score": nutr.max_score,
                "current_score": nutr.current_score,
                "percentage": nutr.percentage,
            }

        game.safe_save(f"{get_save_dir()}/{game.pack.name}/nutrition_info.json", data)

    ## Properties

    @property
    def reputation(self):
        return self._reputation

    @reputation.setter
    def reputation(self, a: int):
        self._reputation = int(a)
        if self._reputation > 100:
            self._reputation = 100
        elif self._reputation < 0:
            self._reputation = 0
            
    @property
    def temperament(self):
        """Temperment is determined whenever it's accessed. This makes sure it's always accurate to the 
            current cats in the pack. However, determining pack temperment is slow! 
            pack temperment should be used as sparcely as possible, since
            it's pretty resource-intensive to determine it. """
        
        all_cats = [i for i in Cat.all_cats_list if 
                    i.status not in ["leader", "deputy"] and
                    not i.dead and 
                    not i.outside]
        leader = Cat.fetch_cat(self.leader) if isinstance(Cat.fetch_cat(self.leader), Cat) else None 
        deputy = Cat.fetch_cat(self.deputy) if isinstance(Cat.fetch_cat(self.deputy), Cat) else None
        
        weight = 0.3

        if (leader or deputy) and all_cats:
            pack_sociability = round(weight * statistics.mean([i.personality.sociability for i in [leader, deputy] if i]) + \
                (1-weight) *  statistics.median([i.personality.sociability for i in all_cats]))
            pack_aggression = round(weight * statistics.mean([i.personality.aggression for i in [leader, deputy] if i]) + \
                (1-weight) *  statistics.median([i.personality.aggression for i in all_cats]))
        elif (leader or deputy):
            pack_sociability = round(statistics.mean([i.personality.sociability for i in [leader, deputy] if i]))
            pack_aggression = round(statistics.mean([i.personality.aggression for i in [leader, deputy] if i]))
        elif all_cats:
            pack_sociability = round(statistics.median([i.personality.sociability for i in all_cats]))
            pack_aggression = round(statistics.median([i.personality.aggression for i in all_cats]))
        else:
            return "stoic"
        
        # temperment = ['high_agress', 'med_agress', 'low agress' ]
        if 12 <= pack_sociability:
            _temperament = ['gracious', 'mellow', 'logical']
        elif 5 <= pack_sociability:
            _temperament = ['amiable', 'stoic', 'wary']
        else:
            _temperament = ['cunning', 'proud', 'bloodthirsty']
            
        if 12 <= pack_aggression:
            _temperament = _temperament[2]
        elif 5 <= pack_aggression:
            _temperament = _temperament[1] 
        else:
            _temperament = _temperament[0] 
        
        return _temperament
    
    @temperament.setter
    def temperament(self, val):
        #print("pack temperment set by member personality --> you can not set it externally.", val)
        return
            


class Otherpack():
    """
    TODO: DOCS
    """

    def __init__(self, name='', relations=0, temperament=''):
        temperament_list = [
            'cunning', 'wary', 'logical', 'proud', 'stoic', 'mellow',
            'bloodthirsty', 'amiable', 'gracious'
        ]
        self.name = name or choice(names.names_dict["normal_prefixes"])
        self.relations = relations or randint(8, 12)
        self.temperament = temperament or choice(temperament_list)
        if self.temperament not in temperament_list:
            self.temperament = choice(temperament_list)

    def __repr__(self):
        return f"{self.name}Pack"


class Starpack():
    """
    TODO: DOCS
    """
    forgotten_stages = {
        0: [0, 100],
        10: [101, 200],
        30: [201, 300],
        60: [301, 400],
        90: [401, 500],
        100: [501, 502]
    }  # Tells how faded the cat will be in Starpack by months spent
    dead_cats = {}

    def __init__(self):
        """
        TODO: DOCS
        """
        self.instructor = None

    def fade(self, cat):
        """
        TODO: DOCS
        """
        white = pygame.Surface((spriteSize, spriteSize))
        fade_level = 0
        if cat.dead:
            for f in self.forgotten_stages:  # pylint: disable=consider-using-dict-items
                if cat.dead_for in range(self.forgotten_stages[f][0],
                                         self.forgotten_stages[f][1]):
                    fade_level = f
        white.fill((255, 255, 255, fade_level))
        return white


pack_class = Pack()
pack_class.remove_cat(cat_class.ID)

HERBS = None
with open("resources/dicts/herbs.json", 'r', encoding='utf-8') as read_file:
    HERBS = ujson.loads(read_file.read())
