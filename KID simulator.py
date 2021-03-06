from src.support import *
import tkinter.messagebox
import pickle

# <editor-fold desc="开头">
win =Tk()
win.geometry('800x600+0+0')
win.title('基德俱乐部模拟器')
myclub = Club()#初始化俱乐部
jcclub = Club()
state = State()
#加载补丁包
from src.patch2021ti10 import *

market = Market()
market.creat()
canvas = Canvas(win)
xbar = Scrollbar(win,orient=HORIZONTAL)
xbar.pack(side ='bottom',fill='x')
xbar.configure(command=canvas.xview)
canvas.configure(xscrollcommand=xbar.set)
ybar = Scrollbar(win,orient=VERTICAL)
ybar.pack(side ='right',fill='y')
ybar.configure(command=canvas.yview)
canvas.configure(yscrollcommand=ybar.set)

canvas.pack()
def mobile(event):#为了适配手机加的滚动条
    canvas.configure(scrollregion=canvas.bbox('all'))
    canvas['width']=win.winfo_width()
    canvas['height'] = win.winfo_height()
#初始化各个界面
frame = []
frame_root =Frame(canvas)
win.bind("<Configure>",mobile)
frame_mkt =Frame(canvas)
frame_player =Frame(canvas)
frame_game =Frame(canvas)
frame_weibo =Frame(canvas)
frame_j =Frame(canvas)
canvas.create_window((0,0), window=frame_root,anchor=NW)
frame = [frame_root, frame_mkt, frame_player, frame_game, frame_weibo, frame_j]
#初始化杰出
jc = Player('杰出哥')
jc.random_power(min = 25, max = 45)
jc.site = 1
jc.cal_ladder()
#日期
def refresh_date():
    var_date.set(str(state.date[0])+'年'+str(state.date[1])+'月'+str(state.date[2])+'日')
var_date = StringVar()
lr_date = Label(frame_root, textvariable = var_date).grid(row = 1, column = 0)
var_date.set(str(state.date[0])+'年'+str(state.date[1])+'月'+str(state.date[2])+'日')
#俱乐部名称
var_clubname = StringVar()
var_clubname.set(myclub.name)
lr_clubname = Label(frame_root, textvariable = var_clubname).grid(row = 3, column = 0)

#俱乐部切换
def clubchange(myclub):
    if var_clubchange.get() == '切换俱乐部':
        var_clubchange.set('确认')
        lbr1.grid(row=3, column=2)
        lbr1.delete(0, END)
        for i in range(len(club_list)):
                lbr1.insert('end', club_list[i].name)
    else:
        var_clubchange.set('切换俱乐部')
        if lbr1.curselection() != ():
            value = lbr1.get(lbr1.curselection())
            for i in range(len(club_list)):
                if club_list[i].name == value:
                    state.cs = i
            club_list.append(Club(myclub.name))
            club_list[-1].player = myclub.player[:]
            myclub.name = club_list[state.cs].name
            myclub.player = club_list[state.cs].player[:]
            var_clubname.set(myclub.name)
            club_list.pop(state.cs)
            lbr1.delete(0, END)
            lbr1.grid_forget()
var_clubchange = StringVar()
var_clubchange.set('切换俱乐部')
br_clubchange = Button(frame_root, textvariable = var_clubchange, command = lambda: clubchange(myclub)).grid(row = 3, column = 1)
lbr1 = Listbox(frame_root)
#俱乐部约战
var_yzclubname = StringVar()
var_yzclubname.set('无')
lr_yzclubname = Label(frame_root, textvariable = var_yzclubname).grid(row = 4, column = 0)
def preclub():
    if var_preclub.get() == '约战俱乐部':
        var_preclub.set('确认')
        lbr2.grid(row=4, column=2)
        lbr2.delete(0, END)
        for i in range(len(club_list)):
                lbr2.insert('end', club_list[i].name)
    else:
        var_preclub.set('约战俱乐部')
        if lbr2.curselection() != ():
            value = lbr2.get(lbr2.curselection())
            for i in range(len(club_list)):
                if club_list[i].name == value:
                    state.yzflag = 1
                    state.yznum = i
            lbr2.delete(0, END)
            lbr2.grid_forget()
            var_yzclubname.set(value)
var_preclub = StringVar()
var_preclub.set('约战俱乐部')
br_preclub = Button(frame_root, textvariable = var_preclub, command = preclub).grid(row = 4, column = 1)
lbr2 = Listbox(frame_root)
#资金
lr1 = Label(frame_root, text = "资金：").grid(row = 2, column = 0)
lr2 = Label(frame_root, textvariable = myclub.money).grid(row = 2, column = 1)
# </editor-fold>

#页面刷新for市场名单
def refresh_win(f):
    if f == frame_mkt:
        lbm.delete(0, END)
        for i in range(len(market.player)):
            lbm.insert('end', market.player[i].name)
    elif f == frame_player:
        lbc1.delete(0, END)
        for i in range(len(myclub.player)):
            if myclub.player[i].site != 0:
                lbc1.insert('end', myclub.player[i].name + '（ '+ str(myclub.player[i].site)+'号位）')
            else:
                lbc1.insert('end', myclub.player[i].name)
    elif f == frame_root:
        refresh_date()
    elif f == frame_weibo:
        refresh_weibo()
    elif f == frame_j:
        for i in range(12):  # 杰出属性显示
            varj1[i].set(
                [jc.name, jc.ladder, jc.damage, jc.control, jc.viability, jc.farm, jc.carry, jc.support, jc.fans, jc.potential,
                 cal_state(jc.state), jc.site][i])

#页面转换
def change_win(f):
    refresh_win(f)
    canvas.delete('all')
    canvas.create_window((0,0), window=f,anchor=NW)

def report_check():
    for i in range(len(state.report)):
        print(state.report[i])

def next_day():
    state.date[2] += 1
    if state.date[2] == 31:
        state.date[2] = 0
        state.data[1] += 1
    if state.date[1] == 13:
        state.date[1] = 1
        state.date[0] += 1
    refresh_date()
    
br1 = Button(frame_root, text ='交易市场', command = lambda :change_win(frame_mkt))#市场按钮
br1.grid(row = 0, column = 1)

br2 = Button(frame_root, text = "选手管理", command = lambda :change_win(frame_player))#俱乐部按钮
br2.grid(row = 0, column = 0)

br3 = Button(frame_root, text = '比赛', command = lambda :change_win(frame_game))#模拟比赛按钮
br3.grid(row = 0, column = 2)

