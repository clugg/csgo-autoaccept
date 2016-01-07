"""
csgo-autoaccept

Provides specific functionality for Valve's official matchmaking service.
"""

import logging

import base

# use this to find csgo's hwnd
WINDOW_TITLE = base.re.compile("^Counter-Strike: Global Offensive$")
VALID_RGB = {
    (8, 59, 24), (0, 117, 75), (0, 107, 27), (74, 181, 139), (4, 89, 70), (5, 94, 73),
    (0, 96, 26), (9, 140, 99), (0, 127, 34), (222, 241, 233), (3, 71, 55), (33, 147, 110),
    (207, 234, 222), (232, 248, 240), (7, 55, 23), (6, 114, 81), (0, 123, 49), (3, 102, 76),
    (41, 138, 105), (31, 144, 108), (2, 83, 67), (221, 240, 232), (5, 131, 91), (81, 168, 137),
    (8, 106, 78), (70, 148, 122), (70, 159, 129), (17, 136, 97), (13, 145, 103), (2, 61, 19),
    (3, 75, 63), (4, 97, 73), (4, 128, 88), (20, 146, 105), (3, 84, 67), (51, 145, 112),
    (3, 83, 32), (14, 146, 103), (6, 97, 74), (0, 117, 28), (241, 249, 246), (1, 94, 72),
    (6, 53, 22), (214, 233, 225), (19, 145, 105), (6, 110, 80), (4, 67, 49),
    (3, 109, 79), (8, 113, 81), (6, 103, 77), (227, 246, 238), (4, 64, 44), (113, 182, 154),
    (22, 149, 108), (74, 165, 133), (2, 108, 79), (7, 112, 80), (40, 144, 108), (9, 132, 92),
    (157, 207, 188), (4, 117, 83), (8, 109, 80), (5, 102, 77), (0, 124, 49), (2, 84, 32),
    (0, 118, 77), (5, 83, 68), (156, 197, 182), (240, 249, 245), (51, 134, 103), (0, 120, 30),
    (1, 113, 81), (7, 91, 72), (150, 202, 182), (0, 99, 29), (4, 69, 53), (40, 154, 117),
    (84, 194, 150), (246, 251, 250), (188, 222, 208), (6, 134, 93), (7, 143, 101), (35, 155, 116),
    (20, 143, 104), (3, 98, 75), (1, 67, 19), (3, 85, 68), (5, 107, 78), (198, 224, 213),
    (2, 68, 39), (2, 84, 67), (0, 122, 32), (73, 163, 132), (154, 209, 190), (5, 69, 53),
    (50, 146, 112), (5, 106, 78), (3, 57, 19), (36, 149, 113), (0, 100, 69), (0, 96, 27),
    (0, 101, 70), (0, 73, 22), (6, 52, 21), (17, 137, 98), (15, 67, 35), (31, 161, 120),
    (209, 230, 222), (244, 251, 248), (16, 129, 92), (15, 136, 96), (3, 77, 64), (80, 170, 138),
    (76, 191, 144), (19, 136, 97), (32, 159, 118), (4, 57, 39), (1, 122, 85), (2, 81, 66),
    (0, 113, 39), (89, 177, 144), (30, 135, 99), (70, 158, 128), (218, 246, 233), (3, 72, 56),
    (206, 232, 221), (3, 130, 89), (0, 117, 76), (19, 108, 82), (9, 115, 83), (5, 115, 82),
    (6, 139, 97), (235, 249, 244), (49, 152, 116), (9, 65, 28), (6, 86, 69), (0, 124, 33),
    (6, 133, 92), (7, 114, 82), (113, 191, 159), (225, 242, 235), (0, 97, 73), (4, 77, 64),
    (202, 230, 219), (0, 107, 73), (7, 85, 69), (7, 88, 70), (3, 128, 87), (81, 162, 134),
    (3, 118, 83), (0, 129, 36), (1, 124, 85), (4, 96, 73), (230, 248, 240), (5, 98, 75),
    (0, 108, 27), (193, 221, 209), (4, 92, 71), (3, 84, 68), (227, 242, 236), (241, 250, 247),
    (6, 98, 75), (109, 169, 148), (8, 96, 74), (3, 86, 69), (28, 155, 115), (74, 158, 130),
    (36, 176, 130), (2, 100, 75), (148, 206, 185), (7, 135, 94), (63, 174, 132), (6, 115, 82),
    (54, 165, 128), (4, 109, 80), (4, 120, 84), (245, 250, 248), (3, 102, 77), (3, 108, 78),
    (9, 119, 85), (249, 254, 252), (20, 141, 102), (6, 94, 72), (1, 86, 68), (1, 80, 28),
    (13, 145, 102), (3, 115, 81), (214, 238, 228), (4, 97, 74), (2, 90, 70), (1, 72, 46),
    (0, 107, 36), (9, 66, 29), (112, 185, 155), (47, 156, 120), (4, 76, 64), (238, 249, 244),
    (212, 233, 224), (12, 141, 99), (2, 82, 67), (222, 244, 234), (74, 188, 143), (16, 134, 96),
    (3, 92, 71), (190, 231, 214), (0, 123, 75), (73, 165, 133), (0, 130, 55), (45, 155, 118),
    (1, 97, 74), (81, 164, 135), (5, 112, 80), (92, 171, 142), (5, 103, 77), (0, 119, 30),
    (18, 134, 96), (6, 105, 78), (8, 78, 33), (4, 80, 66), (150, 203, 184), (41, 145, 110),
    (7, 112, 81), (196, 220, 211), (7, 133, 92), (196, 232, 216), (0, 91, 66), (102, 186, 152),
    (70, 155, 126), (7, 126, 87), (6, 145, 102), (3, 93, 72), (13, 124, 88), (3, 78, 64),
    (98, 179, 148), (3, 100, 75), (240, 249, 246), (22, 138, 100), (7, 80, 67), (9, 64, 28),
    (6, 137, 94), (24, 167, 122), (1, 101, 75), (153, 208, 189), (203, 231, 219), (4, 99, 75),
    (204, 229, 218), (3, 112, 80), (214, 239, 227), (10, 139, 98), (7, 143, 100), (5, 74, 61),
    (0, 92, 66), (194, 225, 212), (6, 84, 69), (18, 55, 37), (2, 96, 73), (70, 161, 129),
    (11, 134, 94), (4, 83, 67), (5, 96, 74), (236, 244, 241), (9, 138, 96), (5, 41, 18),
    (249, 253, 251), (81, 172, 139), (251, 254, 253), (17, 133, 95), (0, 117, 44), (6, 89, 70),
    (1, 98, 75), (73, 166, 133), (8, 136, 95), (235, 247, 242), (6, 92, 72), (7, 98, 75),
    (4, 110, 80), (0, 118, 29), (0, 95, 26), (34, 145, 109), (2, 101, 76), (15, 142, 101),
    (5, 81, 67), (146, 194, 175), (8, 114, 81), (3, 127, 88), (0, 117, 77), (250, 254, 252),
    (46, 177, 132), (4, 129, 89), (1, 114, 81), (38, 161, 122), (226, 242, 236), (74, 159, 130),
    (24, 123, 91), (192, 230, 213), (2, 86, 68), (113, 191, 158), (241, 248, 246), (32, 132, 96),
    (5, 46, 34), (1, 70, 43), (202, 230, 218), (0, 107, 78), (231, 246, 240), (194, 230, 214),
    (6, 91, 72), (10, 126, 88), (2, 65, 35), (14, 135, 96), (73, 164, 132), (5, 145, 101),
    (0, 122, 30), (72, 188, 142), (1, 109, 79), (2, 113, 81), (6, 98, 74), (6, 83, 67),
    (8, 123, 86), (205, 231, 221), (8, 77, 34), (198, 234, 218), (2, 100, 74), (10, 68, 32),
    (172, 222, 202), (2, 106, 78), (29, 139, 103), (7, 108, 80), (94, 153, 134), (0, 96, 73),
    (5, 61, 42), (3, 108, 79), (15, 124, 89), (6, 85, 69), (6, 124, 86), (7, 113, 82),
    (0, 132, 59), (1, 80, 29), (6, 107, 78), (6, 90, 71), (13, 110, 81), (33, 165, 124),
    (4, 97, 75), (5, 129, 88), (9, 112, 80), (79, 167, 136), (0, 100, 75), (30, 162, 120),
    (153, 210, 190), (5, 85, 68), (71, 165, 132), (146, 199, 178), (224, 239, 233), (195, 226, 212),
    (89, 173, 143), (2, 82, 66), (8, 95, 73), (4, 75, 64), (4, 133, 92), (9, 63, 26),
    (0, 98, 33), (5, 127, 88), (0, 93, 66), (154, 208, 189), (0, 72, 22), (70, 163, 131),
    (0, 94, 71), (0, 103, 71), (16, 140, 100), (6, 93, 72), (2, 118, 82), (32, 167, 125),
    (239, 250, 244), (8, 132, 92), (3, 69, 53), (4, 55, 31), (0, 115, 42), (0, 128, 53),
    (52, 168, 128), (7, 138, 96), (2, 109, 79), (4, 86, 69), (0, 82, 60), (0, 77, 22),
    (2, 91, 70), (5, 112, 81), (86, 160, 135), (245, 249, 248), (3, 123, 85), (236, 251, 245),
    (5, 76, 64), (8, 102, 77), (7, 88, 71), (0, 108, 37), (7, 119, 84), (7, 136, 95),
    (2, 92, 72), (1, 81, 30), (5, 96, 73), (252, 254, 253), (0, 98, 74), (7, 118, 83),
    (1, 107, 78), (10, 75, 35), (217, 243, 231), (9, 124, 87), (6, 84, 68), (0, 99, 74),
    (171, 217, 200), (11, 129, 89), (0, 80, 20), (7, 100, 75), (1, 75, 48), (215, 235, 227),
    (37, 140, 104), (12, 129, 90), (5, 78, 65), (236, 249, 244), (5, 52, 37), (73, 157, 129),
    (12, 149, 105), (9, 122, 85), (27, 146, 108), (0, 86, 25), (13, 70, 35), (4, 91, 71),
    (2, 79, 64), (0, 133, 59), (244, 250, 248), (11, 68, 32), (0, 113, 81), (238, 248, 243),
    (5, 83, 34), (6, 109, 80), (5, 79, 65), (6, 88, 69), (0, 77, 25), (243, 250, 248),
    (48, 150, 116), (86, 157, 134), (5, 81, 66), (0, 99, 30), (213, 239, 228), (12, 112, 81),
    (7, 77, 33), (7, 106, 78), (8, 105, 78), (0, 117, 78), (240, 250, 246), (11, 129, 90),
    (3, 120, 84), (2, 88, 70), (13, 143, 101), (83, 154, 132), (2, 77, 64), (207, 234, 221),
    (214, 236, 227), (112, 186, 156), (7, 115, 83), (9, 128, 89), (3, 103, 76), (1, 74, 48),
    (0, 73, 21), (233, 245, 240), (245, 253, 250), (214, 242, 230), (247, 254, 250), (7, 93, 72),
    (3, 83, 33), (113, 192, 159), (8, 119, 85), (6, 135, 93), (25, 110, 84), (25, 145, 108),
    (0, 118, 45), (9, 63, 28), (6, 83, 68), (35, 133, 98), (0, 76, 25), (7, 140, 97),
    (0, 105, 72), (1, 78, 27), (8, 127, 88), (41, 122, 94), (75, 137, 116), (8, 117, 82),
    (166, 209, 195), (11, 130, 90), (35, 150, 113), (2, 106, 77), (93, 187, 150), (8, 122, 85),
    (205, 231, 220), (146, 198, 179), (5, 109, 79), (9, 114, 83), (0, 113, 40), (9, 115, 82),
    (0, 103, 76), (7, 101, 76), (16, 140, 99), (0, 115, 27), (247, 253, 250), (209, 232, 222),
    (155, 207, 188), (2, 93, 72), (0, 106, 34), (6, 107, 79), (4, 83, 34), (8, 139, 97),
    (34, 163, 123), (0, 105, 76), (9, 112, 81), (0, 110, 79), (0, 100, 74), (192, 229, 212),
    (10, 133, 93), (2, 94, 73), (7, 105, 78), (237, 248, 242), (5, 68, 51), (33, 158, 118),
    (0, 87, 64), (8, 24, 18), (10, 66, 31), (16, 133, 95), (0, 77, 26), (24, 157, 116),
    (32, 131, 97), (36, 139, 104), (4, 133, 93), (230, 246, 239), (157, 211, 192), (0, 99, 24),
    (11, 135, 95), (8, 117, 83), (239, 249, 245), (30, 147, 108), (5, 138, 96), (6, 127, 87),
    (5, 48, 20), (2, 66, 36), (0, 114, 41), (213, 238, 227), (0, 81, 58), (236, 245, 241),
    (5, 72, 57), (6, 82, 67), (78, 167, 136), (195, 228, 213), (0, 75, 24), (73, 160, 131),
    (1, 79, 28), (50, 167, 128), (2, 103, 76), (4, 66, 46), (12, 153, 109), (3, 106, 77),
    (10, 128, 88), (234, 245, 241), (7, 115, 82), (0, 112, 74), (212, 232, 224), (8, 102, 76),
    (0, 133, 60), (67, 149, 121), (34, 160, 120), (4, 131, 90), (4, 107, 79), (1, 90, 70),
    (33, 150, 113), (5, 75, 64), (222, 240, 232), (243, 249, 247), (86, 148, 130), (202, 225, 216),
    (0, 101, 31), (0, 109, 78), (146, 203, 181), (139, 191, 170), (229, 241, 236), (2, 84, 68),
    (7, 100, 76), (223, 240, 233), (0, 115, 35), (16, 135, 96), (0, 84, 23), (0, 109, 37),
    (10, 130, 91), (4, 93, 72), (5, 133, 92), (6, 52, 22), (6, 81, 67), (173, 217, 201),
    (52, 148, 115), (43, 165, 125), (0, 126, 51), (11, 68, 33), (6, 140, 97), (6, 48, 20),
    (5, 92, 72), (194, 227, 213), (8, 137, 95), (0, 122, 64), (19, 138, 100), (128, 207, 174),
    (206, 230, 220), (7, 99, 75), (213, 239, 227), (4, 91, 70), (134, 195, 170), (6, 75, 63),
    (7, 108, 79), (6, 127, 88), (16, 65, 36), (249, 254, 250), (2, 123, 85), (9, 124, 86),
    (0, 127, 75), (13, 143, 100), (251, 254, 252), (214, 236, 226), (16, 130, 93), (4, 130, 89),
    (243, 247, 246), (0, 130, 56), (51, 144, 111), (251, 253, 251), (3, 91, 70), (8, 114, 82),
    (4, 118, 83), (37, 148, 112), (7, 86, 69), (2, 82, 30), (0, 119, 45), (0, 107, 35),
    (2, 65, 33), (2, 99, 74), (214, 238, 227), (80, 166, 137), (194, 225, 211), (6, 135, 94),
    (0, 91, 34), (74, 164, 133), (10, 138, 97), (6, 92, 71), (1, 108, 78), (21, 127, 92),
    (32, 166, 123), (79, 168, 137), (6, 101, 76), (19, 155, 112), (3, 87, 69), (5, 100, 75),
    (2, 83, 32), (5, 118, 83), (6, 88, 70), (11, 130, 91), (36, 161, 122), (34, 149, 112),
    (244, 249, 248), (0, 97, 68), (195, 234, 217), (6, 108, 79), (30, 138, 102), (1, 119, 83),
    (2, 80, 66), (247, 253, 249), (8, 110, 80), (4, 59, 41), (9, 133, 92), (0, 99, 69),
    (86, 162, 137), (196, 229, 213), (222, 242, 233), (37, 144, 108), (1, 79, 27), (1, 72, 45),
    (0, 93, 24), (10, 149, 105), (0, 131, 58), (3, 107, 78), (2, 85, 68), (221, 242, 233),
    (234, 247, 241), (149, 205, 184), (2, 117, 82), (189, 223, 208), (4, 85, 69), (4, 117, 82),
    (7, 144, 101), (21, 133, 97), (9, 123, 86), (4, 103, 78), (148, 206, 184), (0, 99, 25),
    (86, 166, 138), (8, 137, 96), (239, 249, 244), (1, 93, 72), (5, 95, 74), (4, 73, 59),
    (5, 126, 86), (0, 83, 62), (0, 82, 21), (78, 165, 135), (1, 78, 26), (4, 79, 65),
    (246, 250, 249), (208, 235, 223), (8, 93, 72), (45, 147, 112), (224, 242, 235), (34, 145, 108),
    (4, 88, 69), (12, 135, 95), (50, 151, 116), (17, 160, 115), (70, 157, 128), (6, 145, 101),
    (4, 114, 81), (35, 144, 107), (3, 80, 66), (60, 180, 135), (112, 187, 156), (70, 162, 130),
    (227, 243, 237), (23, 145, 106), (4, 65, 46), (6, 97, 75), (239, 250, 245), (4, 131, 91),
    (12, 133, 93), (2, 86, 69), (8, 131, 91), (17, 145, 103), (0, 122, 31), (170, 213, 199),
    (242, 251, 248), (7, 31, 18), (16, 120, 87), (113, 188, 158), (18, 61, 36), (4, 106, 77),
    (1, 110, 80), (2, 119, 83), (245, 251, 249), (4, 75, 62), (9, 103, 77), (5, 114, 81),
    (51, 153, 118), (23, 152, 110), (0, 128, 54), (109, 186, 155), (67, 159, 128), (2, 97, 74),
    (6, 50, 21), (10, 130, 90), (4, 74, 61), (5, 46, 19), (5, 84, 68), (0, 78, 25),
    (6, 40, 18), (0, 105, 33), (28, 140, 103), (239, 248, 243), (52, 148, 114), (2, 79, 66),
    (3, 96, 73), (246, 253, 250), (88, 163, 138), (175, 226, 205), (2, 112, 80), (5, 75, 63),
    (6, 113, 81), (0, 103, 32), (4, 66, 48), (234, 248, 241), (0, 90, 66), (68, 143, 116),
    (3, 59, 32), (0, 76, 50), (218, 235, 227), (2, 122, 85), (0, 76, 19), (4, 88, 70),
    (2, 123, 86), (36, 143, 107), (0, 112, 80), (10, 128, 89), (5, 137, 94), (5, 101, 75),
    (1, 73, 48), (229, 242, 238), (11, 72, 34), (0, 123, 32), (241, 248, 245), (151, 200, 181),
    (0, 81, 20), (19, 138, 99), (0, 91, 24), (3, 97, 73), (10, 120, 85), (0, 107, 77),
    (3, 72, 57), (0, 100, 31), (57, 137, 106), (226, 243, 236), (7, 138, 97), (1, 92, 72),
    (72, 176, 138), (97, 162, 139), (6, 95, 73), (5, 50, 21), (38, 143, 107), (6, 100, 75),
    (5, 81, 33), (1, 65, 18), (8, 120, 85), (1, 108, 79), (1, 102, 76), (0, 69, 19),
    (212, 236, 226), (0, 97, 27), (250, 253, 251), (16, 138, 98), (80, 163, 134), (3, 88, 69),
    (7, 91, 71), (4, 87, 69), (79, 147, 125), (5, 74, 63), (0, 84, 64), (2, 115, 81),
    (3, 95, 73), (8, 103, 77), (30, 138, 101), (3, 82, 66), (0, 126, 34), (11, 147, 103),
    (8, 129, 89), (36, 145, 110), (5, 45, 33), (11, 130, 89), (239, 247, 243), (0, 112, 39),
    (17, 148, 105), (33, 146, 109), (0, 72, 19), (7, 30, 19), (27, 127, 91), (3, 92, 72),
    (2, 85, 69), (4, 70, 53), (82, 167, 138), (2, 117, 83), (232, 242, 239), (10, 66, 29),
    (0, 113, 75), (0, 108, 34), (233, 243, 240), (6, 117, 83), (80, 165, 136), (51, 154, 119),
    (205, 229, 219), (143, 201, 178), (4, 103, 76), (1, 96, 73), (3, 99, 75), (215, 241, 229),
    (5, 126, 87), (10, 155, 110), (55, 148, 117), (0, 109, 64), (4, 84, 68), (4, 72, 59),
    (233, 242, 239), (1, 118, 82), (9, 135, 95), (0, 85, 64), (224, 242, 234), (6, 119, 84),
    (67, 176, 134), (6, 120, 85), (0, 127, 52), (17, 138, 98), (0, 101, 75), (8, 107, 79),
    (1, 105, 77), (6, 130, 89), (1, 91, 71), (3, 123, 86), (7, 141, 98), (50, 147, 114),
    (0, 133, 62), (132, 184, 162), (8, 147, 103), (96, 172, 144), (9, 134, 94), (241, 249, 247),
    (4, 122, 85), (14, 122, 88), (0, 94, 72), (5, 41, 19), (92, 181, 147), (0, 110, 39),
    (3, 76, 63), (18, 61, 37), (2, 119, 84), (245, 251, 248), (6, 96, 74), (57, 180, 135),
    (237, 245, 242), (5, 108, 79), (234, 247, 242), (232, 247, 240), (18, 143, 103), (5, 95, 73),
    (16, 132, 94), (10, 107, 79), (8, 138, 97), (194, 218, 208), (195, 230, 214), (0, 98, 29),
    (5, 122, 85), (5, 70, 55), (81, 165, 136), (167, 213, 196), (9, 108, 80), (216, 236, 227),
    (3, 89, 70), (3, 119, 83), (232, 243, 239), (191, 226, 210), (16, 133, 94), (15, 139, 99),
    (7, 122, 85), (70, 160, 129), (0, 103, 33), (164, 230, 204), (7, 98, 74), (4, 71, 57),
    (4, 68, 51), (2, 122, 84), (0, 122, 47), (4, 113, 81), (0, 94, 25), (6, 128, 88),
    (1, 84, 68), (3, 117, 82), (77, 152, 128), (0, 102, 32), (7, 135, 93), (0, 75, 23),
    (0, 127, 36), (50, 150, 115), (34, 148, 110), (1, 100, 75), (50, 155, 120), (223, 239, 232),
    (3, 75, 62), (4, 78, 65), (10, 131, 91), (5, 53, 39), (80, 164, 134), (212, 238, 226),
    (230, 244, 239), (7, 106, 79), (234, 244, 241), (230, 241, 237), (0, 100, 30), (0, 115, 75),
    (36, 146, 110), (243, 250, 247), (103, 189, 155), (213, 236, 227), (2, 80, 29), (3, 101, 76),
    (24, 140, 101), (186, 215, 204), (233, 247, 240), (233, 244, 240), (94, 160, 137), (8, 59, 25),
    (11, 67, 31), (0, 97, 28), (115, 200, 163), (8, 127, 87), (5, 105, 77), (32, 148, 110),
    (137, 187, 166), (6, 87, 69), (146, 184, 169), (11, 123, 87), (204, 228, 218), (11, 142, 100),
    (14, 122, 87), (223, 243, 234), (2, 115, 82), (3, 95, 72), (73, 162, 131), (3, 134, 92),
    (3, 82, 67), (0, 74, 23), (46, 142, 109), (51, 149, 115), (0, 72, 21), (3, 124, 85),
    (4, 109, 79), (227, 239, 234), (0, 95, 72), (8, 61, 25), (213, 233, 225), (0, 128, 36),
    (36, 160, 120), (3, 107, 79), (46, 149, 114), (0, 101, 76), (156, 223, 197), (21, 142, 102),
    (73, 161, 131), (86, 193, 150), (12, 136, 96), (2, 99, 75), (14, 153, 108), (73, 157, 130),
    (16, 134, 95), (213, 238, 226), (235, 249, 242), (2, 120, 83), (12, 69, 34), (235, 248, 241),
    (28, 168, 124), (0, 94, 67), (0, 92, 23), (5, 115, 81), (213, 235, 226), (9, 114, 82),
    (82, 150, 129), (5, 80, 66), (5, 72, 59), (4, 84, 67), (6, 91, 71), (224, 239, 232),
    (25, 139, 102), (70, 161, 130), (5, 103, 76), (215, 241, 230), (7, 117, 83),
    (7, 124, 87), (72, 147, 124), (0, 110, 80), (3, 90, 70), (5, 77, 65), (206, 228, 218),
    (0, 118, 75), (6, 137, 95), (4, 71, 55), (1, 78, 54), (239, 248, 245), (248, 251, 250),
    (6, 108, 80), (134, 212, 180), (1, 112, 80), (6, 112, 81), (4, 131, 89), (113, 183, 155),
    (198, 233, 217), (4, 138, 95), (4, 122, 84), (115, 187, 158), (2, 79, 65), (0, 89, 65),
    (7, 124, 86), (9, 110, 80), (26, 150, 111), (227, 238, 233), (0, 117, 82), (3, 81, 67),
    (2, 91, 71), (0, 76, 24), (93, 161, 138), (5, 95, 72), (238, 247, 242), (4, 70, 55),
    (49, 152, 118), (3, 109, 80), (57, 148, 116), (8, 138, 96), (29, 146, 108), (10, 141, 100),
    (0, 98, 28), (0, 106, 77), (0, 96, 68), (10, 131, 92), (7, 109, 80), (3, 57, 18),
    (10, 129, 89), (7, 130, 91), (53, 176, 132), (113, 187, 157), (6, 140, 98), (20, 159, 116),
    (2, 65, 36), (8, 118, 83), (0, 72, 20), (15, 139, 98), (3, 94, 72), (164, 212, 194),
    (42, 147, 112), (15, 136, 97), (87, 167, 139), (18, 156, 113), (11, 110, 81), (0, 79, 56),
    (6, 123, 85), (35, 147, 109), (208, 227, 219), (3, 127, 87), (172, 209, 196), (8, 106, 79),
    (6, 79, 65), (5, 94, 72), (74, 162, 132), (3, 113, 81), (1, 99, 75), (1, 94, 71),
    (0, 102, 76), (14, 127, 90), (7, 120, 84), (2, 83, 66), (4, 118, 84), (3, 73, 59),
    (230, 244, 238), (0, 126, 36), (223, 241, 235), (0, 100, 29), (37, 145, 109), (70, 159, 128),
    (113, 189, 158), (17, 136, 96), (4, 72, 57), (5, 130, 90), (14, 66, 35), (9, 130, 90),
    (4, 75, 63), (14, 150, 107), (4, 106, 78), (6, 35, 19), (5, 77, 64), (1, 103, 76),
    (4, 100, 75), (232, 244, 239), (3, 87, 70), (0, 122, 75), (5, 70, 53), (37, 147, 110),
    (7, 57, 24), (5, 132, 91), (1, 76, 25), (11, 123, 86), (26, 157, 116), (0, 93, 71),
    (66, 133, 108), (26, 147, 108), (2, 69, 41), (0, 103, 72), (3, 89, 71), (96, 173, 144),
    (4, 46, 18), (3, 74, 61), (7, 87, 69), (3, 124, 86), (150, 205, 185), (0, 95, 73),
    (8, 61, 26), (213, 233, 224), (0, 128, 35), (2, 88, 69), (8, 133, 93), (1, 88, 69),
    (67, 182, 138), (5, 102, 76), (0, 131, 57), (191, 225, 210), (2, 84, 33), (0, 80, 56),
    (16, 170, 122), (9, 128, 88), (6, 130, 90), (2, 89, 70), (83, 160, 135), (11, 132, 93),
    (2, 76, 63), (2, 92, 71), (25, 156, 115), (5, 76, 65), (235, 248, 242), (0, 98, 73),
    (7, 89, 70), (10, 133, 92), (53, 159, 123), (4, 110, 79), (7, 79, 34), (0, 108, 73),
    (204, 229, 219), (3, 85, 69), (2, 87, 69), (5, 107, 79), (37, 151, 114), (2, 76, 64),
    (49, 156, 120), (7, 117, 82), (10, 153, 109), (8, 126, 87), (5, 106, 77), (7, 95, 74),
    (228, 239, 234), (154, 210, 190), (1, 95, 72), (2, 109, 80), (17, 131, 94), (214, 233, 226),
    (3, 78, 65), (251, 253, 253), (147, 201, 180), (2, 67, 38), (78, 171, 137), (3, 132, 91),
    (42, 176, 131), (217, 234, 228), (0, 108, 78), (3, 83, 67), (6, 112, 80), (5, 82, 67),
    (1, 87, 69), (3, 105, 77), (1, 92, 71), (16, 168, 121), (196, 233, 216), (113, 188, 157),
    (11, 138, 96), (1, 71, 43), (1, 89, 70), (0, 109, 74), (70, 156, 128), (1, 91, 70),
    (6, 55, 23), (46, 134, 101), (15, 126, 89), (96, 162, 140), (3, 81, 66), (232, 245, 240),
    (4, 102, 76), (206, 231, 221), (6, 139, 96), (238, 247, 243), (13, 118, 86), (98, 171, 145),
    (9, 65, 29), (7, 97, 74), (0, 114, 27), (5, 110, 80), (7, 92, 72), (110, 182, 154),
    (0, 120, 47), (4, 50, 36), (0, 91, 23), (3, 79, 65), (244, 250, 247), (6, 123, 86),
    (106, 160, 141), (0, 77, 52), (0, 115, 81), (12, 131, 92), (4, 81, 67), (5, 98, 74),
    (22, 150, 110), (97, 207, 162), (25, 145, 107), (99, 181, 149), (5, 99, 75)
}

log = logging.getLogger("services.mm")

get_hwnd = lambda: base.get_hwnd(WINDOW_TITLE)
focused = lambda: base.focused(WINDOW_TITLE)
exists = lambda: base.exists(WINDOW_TITLE)
screenshot = lambda: base.screenshot(WINDOW_TITLE)

def get_accept():
    """
    Find the accept button if the CS:GO window exists.

    Returns:
        tuple: x, y coordinates of accept button.
        bool: False if no CS:GO window exists or no accept button is found.
    """

    game = screenshot()
    if not game:
        log.debug("get_accept failed: csgo not running")
        return False
    elif not focused():
        log.debug("get_accept failed: csgo not focused")
        return False

    startx, starty, _, _ = base.win32gui.GetWindowRect(get_hwnd())
    w, h = game.size
    pixels = game.load()
    # assume button is in top left quarter of game window
    for x in range(0, w // 2, 4): # skip 4 horizontal pixels at a time due to vertical gradient
        for y in range(0, h // 2):
            if pixels[x, y] in VALID_RGB:
                log.debug("get_accept found valid colour {} at {}, {}".format(pixels[x, y], x, y))
                return startx + x, starty + y
    log.debug("get_accept failed: accept not found")
    return False
