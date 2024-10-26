from tkinter import *
import random
import numpy as np
root=Tk()
root.geometry('280x320')
root.title('2048')   #root为根窗口，desk为画布
desk=Canvas(root,width=280,height=280,background='lightcyan')
desk.pack()          #窗体及画布的基础设置
score = StringVar()
score.set('总分：')#score用来放置当前分数的文本
scorelabel=Label(root,textvariable=score,font=('黑体',12)).place_configure(x=0,y=290)#设置计分窗口
A=np.full((4,4),0)#A二维数组用来记录当前数字
B=np.full((4,4),0)#B二维数组用0和1来记录有数字的位置
score1=0#score1用来存储当前分数
#画线
for i in range(0, 5):
    desk.create_line(i * 60 + 20, 20, i * 60 + 20, 260)
    desk.create_line(20, i * 60 + 20, 260, i * 60 + 20)
def calculatescore():#计算总分的函数
    global A,score1,score
    score1=np.sum(A)#用np.sum函数计算数组A的分数总和
    score.set('总分:'+str(score1))#更新score文本的内容为score1
def redraw():#更新图案及重新画线的函数
    global A,B,desk
    desk.delete("all")
    for i in range(0, 5):#重新画线
        desk.create_line(i * 60 + 20, 20, i * 60 + 20, 260)
        desk.create_line(20, i * 60 + 20, 260, i * 60 + 20)
    for i in range(0,4):
        for j in range (0,4):
            if B[i][j]==1:
                desk.create_text(j * 60 + 50, i * 60 + 50, text=A[i][j], font=('宋体', 20), fill='#000000')#更新图案
def createrandom():#在随机空位置设置
    global A,B,desk
    spacelist=[]#用space数组储存空的位置
    space=np.where(B==0)
    for i in zip(list(space[0]),list(space[1])):
        spacelist.append(i)#找出空位置并将空位置坐标存储进spacelist数组
    randint=random.randint(0,len(spacelist)-1)#随机找到一个空坐标
    x=spacelist[randint][0]
    y=spacelist[randint][1]
    A[x][y]=2#将空位置赋值为2
    B[x][y]=1#在B二维数组中将此位置标记为有数字
    redraw()#更新图案
    calculatescore()#更新分数
def order(alist):#排序函数：将非零数向左移，将0向右移
    blist=list(filter(lambda x:x>0,alist))
    clist=list(filter(lambda x:x==0,alist))
    dlist=blist+clist
    return dlist
def push(alist):#实现推这一动作，先进行排序，再将相邻的相等数合并，再进行排序
    alist=order(alist)#排序
    for i in range(0, len(alist) - 1):#相同数合并
        j = i + 1
        if alist[j] > 0:
            if alist[j] == alist[i]:
                alist[i] += alist[j]
                alist[j] = 0
    alist =order(alist)#排序
    return alist
def left(event):#摁下左键的事件
    global A,B
    A0=A#将操作前的A数组存入A0，便于判断数组A有无发生变化
    A1=A.tolist()
    A2=[push(i) for i in A1]#将A数组的每一行分别进行推的处理
    A=np.array(A2)#更新A数组
    B = np.full((4, 4), 0)#更新B数组
    space= np.where(A > 0)
    for i in zip(list(space[0]), list(space[1])):
        B[i[0]][i[1]] = 1
    if (A == A0).all() == False:#如果A数组发生改变就在随机空处放置2
        createrandom()
def right(event):#摁下右键的事件，原理不变，但向右推需要反转再进行操作
    global A, B
    A0 = A
    A1=A.tolist()
    A2 = [list(reversed(push(list(reversed(i))))) for i in A1]
    A = np.array(A2)
    B = np.full((4, 4), 0)
    space = np.where(A > 0)
    for i in zip(list(space[0]), list(space[1])):
        B[i[0]][i[1]] = 1
    if (A == A0).all() == False:
        createrandom()
def up(event):#摁下上键的事件，推的实现是:转置后再向左推
    global A,B
    A0=A
    A=np.transpose(A)
    A1=A.tolist()
    A2=[push(i)for i in A1]
    A=np.array(A2)
    A=np.transpose(A)
    B = np.full((4, 4), 0)
    space = np.where(A > 0)
    for i in zip(list(space[0]), list(space[1])):
        B[i[0]][i[1]] = 1
    if (A == A0).all() == False:
        createrandom()
def down(event):#摁下下键的事件，推的实现是:转置后再向右推
    global A,B
    A0=A
    A=np.transpose(A)
    A1=A.tolist()
    A2 = [list(reversed(push(list(reversed(i))))) for i in A1]
    A = np.array(A2)
    A=np.transpose(A)
    B = np.full((4, 4), 0)
    space = np.where(A > 0)
    for i in zip(list(space[0]), list(space[1])):
        B[i[0]][i[1]] = 1
    if (A == A0).all() == False:
        createrandom()
createrandom()
root.bind("<KeyPress-Right>", right)
root.bind("<KeyPress-Up>", up)
root.bind("<KeyPress-Left>", left)
root.bind("<KeyPress-Down>",down)
mainloop()