br4 = Button(frame_root, text = '查看上局战报', command = report_check)#模拟比赛按钮
br4.grid(row = 0, column = 3)

br5 = Button(frame_root, text = '微博', command = lambda :change_win(frame_weibo))#微博
br5.grid(row = 0, column = 4)

br6 = Button(frame_root, text = '下个比赛日', command = next_day)#微博
br6.grid(row = 1, column = 1)

def change_win_j(f):
    if f == frame_j:
        state.wsjc =1
    else:
        state.wsjc =0
    change_win(f)

br7 = Button(frame_root, text = '启动杰出模拟器', command = lambda :change_win_j(frame_j))#我是杰出
br7.grid(row = 0, column = 5)

#我是阿杰界面
bj1 = Button(frame_j, text = '返回', command = lambda :change_win_j(frame_root))
bj1.grid(row =0, column = 0)

lj1 = []
for i in range(12):
    lj1.append(Label(frame_j,text =['姓名：','天梯积分','伤害能力：','控制能力：',
                                       '生存能力：','发育能力：','核心能力：','辅助能力：',
                                       '粉丝数目：','属性点：','状态：','位置：'][i]).grid(row=3+i,column =0))
varj1 = []
ej1 = []
for i in range(12):
    varj1.append(IntVar())
varj1[9] = IntVar()
for i in range(12):#选手属性显示
    varj1[i].set([jc.name,jc.ladder,jc.damage,jc.control,jc.viability,jc.farm,jc.carry,jc.support,jc.fans,jc.potential,cal_state(jc.state),jc.site][i])

#杰出属性加点
bj_add = []
def bj_add_init():
    def bj_add1():
        if varj1[9].get() >0:
            varj1[2].set(varj1[2].get()+1)
            varj1[9].set(varj1[9].get()-1)
            jc.damage += 1
            jc.potential -= 1
    def bj_add2():
        if varj1[9].get() >0:
            varj1[3].set(varj1[3].get()+1)
            varj1[9].set(varj1[9].get()-1)
            jc.control += 1
            jc.potential -= 1
    def bj_add3():
        if varj1[9].get() >0:
            varj1[4].set(varj1[4].get()+1)
            varj1[9].set(varj1[9].get()-1)
            jc.viability += 1
            jc.potential -= 1
    def bj_add4():
        if varj1[9].get() >0:
            varj1[5].set(varj1[5].get()+1)
            varj1[9].set(varj1[9].get()-1)
            jc.farm += 1
            jc.potential -= 1
    def bj_add5():
        if varj1[9].get() > 0:
            varj1[6].set(varj1[6].get()+1)
            varj1[9].set(varj1[9].get()-1)
            jc.carry += 1
            jc.potential -= 1
    def bj_add6():
        if varj1[9].get() >0:
            varj1[7].set(varj1[7].get()+1)
            varj1[9].set(varj1[9].get()-1)
            jc.support += 1
            jc.potential -= 1
    bj_add.append(Button(frame_j, text="+", command=bj_add1))
    bj_add.append(Button(frame_j, text="+", command=bj_add2))
    bj_add.append(Button(frame_j, text="+", command=bj_add3))
    bj_add.append(Button(frame_j, text="+", command=bj_add4))
    bj_add.append(Button(frame_j, text="+", command=bj_add5))
    bj_add.append(Button(frame_j, text="+", command=bj_add6))
    for i in range(6):
        bj_add[i].grid(row= 5+i, column=2)
bj_add_init()
for i in range(12):
    varj1.append(IntVar())
    ej1.append(Entry(frame_j, textvariable = varj1[i], state = 'disabled'))
    ej1[i].grid(row =i+3, column =1)
varj1.pop(12)#忘了为什么了
#杰出位置选择

#天梯单排
bj2 = Button(frame_j, text = '比赛', command = lambda :change_win(frame_game))#模拟比赛按钮
bj2.grid(row = 0, column = 1)

#选手市场部分
lm1 = Label(frame_mkt, text = '自由市场选手').grid(row = 1, column =0, columnspan =2)
lbm = Listbox(frame_mkt)
lbm.grid(row = 2, columnspan = 2)
for i in range(len(market.player)):
    lbm.insert('end',market.player[i].name)
def checkm(event = None):
    if lbm.curselection() != ():
        value = lbm.get(lbm.curselection())
        for ii in range(len(market.player)):
            if market.player[ii].name == value:
                i =ii
        a = market.player[i]
        for j in range(9):
            varm1[j].set([a.name,a.age,a.damage,a.control,a.viability,a.farm,a.carry,a.support,a.fans][j])
lbm.bind('<ButtonRelease-1>', checkm)#事件触发
lbm.bind('<KeyRelease-Up>', checkm)
lbm.bind('<KeyRelease-Down>', checkm)

# <editor-fold desc="市场界面">
bm1 = Button(frame_mkt, text = '返回', command = lambda :change_win(frame_root))
bm1.grid(row =0, column =0)
lm2 = []
varm1 = []
em1 = []
for i in range(9):
    lm2.append(Label(frame_mkt,text=['姓名：','年龄：','伤害能力：',
                                     '控制能力：','生存能力：','发育能力：','核心能力：',
                                     '辅助能力：','粉丝数目：'][i]).grid(row =3+i,column =0))
    varm1.append(StringVar())
    varm1[i].set('')
    em1.append(Entry(frame_mkt, textvariable = varm1[i], state = 'disabled').grid(row =i+3, column =1))
def buy_player():
    if lbm.curselection() != ():
        value = lbm.get(lbm.curselection())
        for i in range(len(market.player)):
            if market.player[i].name == value:
                the_one = i#pop会导致m.p人数减少
        lbm.delete(the_one)
        myclub.player.append(market.player.pop(the_one))

bm2 = Button(frame_mkt, text = '购买选手', command = buy_player)
bm2.grid(row = 0, column = 1)
# </editor-fold>

#微博界面
bw1 = Button(frame_weibo, text = '返回', command = lambda :change_win(frame_root))
bw1.grid(row =0, column = 0)

