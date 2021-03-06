import random
from tkinter import *
from tkinter import ttk
import time
import copy
import os
import xlrd
#state
class State:
    def __init__(self):
        self.mode = 0
        self.speed = 100
        self.date = [1,1,1]
        self.cs = 0  # 俱乐部界面选中选手编号
        self.yzflag = 0
        self.yznum = 0
        self.report = []
        self.weibo_name = []
        self.weibo_says = []
        self.wsjc = 0

    def refresh_date(self,day =1,month =0):
        self.date[2]+=day
        self.date[1]+=month
        if self.date[2]>30:
            self.date[2]-=30
            self.date[1]+=1
        if self.date[1]>12:
            self.date[1]-=12
            self.date[0]+=1
#选手对象
class Player:
    def __init__(self,name =''):
        #基本属性，
        self.name = name
        self.potential = 0
        self.damage = 0
        self.control = 0
        self.viability = 0
        self.farm = 0
        self.carry = 0
        self.support = 0
        self.state = 0 #S A B C D E
        self.fans = 0
        self.site = 0 #上路 中路 下路 游走 辅助
        self.level = 0
        self.active = 0
        self.age = 16
        self.mvp_times = 0
        self.ladder = 7500
    def level_cal(self):
        self.level = self.damage + self.control + self.viability + self.farm + self.carry + self.support#待定
    def add_point(self, point):
        self[str(point)] += 1
    def random_power(self,min=20,max=80):
        self.age = random.randint(12, 30)
        self.damage = random.randint(min, max)
        self.control = random.randint(min, max)
        self.viability = random.randint(min, max)
        self.farm = random.randint(min, max)
        self.carry = random.randint(min, max)
        self.support = random.randint(min, max)
        self.fans = random.randint(100, 10000)
        #随机状态
        self.state = random.randint(0,6) - 3
    def cal_ladder(self):
        a = self.damage + self.control + self.viability + self.farm + self.carry + self.support
        self.ladder = int(a * 100 / 6)


class Club:
    def __init__(self, name = '基德俱乐部'):
        self.name = name
        self.money = 1000
        self.player = []
    def random_player5(self, biasmin =30, biasmax =60):
        for i in range(5):
            self.player.append(Player(random_name_jd()))
            self.player[i].random_power(biasmin, biasmax)
            self.player[i].site =i+1
    def random_name(self):
        a = ['圣光','无敌','Best','Chaos','Evil','皇家','自由','狂','Dog']
        b = ['独轮车','大爹','Gay','Cat','Home','Wings','龙','俱乐部','宇宙','Gaming','巢穴','野人']
        r = random.randint(0,len(a)-1)
        self.name = a[r]
        r = random.randint(0, len(b) - 1)
        self.name += b[r]

    def add_player(self, name, biasmin =30, biasmax =80):
        self.player.append(Player(name))
        self.player[-1].random_power(biasmin, biasmax)
        self.player[-1].site = len(self.player)

    def creat_player5(self, namelist, biasmin =30, biasmax =80):
        for i in range(5):
            self.player.append(Player(namelist[i]))
            self.player[i].random_power(biasmin, biasmax)
            self.player[i].site =i+1

class Character:
    def __init__(self, player, num):
        self.num = num
        self.hero = ''
        self.nh = ''
        self.money = 600
        self.hpmax = 500
        self.hp = 500
        self.location = ''
        self.location_target =''
        self.speed = 1.2
        self.damage = 40
        self.through = 0
        self.healps = 2
        self.defence = 0 #a/(x+a)为有效伤害公式a=10时有：x=0，受100%伤害；x=10,受50%伤害
        self.controltime = 1.2
        self.controlcd = 0
        self.tpcd = 0#70
        self.name = player.name
        self.site = player.site
        self.d = player.damage + player.state * 3
        self.c = player.control + player.state * 3
        self.v = player.viability + player.state * 3
        self.f = player.farm + player.state * 3
        self.carry = player.carry + player.state * 3
        self.support = player.support + player.state * 3
        self.busy = 0
        self.tmb_flag = 4 # 0，1，2top mid bot
        self.dead_flag = 0
        self.kda = [0,0,0]
        self.dtc = 0#对人累计伤害
        self.dtt = 0#对塔累计伤害
        self.dtd = 0#累计吸收伤害
        self.ctc = 0#累计控制时间
        self.point = 0
    def cal(self):
        self.damage= 40 + self.money * 0.015 * self.d * 0.01
        self.healps= 3 + self.money * 0.0005 * self.v * 0.01
        self.hpmax = 500 + self.money * 0.12 * self.v * 0.01
        self.defence = 5 + self.money *0.0012 * self.v * 0.01
        self.through = self.money *0.0004 * self.d * 0.01
        self.speed = 1.4 - self.money*0.00002 * self.d *0.01
        self.controltime = 2.2 + self.money * 0.0001 * self.c * 0.01
        self.controlcd = 20 - self.money * 0.0003 * self.c * 0.01


class Tower:
    def __init__(self,num):
        self.hpmax = num * 2000 + 1500
        self.hp = num * 2000 + 1500
        self.damage = 30 * num + 90
        self.defence = 9 + 3 * num

