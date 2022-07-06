import matplotlib.pyplot as plt
import pandas as pd
pd.options.mode.chained_assignment = None #消除loc警告

cash = 100000000

flag = [0]

data = pd.read_excel('test.xlsx')
print(data)

#extract work_datas
wd = pd.DataFrame()
label_list = ['open', 'close', 'ma5', 'ma20']
wd = data[label_list]
#initial parameters
wd['pos'] = 0       #持仓数量
wd['cash'] = cash   #cash指手上的现金
wd['asset'] = 0     #初始化

'''
wd['fee'] = 0
wd['total_fee'] = 0
'''

#不考虑手续费的日均双均线交易
for i in range(len(wd)-1):  #交易到截止日期前一天
    wd['asset'][i] = wd['pos'][i] * wd['close'][i]+ wd['cash'][i]   #计算i时的资产价值
    if wd['ma5'][i] >= wd['ma20'][i]:           
        flag.append(1)                      #用flag判断是否穿越
        if flag[-1] != flag[-2]:            #发生ma5穿越ma20：
            wd['pos'][i+1] = int(wd['cash'][i] / wd['open'][i+1] / 100) * 100  #在第二天开盘时全仓买入，以100股为单位
            wd['cash'][i+1] = wd['cash'][i] - wd['pos'][i+1] * wd['open'][i+1]  #扣除相应的现金
        else:
            wd['pos'][i+1] = wd['pos'][i]
            wd['cash'][i+1]  = wd['cash'][i]   #不进行操作
    if wd['ma5'][i] < wd['ma20'][i]:
        flag.append(-1)
        if flag[-1] != flag[-2]:            #如果ma5向下穿越ma20：
            wd['cash'][i+1] = wd['cash'][i] + wd['pos'][i] * wd['open'][i+1]    #第二天开盘全仓卖出，以100股为单位
            wd['pos'][i+1] = 0              #清仓
        else:
            wd['pos'][i+1] = wd['pos'][i]
            wd['cash'][i+1]  = wd['cash'][i]   #不进行操作
wd['asset'][-1:] = wd['pos'][-1:] * wd['close'][-1:]+ wd['cash'][-1:]   #计算最后一天的asset，因为没有操作
print(wd)