mw1 = []
mw2 = []
def weibo_creat():
    if game.result == 0:#蓝色方获胜
        winner = var_blue.get()
        loser = var_red.get()
    else:
        winner = var_red.get()
        loser = var_blue.get()
    name = ['@ROTK：', '@Fade乌龙院：', '@LGD电子俱乐部：', '@Esport海涛：', '@斗鱼杰出哥：', '@Iceforg：', '@G胖：', '@Inflame：',
            '@BurNing：', '@AMS：', '@IG_Ana：', '@Faker：','@小辣椒：','@Snow不会打工夫：','@单车：','@DC','@Esports海涛：','@吃花椒的喵酱：',
            '@绵绵：','@IG 430：','@BBC：','@解说AA：','@郑翔：','@Inflame：']
    says = [loser + '下次干回来啊！', '这把' + winner + '发挥得太好了', loser + '这局打的是个什么东西？！', loser + '简直是被' + winner + '摁在地上摩擦……',
            '今年ti就看' + winner + '的了！', loser + '不如解散了吧?', winner + '硬实力冠军啊！恭喜' + winner, loser+'！！！' + '经典刷了送，看哭了！',
            loser + '这局被b爆了啊', f'我就直说了，这波{loser}不是假赛，我倒立拉屎！',f'涛哥震怒，{loser}假赛',
            f'内部消息：{loser}1、{random.choice(["2","3","4","5"])}不和，消息来源{random.choice(["人杰地灵工作室","SG","NGA","贴吧","MAX+"])}']
    for i in range(7):
        state.weibo_name.append(name[random.randint(0, len(name) - 1)])
        state.weibo_says.append(says[random.randint(0, len(says) - 1)])
def refresh_weibo():
    for i in range(len(mw1)):
        mw1[-1].grid_remove()
        mw2[-1].grid_remove()
    l = len(state.weibo_name)
    for i in range(l):
        mw1.append(Message(frame_weibo,text = state.weibo_name[-i], fg ='blue', width = 120, justify ='right', anchor ='e').grid(row = 2*i+1, column = 1))
        mw2.append(Message(frame_weibo,text = state.weibo_says[-i], width = 800, justify = 'left', anchor ='w').grid(row = 2*i+1, column = 2, rowspan = 2))
#选手管理部分

bc1 = Button(frame_player, text = '返回', command = lambda :change_win(frame_root))
bc1.grid(row =0, column = 0)
lc1 = Label(frame_player, text = '选手列表').grid(row =1, column = 0, columnspan = 2)
lbc1 = Listbox(frame_player)
lbc1.grid(row = 2, columnspan = 2)
def checkc(event = None):
    if lbc1.curselection() != ():
        value = lbc1.get(lbc1.curselection())
        for i in range(len(myclub.player)):
            if myclub.player[i].name in value:
                state.cs = i
        a = myclub.player[state.cs]
        for j in range(12):#选手属性显示
            varc1[j].set([a.name,a.age,a.damage,a.control,a.viability,a.farm,a.carry,a.support,a.fans,a.potential,cal_state(a.state),a.site][j])
        bc2.grid(row=3, column=2)
        bc3.grid(row=14, column=2)
#俱乐部界面生成
lc2 = []
for i in range(12):
    lc2.append(Label(frame_player,text =['姓名：','年龄','伤害能力：','控制能力：',
                                       '生存能力：','发育能力：','核心能力：','辅助能力：',
                                       '粉丝数目：','属性点：','状态：','位置：'][i]).grid(row=3+i,column =0))
#属性加点
bc_add = []
def bc_add_init():
    def bc_add1():
        if varc1[9].get() >0:
            varc1[2].set(varc1[2].get()+1)
            varc1[9].set(varc1[9].get()-1)
            myclub.player[state.cs].damage += 1
            myclub.player[state.cs].potential -= 1
    def bc_add2():
        if varc1[9].get() >0:
            varc1[3].set(varc1[3].get()+1)
            varc1[9].set(varc1[9].get()-1)
            myclub.player[state.cs].control += 1
            myclub.player[state.cs].potential -= 1
    def bc_add3():
        if varc1[9].get() >0:
            varc1[4].set(varc1[4].get()+1)
            varc1[9].set(varc1[9].get()-1)
            myclub.player[state.cs].viability += 1
            myclub.player[state.cs].potential -= 1
    def bc_add4():
        if varc1[9].get() >0:
            varc1[5].set(varc1[5].get()+1)
            varc1[9].set(varc1[9].get()-1)
            myclub.player[state.cs].farm += 1
            myclub.player[state.cs].potential -= 1
    def bc_add5():
        if varc1[9].get() > 0:
            varc1[6].set(varc1[6].get()+1)
            varc1[9].set(varc1[9].get()-1)
            myclub.player[state.cs].carry += 1
            myclub.player[state.cs].potential -= 1
    def bc_add6():
        if varc1[9].get() >0:
            varc1[7].set(varc1[7].get()+1)
            varc1[9].set(varc1[9].get()-1)
            myclub.player[state.cs].support += 1
            myclub.player[state.cs].potential -= 1
    bc_add.append(Button(frame_player, text="+", command=bc_add1))
    bc_add.append(Button(frame_player, text="+", command=bc_add2))
    bc_add.append(Button(frame_player, text="+", command=bc_add3))
    bc_add.append(Button(frame_player, text="+", command=bc_add4))
    bc_add.append(Button(frame_player, text="+", command=bc_add5))
    bc_add.append(Button(frame_player, text="+", command=bc_add6))
    for i in range(6):
        bc_add[i].grid(row= 5+i, column=2)
bc_add_init()
varc1 = []
ec1 = []
for i in range(12):
    varc1.append(IntVar())
    ec1.append(Entry(frame_player, textvariable = varc1[i], state = 'disabled'))
    ec1[i].grid(row =i+3, column =1)
#varc1.pop(12)#忘了为什么了
#选手位置选择
varc3 = IntVar()
varc3.set(1)
rb_site=[]
for i in range(5):
    rb_site.append(Radiobutton(frame_player,
                               text = ['1号位','2号位','3号位','4号位','5号位'][i],
                               variable = varc3, value = i+1))
varc4 = StringVar()
varc4.set('改位置')
def change_site():
    if lbc1.curselection() != ():
        if varc4.get() == '改位置':
            for i in range(5):
                rb_site[i].grid(row=14, column=3+i)
            value = lbc1.get(lbc1.curselection())
            for i in range(len(myclub.player)):
                if myclub.player[i].name in value:
                    state.cs = i
            varc4.set('确定')
            lbc1['state'] = 'disabled'
        else:
            for i in range(len(myclub.player)):
                if myclub.player[i].site == varc3.get():
                    myclub.player[i].site = 0
                    myclub.player[i].active = 0
            myclub.player[state.cs].active = 1
            myclub.player[state.cs].site = varc3.get()
            lbc1['state'] = 'normal'
            varc4.set('改位置')
            for i in range(5):
                rb_site[i].grid_forget()
            refresh_win(frame_player)

bc3 = Button(frame_player, textvariable = varc4, command = change_site)#改名按钮

