import math

import pymel.core as pm

selected_skin = pm.ls(sl=True)
get_history = pm.listHistory(selected_skin, lv=0)  # 讀取歷史紀錄
skin_name = pm.ls(get_history, type="skinCluster")  # 取得skinCluster名稱
print(skin_name)

#得到受影響的vtx,並選擇vtx
pm.skinCluster(skin_name[0], edit=True, selectInfluenceVerts="L_Arm")
inf_vtx = pm.filterExpand(sm=31)
print(inf_vtx)


x_list = []
y_list = []
z_list = []

#取得受影響的vtx的xyz座標
for i in inf_vtx:
    inf_vtx_pos = pm.pointPosition(i,w=True)
    print(inf_vtx_pos)
    x_list.append(inf_vtx_pos[0])
    y_list.append(inf_vtx_pos[1])
    z_list.append(inf_vtx_pos[2])

print(x_list)
print(y_list)
print(z_list)

#先試著處裡x軸,套入四分位數公式
print(len(x_list))

def quantile_exc(data, n):
    data.sort()
    position = (len(data))*n/4
    #print("pos",position)
    pos_integer = int(math.modf(position)[1])
    pos_decimal = position - pos_integer
    quartile = data[pos_integer - 1] + (data[pos_integer] - data[pos_integer -1]) * pos_decimal
    return quartile

print("Q1 :",quantile_exc(x_list, 1))
print("Q2 :",quantile_exc(x_list, 2))
print("Q3 :",quantile_exc(x_list, 3))

#計算離群值
IQR = quantile_exc(x_list, 3) - quantile_exc(x_list, 1)
print("IQR:",IQR)

x1 = quantile_exc(x_list, 3) + (IQR)*1.8
x2 = quantile_exc(x_list, 1) - (IQR)*1.8

print(x1,"|",x2)

for z in x_list:
    if z>x1 or z<x2 :
        print("find it:",z)
    else:
        pass
