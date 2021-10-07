from src.support import *

club_list =[]
#club_list.append(Club('PSG.LGD'))
#club_list[len(club_list)-1].creat_player(['萧瑟', 'SoMnus丶M', 'Old Eleven', 'Fy', 'Xnova'],65,90)
#club_list.append(Club('Alliance'))
#club_list[len(club_list)-1].creat_player(['Nikobaby', 'Limmp', 's4', 'Handsken', 'fng'],65,90)
#club_list.append(Club('Evil Geniuses'))
#club_list[len(club_list)-1].creat_player(['Arteezy', 'Abed', 'iceiceice', 'Cr1t-', 'Fly'],65,90)
#club_list.append(Club('Invictus Gaming'))
#club_list[len(club_list)-1].creat_player(['flyfly', 'Emo', 'JT-', 'Kaka', 'Oli'],65,90)

path = os.getcwd()
patch_data = xlrd.open_workbook(path+'/src/patch2021ti10.xls')
patch_table = patch_data.sheets()[0]
row = patch_table.nrows

for i in range(1,row):
    if patch_table.cell_value(i,0) == '队名':
        club_list.append(Club(patch_table.cell_value(i,1)))
        print(patch_table.cell_value(i,1) + " 战队加载中……")
        club_list[len(club_list) - 1].add_player(patch_table.cell_value(i + 1, 1), patch_table.cell_value(i + 1, 2),
                                                 patch_table.cell_value(i + 1, 3))
        club_list[len(club_list) - 1].add_player(patch_table.cell_value(i + 2, 1), patch_table.cell_value(i + 2, 2),
                                                 patch_table.cell_value(i + 2, 3))
        club_list[len(club_list) - 1].add_player(patch_table.cell_value(i + 3, 1), patch_table.cell_value(i + 3, 2),
                                                 patch_table.cell_value(i + 3, 3))
        club_list[len(club_list) - 1].add_player(patch_table.cell_value(i + 4, 1), patch_table.cell_value(i + 4, 2),
                                                 patch_table.cell_value(i + 4, 3))
        club_list[len(club_list) - 1].add_player(patch_table.cell_value(i + 5, 1), patch_table.cell_value(i + 5, 2),
                                                 patch_table.cell_value(i + 5, 3))