#改名字
varc2 = StringVar()
varc2.set('修改姓名')
def change_name():
    if varc2.get() == '修改姓名':
        if lbc1.curselection() != ():
            value = lbc1.get(lbc1.curselection())
            for i in range(len(myclub.player)):
                if myclub.player[i].name in value:
                    state.cs = i
            lbc1['state'] = 'disabled'
            ec1[0]['state'] = 'normal'
            varc2.set('确定修改')
    else:
        myclub.player[state.cs].name = varc1[0].get()
        lbc1['state'] = 'normal'
        ec1[0]['state'] = 'disabled'
        varc2.set('修改姓名')
        refresh_win(frame_player)

bc2 = Button(frame_player, textvariable = varc2, command = change_name)#改名按钮
#开除选手
# varc3 = StringVar()
# varc3.set('开除选手')
def fire():
    if lbc1.curselection() != ():
        value = lbc1.get(lbc1.curselection())
        for i in range(len(myclub.player)):
            if myclub.player[i].name in value:
                if tkinter.messagebox.askyesno('提示', '要执行此操作吗'):
                    myclub.player.pop(i)
                    refresh_win(frame_player)

bc4 = Button(frame_player, text = '开除选手', command = fire)#开除按钮
bc4.grid()
#俱乐部事件
lbc1.bind('<ButtonRelease-1>', checkc)
lbc1.bind('<KeyRelease-Up>', checkc)
lbc1.bind('<KeyRelease-Down>', checkc)

def change_win_g():
    if state.wsjc == 1:
        change_win(frame_j)
    else:
        change_win(frame_root)

#比赛界面
frame_game_state = Frame(frame_game)
frame_game_state.grid(row =1, column =9, rowspan =11, columnspan =5)
frame_game_msg = LabelFrame(frame_game, bg ='white')
frame_game_msg.grid(row =13, column =9, rowspan =11, columnspan =5)
bg1 = Button(frame_game, text = '返回', command = lambda :change_win_g())
bg1.grid(row =0,column =0)
varg1 = StringVar()
varg1.set('准备')
#关键部分准备游戏
def reportcreat(text):
    state.report.append('[' + str(game.gt[0]) + '分' + str(game.gt[1]) + '.' + str(game.gt[2]) + '秒] '+ text)
def printf(text):
    for i in range(9):
        var_msg[9-i].set(var_msg[8-i].get())
    var_msg[0].set('~~'+text+'~~')
def recoverbb():#修复加速导致的错位
    for i in range(10):
        bgc[i].grid_forget()
        hpb[i].grid_forget()
    for i in range(10):
        # a = game.ch[i].dead_flag
        j = game.ch[i].tmb_flag
        if game.ch[i].dead_flag ==0:
            if i <5:
                bgc[i].grid(row=11 - game.ps[j].index(i) * 2, column=3 + 2 * j)
                hpb[i].grid(row=10 - game.ps[j].index(i) * 2, column=3 + 2 * j)
            else:
                bgc[i].grid(row=15 + game.ps[j+3].index(i) * 2, column=3 + 2 * j)
                hpb[i].grid(row=14 + game.ps[j+3].index(i) * 2, column=3 + 2 * j)
        else:
            if i <5:
                bgc[i].grid(row=11 - game.spring[0].index(i) * 2, column=8)
                hpb[i].grid(row=10 - game.spring[0].index(i) * 2, column=8)
            else:
                bgc[i].grid(row=15 + game.spring[1].index(i) * 2, column=8)
                hpb[i].grid(row=14 + game.spring[1].index(i) * 2, column=8)
def refreshbb():#界面刷新
    for i in range(10):
        hpb[i].refresh(game.ch[i].hp,game.ch[i].hpmax)
    varg3.set('游戏时间：' + str(game.gt[0]) + '分钟' + str(game.gt[1]) + '.' + str(game.gt[2]) + '秒')
    ch=game.ch[game.sc]
    var_state[0].set(ch.name)
    var_state[1].set(str(ch.kda[0])+'/'+str(ch.kda[1])+'/'+str(ch.kda[2]))#kda
    var_state[2].set(ch.money)
    var_state[3].set(int(ch.damage))
    var_state[4].set(int(ch.through))
    var_state[5].set(int(ch.defence))
    var_state[6].set(int(ch.healps))
def judgement(ch):
    ch.hp += ch.healps * 0.1
    if ch.hp > ch.hpmax:
        ch.hp = ch.hpmax
    ch.busy -= 0.1
    if ch.controlcd > 0:
        ch.controlcd -= 0.1
    if ch.tpcd != 0:
        ch.tpcd -= 0.1
    if ch.busy <= 0 and ch.dead_flag == 0:
        if swim(ch) == 0:
            b = ch.d + ch.c + ch.v + ch.f
            r = random.randint(1, b)
            if r >= 1 and r < ch.d:
                damage_behave(ch)
            elif r >= ch.d and r < ch.d + ch.c:
                control_behave(ch)
            elif r >= ch.d + ch.c and r < ch.d + ch.c + ch.v:
                viability_behave(ch)
            elif r >= ch.d + ch.c + ch.v and r <= b:
                farm_behave(ch)
    elif ch.busy <= 0 and ch.dead_flag == 1:
        back(ch)
def refreshgame_time(n=100):
    if varg1.get() == '暂停游戏':
        game_time_refresh()
        for i in range(10):
            judgement(game.ch[i])
        refreshbb()
        win.after(n, lambda :refreshgame_time(state.speed))
def refreshgame():#后台的，用来push
    game_time_refresh()
    for i in range(10):
        judgement(game.ch[i])
def play():
    if varg1.get() == '准备':
        checkgame()
        #清理信息框
        for i in range(10):
            printf('~~~')
    elif varg1.get() == '游戏初始化':
        varg1.set('进行游戏')
        game_init()
    elif varg1.get() == '进行游戏':
        varg1.set('暂停游戏')
        refreshgame_time(state.speed)
    elif varg1.get() == '暂停游戏':
        varg1.set('进行游戏')
    elif varg1.get() =='开始结算':
        cal_game()
        varg1.set('准备')
        bg2['state']=='disabled'