class Game:
    def __init__(self):
        self.tower = [[],[]]#wofang
        self.player = []
        self.ch = []#角色
        self.ps = [[],[],[],[],[],[]] #角色分路容器
        self.sc = 0 #选择的角色,查看属性用的
        self.tmb_avi =[[0,1,2],[0,1,2]]
        self.spring = [[],[]]#泉水玩家坑
        self.gt = [0,0,0]#游戏时间 分钟 秒钟0.1秒
        self.resource = [[300,300,300],[300,300,300],[300,300,300]]#9个元素三路资源
        self.pressure = [[0,0,0],[0,0,0]]
        self.result = 0
        self.gospeed = 100
        self.side = 0 #选边情况0为蓝色
    def cal_mvp(self):#mvp是个号码
        point_kda = []
        point_dtc = []
        point_dtt = []
        point_dtd = []
        point_ctc = []
        point_sum = []
        for i in range(5):
            a = self.ch[5*self.result+i]
            point_kda.append(((a.kda[0]+a.kda[2])/(a.kda[1]+1),a.num))
            point_dtc.append((a.dtc,a.num))
            point_dtt.append((a.dtt,a.num))
            point_dtd.append((a.dtd,a.num))
            point_ctc.append((a.ctc,a.num))
        point_kda.sort()#低到高排序
        point_dtc.sort()
        point_dtt.sort()
        point_dtd.sort()
        point_ctc.sort()
        for i in range(5):
            self.player[5 * self.result + i].potential+=2
            a = self.ch[5 * self.result + i]
            a.point = point_kda.index(((a.kda[0]+a.kda[2])/(a.kda[1]+1),a.num))\
                      + point_dtc.index((a.dtc,a.num))\
                      + point_dtt.index((a.dtt,a.num))\
                      + point_dtd.index((a.dtd,a.num))\
                      + point_ctc.index((a.ctc,a.num))
            point_sum.append((a.point,a.num))
        point_sum.sort()
        mvp = point_sum[4][1]
        self.player[mvp].potential+=2
        for i in range(5):#天梯分
            self.player[5 * self.result + i].ladder += 30
            self.player[5 * (1 - self.result) + i].ladder -= 30
        return mvp
    def tower_creat(self):
        for i in range(3):
            self.tower[0].append([])
            for j in range(3):
                self.tower[0][i].append(Tower(j))
        for i in range(3):
            self.tower[1].append([])
            for j in range(3):
                self.tower[1][i].append(Tower(j))
    def resource_fresh(self):
        self.resource = [[300, 300, 300], [300, 300, 300], [300, 300, 300]]

class Market:
    def __init__(self):
        self.player = []

    def creat(self):
        for i in range(random.randint(7,15)):
            self.player.append(Player(random_name()))
            self.player[i].random_power()
#随机中文名
def random_name():
    name =''
    i = random.randint(1,2)
    last_names = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯',
                  '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
                  '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明',
                  '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
                  '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
    mid_names = ['的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
               '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
               '乾', '坤', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    first_names = ['的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
               '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
               '乾', '坤']
    r = random.randint(0,len(last_names)-1)
    name += last_names[r]
    r = random.randint(0,len(mid_names)-1)
    name += mid_names[r]
    r = random.randint(0,len(first_names)-1)
    name += first_names[r]
    return name

dj_name = []
path = os.getcwd()
dj_data = xlrd.open_workbook(path+'/src/name_jd.xls')
dj_table = dj_data.sheets()[0]
row = dj_table.nrows
for i in range(row):
    dj_name.append(dj_table.cell_value(i, 0))

def random_name_jd():
    name = random.choice(dj_name)
    return name

class Hpbar:
    def __init__(self,master,height =18,width =100,hpmax =100,hp =100, bg='pink',fg ='green'):
        self.master = master
        self.height = height
        self.width = width
        self.hpmax = hpmax
        self.hp = hp
        self.bg = bg
        self.fg = fg
        self.canvas = Canvas(master, width=self.width, height = self.height, bg=self.bg)
        length = self.width*hp/hpmax
        self.line = self.canvas.create_rectangle(0,0,length+1,self.height+1, fill=self.fg)
        self.lt = self.canvas.create_text(self.width/2,self.height/2,text = str(int(self.hp))+'/'+str(int(self.hpmax)))
    def change(self):
        self.canvas['width']=self.width
        self.canvas['height'] = self.height
        length = self.width * self.hp / self.hpmax
        self.canvas.coords(self.line,(0,0,length+1,self.height+1))
    def grid(self,row =0,column = 0,rowspan =1,columnspan =1):
        self.canvas.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
    def grid_forget(self):
        self.canvas.grid_forget()
    def refresh(self,hp,hpmax):
        self.hp =hp
        self.hpmax =hpmax
        length = self.width*hp/hpmax
        self.canvas.coords(self.line,(0,0,length+1,self.height+1))
        self.canvas.delete(self.lt)
        self.lt = self.canvas.create_text(self.width/2,self.height/2,text = str(int(self.hp))+'/'+str(int(self.hpmax)))

def cal_state(state):
    if state < -3:
        state = -3
    elif state > 3:
        state = 3
    a = ['摆烂','糟糕透顶','糟糕','一般','神勇','陈独秀','1V9'][state+3]
    return a