def end_game():
    varg1.set('准备')
    bg2['state'] = 'normal'
    bg3['state'] = 'disabled'
    bg4['state'] = 'disabled'
    for i in range(10):
        bgc[i].grid_forget()
        hpb[i].grid_forget()
        msg_game[i].grid_forget()
        var_msg[i].set('~~~~~~~~~~')
    for i in range(3):
        thpb[i].grid_forget()
        b_midline[i].grid_forget()
    b_midline[3].grid_forget()
    for i in range(7):
        e_state[i].grid_forget()
        l_state[i].grid_forget()
    lg_blue.grid_forget()
    lg_red.grid_forget()
    var_red.set('')
    state.refresh_date(3)
    market.creat()
    #清理杰出
    for i in range(len(jcclub.player)):
        jcclub.player.pop(0)
def rivalcheck():
    global rival
    if state.wsjc == 0:
        if state.yzflag == 1:
            rival = club_list[state.yznum]
        else:
            # 天梯随机对手
            r = random.randint(0,len(club_list)+3)
            if r >= len(club_list):
                rival = Club()
                rival.random_player5()
                rival.random_name()
            else:
                rival = club_list[r]
    else:
        rival = Club()
        max = int(jc.ladder / 100) + 5
        rival.random_player5(max - 20, max)
    state.yzflag = 0
    var_yzclubname.set('无')
def checkgame():
    print('目前杰出的天梯分：' + str(jc.ladder))
    global game
    game = Game()
    rivalcheck()
    a = []
    if state.wsjc == 1:
        # 天梯队友
        max = int(jc.ladder / 100) + 5
        jcclub.player = []
        jcclub.random_player5(max - 20, max)
        jcclub.player.pop(0)
        jcclub.player.append(jc)
        if state.wsjc == 1:
            var_blue.set("天辉")
            var_red.set("夜魇")
            state.report.append('比赛开始，对阵双方分别是蓝色方的【天辉】和红色方【夜魇】')
        r = random.randint(0, 1)
        if r == 0:  # 蓝色方
            for i in range(5):
                game.player.append(jcclub.player[i])
            for i in range(5):
                game.player.append(rival.player[i])
        else:
            for i in range(5):
                game.player.append(rival.player[i])
            for i in range(5):
                game.player.append(jcclub.player[i])
        for i in range(10):
            game.ch.append(Character(game.player[i], i))
        varg1.set('游戏初始化')
    else:
        for i in range(len(myclub.player)):  # 判定是否能开始
            a.append((myclub.player[i].site,myclub.player[i]))
        a.sort(reverse=1)
        if len(a)>=5:
            if a[4][0] ==1:#从大到小排列第五个选手位置是1号位
                r = random.randint(0,1)
                if r ==0:#蓝色方
                    for i in range(5):
                        game.player.append(a[4-i][1])
                    for i in range(5):
                        game.player.append(rival.player[i])
                    var_blue.set(myclub.name)
                    var_red.set(rival.name)
                    state.report.append('比赛开始，对阵双方分别是蓝色方的【' + myclub.name + '】和红色方【' + rival.name + '】')
                else:
                    for i in range(5):
                        game.player.append(rival.player[i])
                    for i in range(5):
                        game.player.append(a[4-i][1])
                    var_red.set(myclub.name)
                    var_blue.set(rival.name)
                    state.report.append('比赛开始，对阵双方分别是蓝色方的【' + rival.name + '】和红色方【' + myclub.name + '】')
                for i in range(10):
                    game.ch.append(Character(game.player[i],i))
                varg1.set('游戏初始化')
            else:
                tkinter.messagebox.showinfo('提示', '选手未分配位置！')
        else:
            tkinter.messagebox.showinfo('提示', '选手人数不足！')
def game_init():#功能是把角色对应的按钮放在相应的位置
    #清理上局的战报
    state.report.clear()
    bg4['state'] = 'normal'
    bg3['state'] = 'normal'
    #角色属性初始化
    for i in range(10):
        game.ch[i].cal()
        bgc[i]['bg']='white'
    #塔初始化
    game.tower_creat()
    #分路按钮和血条初始化放置
    hero_list =["齐天大圣","神谕者","大地之灵","恐怖利刃","孽主","地狱领主",
         "天穹守望者","军团指挥官","凤凰","上古巨神","寒冬飞龙","炸弹人",
         "灰烬之灵","钢背兽","天怒法师","巨牙海民","巨魔战将","蛇发女妖","地精撕裂者","双头龙",
         "魅惑魔女","先知","死灵飞龙","地精修补匠","暗影恶魔","暗影萨满","食人魔魔法师","沉默术士",
         "祈求者","圣骑士","光之守卫","干扰者","大魔导师","黑暗贤者","殁境神蚀者","受折磨的灵魂","蝙蝠骑士",
         "极寒幽魂","暗影牧师","秀逗魔导士","宙斯","风行者","赏金猎人","复仇之魂","熊战士","圣堂刺客","卓尔游侠",
         "矮人直升机","风暴之灵","隐形刺客","月之公主","仙女龙","幻影长矛手","娜迦海妖","变体精灵","遗忘法师",
         "月之骑士","水晶室女","死亡先知","痛苦女王","德鲁伊","术士","主宰","瘟疫法师","谜团","巫医","虚空假面",
         "鱼人夜行者","冥界亚龙","剃刀","地卜师","剧毒术士","幽鬼","影魔","幻影刺客","编织者","半人猛犸","司夜刺客","不朽尸王",
         "育母蜘蛛","混沌骑士","骷髅弓箭手","血魔","狼人","裂魂人","末日使者","狙击手","恶魔巫师","暗夜魔王","噬魂鬼","半人马战行者",
         "精灵守卫","树精卫士","酒仙","炼金术士","神灵武士","全能骑士","发条技师","龙骑士","巫妖","兽王",
         "海军上将","骷髅王","潮汐猎人","鱼人守卫","山岭巨人","流浪剑客","撼地者","沙王","屠夫","敌法师","斧王","祸乱之源"]
    state.report.append('经过一系列紧张的Ban/Pick，双方选人如下：')
    for i in range(10):
        r = random.randint(0,len(hero_list)-1)
        game.ch[i].hero = hero_list.pop(r)
        game.ch[i].nh = game.ch[i].name + '【' + game.ch[i].hero + '】'
        bgc[i]['text'] = game.ch[i].name + '（' + game.ch[i].hero + '）'
        hpb[i].hpmax=game.ch[i].hpmax
        hpb[i].hp = game.ch[i].hp
        if i == 0:
            state.report.append('蓝色方【'+ var_blue.get() + '】')
        elif i == 5:
            state.report.append('红色方【' + var_red.get() + '】')
        state.report.append(str(game.ch[i].site) + '号位' + game.ch[i].name + '操刀【' + game.ch[i].hero + '】')
    #修正血条后续加上###############################
    for i in [0,5]:
        r =random.randint(0,1)
        if r ==0:
            game.ch[i].tmb_flag = 2
            game.ch[i + 4].tmb_flag = 2
            game.ch[i + 2].tmb_flag = 0
        elif r==1:
            game.ch[i].tmb_flag = 0
            game.ch[i + 4].tmb_flag = 0
            game.ch[i + 2].tmb_flag = 2
        game.ch[i + 1].tmb_flag = 1
        game.ch[i + 3].tmb_flag = random.randint(0,2)
    for i in range(10):
        j =game.ch[i].tmb_flag
        if i <5:
            game.ps[j].append(i)
            bgc[i].grid(row=11 - game.ps[j].index(i) * 2, column=3 + 2 * j)
            hpb[i].grid(row=10 - game.ps[j].index(i) * 2, column=3 + 2 * j)
        else:
            game.ps[j+3].append(i)
            bgc[i].grid(row=15 + game.ps[j+3].index(i) * 2, column=3 + 2 * j)
            hpb[i].grid(row=14 + game.ps[j+3].index(i) * 2, column=3 + 2 * j)
    for i in range(5):
        bgc[i]['fg'] = 'blue'
        bgc[i + 5]['fg'] = 'red'
    #中线初始化放置
    var_midline[0].set('~~上路河道~~')
    var_midline[1].set('~~中路河道~~')
    var_midline[2].set('~~下路河道~~')
    var_midline[3].set('~~双方泉水~~')
    #状态栏初始化
    for i in range(7):
        e_state[i].grid(row=i, column=1)
        l_state[i].grid(row=i, column=0)
    for i in range(3):#中线标签和塔血条的初始化
        b_midline[i].grid(row=13, column=3 + 2 * i)
        thpb[i].grid(row=12, column=3 + 2 * i)
    b_midline[3].grid(row=13, column=8)
    #msg初始化
    for i in range(10):
        msg_game[9-i].grid(columnspan =8)
    #俱乐部名称
    lg_blue.grid(row =11,column =0,columnspan = 2)
    lg_red.grid(row=15, column=0, columnspan=2)
def game_time_refresh():
    if game.gt[2] == 9:
        game.gt[2] =0
        game.gt[1]+=1
    else:
        game.gt[2] +=1
    if game.gt[1] == 60:
        game.gt[1] =0
        game.gt[0] +=1
    #刷新资源
    if game.gt[1] in [0, 30]:
        game.resource_fresh()
def back(ch):
    ch.dead_flag = 0
    if ch.num<5:
        b=0
    else:
        b=1
    bgc[ch.num]['bg'] = 'white'
    game.spring[b].pop(game.spring[b].index(ch.num))
    if ch.num < 5:
        game.ps[ch.tmb_flag].append(ch.num)
    else:
        game.ps[ch.tmb_flag + 3].append(ch.num)
    recoverbb()
def leave(ch):
    a = ch.tmb_flag
    if ch.num <5:
        b = 0
    else:
        b = 1
    game.ps[a + 3 * b].pop(game.ps[a + 3 * b].index(ch.num))
    ch.dead_flag =1
    bgc[ch.num]['bg'] ='grey'
    bgc[ch.num].grid_forget()
    hpb[ch.num].grid_forget()
    game.spring[b].append(ch.num)
    recoverbb()
    ch.hp=ch.hpmax
    # ch.busy += 20
    # game.pressure[b][a] +=15
def dead(ch):
    a = ch.tmb_flag
    if ch.num < 5:
        b = 0
    else:
        b = 1
    game.ps[a + 3 * b].pop(game.ps[a + 3 * b].index(ch.num))
    ch.dead_flag =1
    bgc[ch.num]['bg'] ='grey'
    game.spring[b].append(ch.num)
    recoverbb()
    ch.busy += 10 + 80 * ch.money/50000
    ch.hp = ch.hpmax
    game.pressure[b][a] += 50
def swim(ch):
    a = ch.tmb_flag
    if ch.num>5:
        b =0
    else:
        b=1
    c =[]
    for i in range(len(game.tmb_avi[b])):
        if game.pressure[b][i] >= 300 and game.tmb_avi[b][i] != a:
            c.append(game.tmb_avi[b][i])
    if c!=[]:
        r = random.randint(0,len(c)-1)
        game.pressure[b][c[r]] = 0
        move(ch,c[r])
        swim_flag =1
    else:
        swim_flag =0
    return swim_flag
def search_target(ch):
    target = 10
    if ch.num < 5 and game.ps[ch.tmb_flag+3] !=[]:
        r = random.randint(0, len(game.ps[ch.tmb_flag+3]) - 1)
        target = game.ps[ch.tmb_flag+3][r]
    elif ch.num >= 5 and game.ps[ch.tmb_flag] !=[]:
        r = random.randint(0, len(game.ps[ch.tmb_flag]) - 1)
        target = game.ps[ch.tmb_flag][r]
    return target# 返回的是编号
def tower_set(ch):#
    a=''
    b=['上路','中路','下路']
    if ch.num<5:
        a+='~红色方'
    else:
        a+='~蓝色方'
    for i in range(3):
        if ch.tmb_flag == i:
            a+=b[i]
    if ch.num<5 and len(game.tower[1][ch.tmb_flag])!= 0:
        a += str(4-len(game.tower[1][ch.tmb_flag])) + '塔~'
    elif ch.num>=5 and len(game.tower[0][ch.tmb_flag])!= 0:
        a += str(4 - len(game.tower[0][ch.tmb_flag])) + '塔~'
    elif ch.num<5 and len(game.tower[1][ch.tmb_flag])== 0:
        a ='~~红色方基地~~'
    elif ch.num>=5 and len(game.tower[0][ch.tmb_flag]) == 0:
        a ='~~蓝色方基地~~'
    for i in range(3):
        if ch.tmb_flag == i:
            var_midline[i].set(a)
def hit_tower(ch):
    tower_set(ch)
    if ch.num <5:
        a = 0
    else:
        a = 1
    b = ch.tmb_flag
    ch.busy += ch.speed
    if game.tower[1-a][b] ==[]:#如果对方b塔为空
        if b in game.tmb_avi[a]:# 检测 b是不是可去路，是就去除
            game.tmb_avi[a].pop(game.tmb_avi[a].index(b))
        if game.tmb_avi[a] !=[]:#可去的路不为空
            move(ch, game.tmb_avi[a][random.randint(0, len(game.tmb_avi[a])-1)])
        else:
            final(a)#a获胜
            game.result = a
    else:
        ch.hp -= game.tower[1 - a][b][0].damage * 18/(18 + ch.defence)
        ch.dtd -= game.tower[1 - a][b][0].damage
        if ch.hp<= 0:
            leave(ch)
            ch.busy+=20
        game.tower[1-a][b][0].hp -= ch.damage * 18/(18 + game.tower[1-a][b][0].defence - ch.through/2)
        ch.dtt += ch.damage * 18/(18 + game.tower[1-a][b][0].defence - ch.through/2)
        game.pressure[a][b]+=20
        thpb[b].refresh(game.tower[1-a][b][0].hp,game.tower[1-a][b][0].hpmax)
        if game.tower[1-a][b][0].hp <=0:#击破塔
            printf(ch.name+'击破'+var_midline[b].get())
            reportcreat(ch.nh+'击破'+var_midline[b].get())
            for i in range(5):
                game.ch[5*a+i].money += 200
            game.tower[1-a][b].pop(0)
def final(a):
    if a == 0:
        b = '蓝色方获胜！！'
        reportcreat('面对对方激烈的攻势，红色方打出GG！')
    else:
        b = '红色方获胜！！'
        reportcreat('面对对方激烈的攻势，蓝色方打出GG！')
    printf(b)
    bg4['state'] = 'disabled'
    varg1.set('开始结算')
def cal_game():
    mvp = game.cal_mvp()
    a = game.ch[mvp]
    printf('MVP的得主是：' + a.name)
    printf('在比赛中完成了：' + str(a.kda[0]) + '杀' + str(a.kda[1]) + '死' + str(a.kda[2]) + '助攻')
    printf('总英雄伤害：' + str(int(a.dtc)))
    printf('总建筑伤害：' + str(int(a.dtt)))
    printf('总吸收伤害：' + str(int(a.dtd)))
    printf('总控制时间：' + str(int(a.ctc)) + '秒')
    reportcreat('MVP的得主是：' + a.name)
    reportcreat('在比赛中完成了：' + str(a.kda[0]) + '杀' + str(a.kda[1]) + '死' + str(a.kda[2]) + '助攻')
    reportcreat('总英雄伤害：' + str(int(a.dtc)))
    reportcreat('总建筑伤害：' + str(int(a.dtt)))
    reportcreat('总吸收伤害：' + str(int(a.dtd)))
    reportcreat('总控制时间：' + str(int(a.ctc)) + '秒')
    #选手转态变化触发
    for i in range(len(myclub.player)):
        myclub.player[i].state = random.randint(-3,3)
    jc.state = random.randint(-3,3)
    #weibo更新
    weibo_creat()
def move(ch, tmb):#num号玩家移动到tmb位置
    printf(ch.name+'移动到'+['上路','中路','下路'][tmb])
    reportcreat(ch.nh+'收到队友呼救，支援到'+['上路','中路','下路'][tmb])
    a = ch.tmb_flag
    b = ch.num
    bgc[b].grid_forget()
    hpb[b].grid_forget()
    if b <5:
        game.ps[a].pop(game.ps[a].index(b))
        game.ps[tmb].append(b)
        # bgc[b].grid(row=11 - game.ps[tmb].index(b) * 2, column=3 + 2 * tmb)
        # hpb[b].grid(row=10 - game.ps[tmb].index(b) * 2, column=3 + 2 * tmb)
    else:
        game.ps[a+3].pop(game.ps[a+3].index(b))
        game.ps[tmb+3].append(b)
        # bgc[b].grid(row=15 + game.ps[tmb+3].index(b) * 2, column=3 + 2 * tmb)
        # hpb[b].grid(row=14 + game.ps[tmb+3].index(b) * 2, column=3 + 2 * tmb)
    if ch.tpcd == 0:
        ch.busy += 3
        ch.tpcd += 70
    else:
        ch.busy += 12
    ch.tmb_flag = tmb
    recoverbb()
def damage_behave(ch):
    if search_target(ch) <10:
        target = game.ch[search_target(ch)]
        target.hp -= ch.damage*18/(18+target.defence-ch.through)
        ch.dtc +=ch.damage*18/(18+target.defence-ch.through)
        target.dtd +=ch.damage
        ch.busy += ch.speed
        if target.hp <= 0:
            printf(ch.nh+'击杀'+target.nh)
            r = random.randint(0,2)
            if r == 0:
                reportcreat(ch.nh+'抓住'+target.nh+'的走位失误,完成击杀！')
            elif r ==1:
                reportcreat(ch.nh+'在野区抓到逛街的'+target.nh+'完成击杀！')
            else:
                reportcreat(ch.nh+'对'+target.nh+'持续进行消耗，最终越塔强杀！')
            ch.kda[0]+=1
            target.kda[1]+=1
            ch.kda[2]-=1
            if ch.num<5:
                for i in range(len(game.ps[ch.tmb_flag])):
                    n = game.ps[ch.tmb_flag][i]
                    game.ch[n].kda[2] += 1
                    game.ch[n].money += 50
            else:
                for i in range(len(game.ps[ch.tmb_flag+3])):
                    n = game.ps[ch.tmb_flag+3][i]
                    game.ch[n].kda[2] += 1
                    game.ch[n].money += 50
            dead(target)
            ch.money += 150
    else:
        hit_tower(ch)
def control_behave(ch):
    if ch.controlcd <=0:
        if search_target(ch) <10:
            target = game.ch[search_target(ch)]
            target.busy += ch.controltime
            ch.ctc += ch.controltime
            ch.controlcd +=20
            ch.busy+=0.5
        else:
            judgement(ch)
    else:
        judgement(ch)
def viability_behave(ch):
    if ch.hpmax-5*ch.hp>0:
        leave(ch)
        ch.busy+=20
    else:
        ch.hp += ch.healps*7
        ch.busy += 1
def farm_behave(ch):
    if ch.money<50000:
        a = ch.tmb_flag
        if ch.num<5:
            if game.resource[a][0]>0:
                ch.money+=50+int(ch.f/4)
                game.resource[a][0] -= 50
            elif game.resource[a][1]>0:
                game.resource[a][1] -= 50
            elif game.resource[a][2]>0:
                game.resource[a][2] -= 100
                ch.money +=100+int(ch.f/2)
                ch.busy += ch.speed*2
        else:
            if game.resource[a][1]>0:
                ch.money+=50+int(ch.f/4)
                game.resource[a][1] -= 50
            elif game.resource[a][0]>0:
                game.resource[a][0] -= 50
            elif game.resource[a][2]>0:
                game.resource[a][2] -= 100
                ch.money +=100+int(ch.f/2)
                ch.busy += ch.speed*2
        ch.busy += ch.speed
    else:
        damage_behave(ch)
    ch.cal()
#开启游戏按钮
bg2 = Button(frame_game, textvariable = varg1, command = play)
bg2.grid(row =0, column =1)
bgc = []#角色按钮
hpb = []#血条
thpb = []
for i in range(3):
    thpb.append(Hpbar(frame_game,fg ='yellow'))
#罗嗦的一段
def btm_player():
    def checkch0():
        game.sc =0
        refreshbb()
    def checkch1():
        game.sc =1
        refreshbb()
    def checkch2():
        game.sc =2
        refreshbb()
    def checkch3():
        game.sc =3
        refreshbb()
    def checkch4():
        game.sc =4
        refreshbb()
    def checkch5():
        game.sc =5
        refreshbb()
    def checkch6():
        game.sc =6
        refreshbb()
    def checkch7():
        game.sc =7
        refreshbb()
    def checkch8():
        game.sc =8
        refreshbb()
    def checkch9():
        game.sc =9
        refreshbb()
    bgc.append(Button(frame_game,bg='white',command =checkch0))
    bgc.append(Button(frame_game,bg='white',command =checkch1))
    bgc.append(Button(frame_game,bg='white',command =checkch2))
    bgc.append(Button(frame_game,bg='white',command =checkch3))
    bgc.append(Button(frame_game,bg='white',command =checkch4))
    bgc.append(Button(frame_game,bg='white',command =checkch5))
    bgc.append(Button(frame_game,bg='white',command =checkch6))
    bgc.append(Button(frame_game,bg='white',command =checkch7))
    bgc.append(Button(frame_game,bg='white',command =checkch8))
    bgc.append(Button(frame_game,bg='white',command =checkch9))
btm_player()
for i in range(10):
    hpb.append(Hpbar(frame_game))
b_midline =[]
#中线label
var_midline = []
for i in range(4):
    var_midline.append(StringVar())
    b_midline.append(Button(frame_game, textvariable=var_midline[i],bg ='grey'))
#时间label
varg3 = StringVar()
lg2 = Label(frame_game,textvariable =varg3).grid(row =1,column =2,columnspan = 6)
#俱乐部名称label
var_blue=StringVar()
var_red=StringVar()
lg_blue =Label(frame_game,textvariable =var_blue,fg='blue')
lg_red =Label(frame_game,textvariable =var_red,fg='red')
#状态栏label
l_state = []
e_state = []
var_state =[]
for i in range(7):
    var_state.append(StringVar())
    e_state.append(Entry(frame_game_state, textvariable=var_state[i], state ='disabled'))
    l_state.append(Label(frame_game_state,text =['姓名','KDA','经济','伤害','穿透','防御','恢复'][i]))
#msg
var_msg = []
msg_game = []
for i in range(10):
    var_msg.append(StringVar())
    var_msg[i].set('~~~~~~~')
    msg_game.append(Message(frame_game_msg,bg = "white",width = 300,textvariable =var_msg[i]))
#倍速
def gospeed():
    if bg5['text']=='1倍速':
        state.speed = 50
        bg5['text'] = '2倍速'
    elif bg5['text']=='2倍速':
        state.speed = 20
        bg5['text'] = '5倍速'
    elif bg5['text'] == '5倍速':
        state.speed = 10
        bg5['text'] = '10倍速'
    elif bg5['text'] == '10倍速':
        state.speed = 100
        bg5['text'] = '1倍速'
bg5 =Button(frame_game,text ='1倍速',command=gospeed)
bg5.grid(row =0, column =3)
def pushmin():
    for i in range(600):
        if varg1.get() == '开始结算':
            break
        else:
            refreshgame()
    recoverbb()
    refreshbb()
#加速
bg3 =Button(frame_game,text ='推进1分钟', state= 'disabled' ,command=pushmin)#
bg3.grid(row =0, column =5)
#结束游戏
bg4 =Button(frame_game, text ='结束游戏', state= 'disabled',command= end_game)
bg4.grid(row =0, column =7)


def save():
    if tkinter.messagebox.askyesno('提示', '确认要执行存档操作吗？'):
        #切回原俱乐部
        if myclub.name != '基德俱乐部':
            for i in range(len(club_list)):
                if club_list[i].name == '基德俱乐部':
                    state.cs = i
            club_list.append(Club(myclub.name))
            club_list[-1].player = myclub.player[:]
            myclub.name = club_list[state.cs].name
            myclub.player = club_list[state.cs].player[:]
            club_list.pop(state.cs)
        data = [state.date, jc, myclub.player]
        f = open('save.pckl', 'wb')
        pickle.dump(data, f)
        f.close()

def load():
    if tkinter.messagebox.askyesno('提示', '确认要执行读取操作吗？'):
        global jc
        f = open('save.pckl', 'rb')
        data = pickle.load(f)
        f.close()
        state.date = data[0]
        jc = data[1]
        myclub.player = data[2]
        refresh_win(frame_player)
        for i in range(12):  # 杰出属性显示
            varj1[i].set(
                [jc.name, jc.ladder, jc.damage, jc.control, jc.viability, jc.farm, jc.carry, jc.support, jc.fans, jc.potential,
                 cal_state(jc.state), jc.site][i])
def mode_change():
    if state.mode ==0:
        if tkinter.messagebox.askyesno('提示', '确认要切换到手机模式么？'):
            state.mode = 1
            for i in range(10):
                hpb[i].height = 50
                hpb[i].width = 400
                hpb[i].change()
                msg_game[i]['width'] = 600
            for i in range(3):
                thpb[i].height = 50
                thpb[i].width = 400
                thpb[i].change()
    else:
        if tkinter.messagebox.askyesno('提示', '确认要切换到电脑模式么？'):
            state.mode = 0
            for i in range(10):
                hpb[i].height = 18
                hpb[i].width = 100
                hpb[i].change()
                msg_game[i]['width'] = 200
            for i in range(3):
                thpb[i].height = 18
                thpb[i].width = 100
                thpb[i].change()
#menubar
menubar = Menu(win)
#　定义一个空的菜单单元
filemenu = Menu(menubar, tearoff=0)  # tearoff意为下拉
menubar.add_cascade(label='菜单', menu = filemenu)
filemenu.add_command(label='保存',command = save)#存储功能实装！
filemenu.add_command(label='载入',command = load)
filemenu.add_command(label='手机/电脑',command = mode_change)
# 分隔线
filemenu.add_separator()
filemenu.add_command(label='退出', command = win.quit)
win.config(menu = menubar)

win.mainloop()


