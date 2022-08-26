import math

import pymel.core as pm

def quantile_exc(data, n):
    data.sort()
    position = (len(data))*n/4
    #print("pos",position)
    pos_integer = int(math.modf(position)[1])
    pos_decimal = position - pos_integer
    quartile = data[pos_integer - 1] + (data[pos_integer] - data[pos_integer -1]) * pos_decimal
    return quartile


selected_skin = pm.ls(sl=True)
get_history = pm.listHistory(selected_skin, lv=0)  # 讀取歷史紀錄
skin_name = pm.ls(get_history, type="skinCluster")  # 取得skinCluster名稱
print(skin_name)

#得到受影響的vtx,並選擇vtx
pm.skinCluster(skin_name[0], edit=True, selectInfluenceVerts="L_Arm")
inf_vtx = pm.filterExpand(sm=31)
print(inf_vtx)

vtx_pos_dict = {}
x_list = []
y_list = []
z_list = []

#取得受影響的vtx的xyz座標
for i in inf_vtx:
    inf_vtx_pos = pm.pointPosition(i,w=True)
    vtx_pos_dict[i] = inf_vtx_pos
    #print(inf_vtx_pos)
    x_list.append(inf_vtx_pos[0])
    y_list.append(inf_vtx_pos[1])
    z_list.append(inf_vtx_pos[2])

# print(x_list)
# print(y_list)
# print(z_list)
# for zzz in vtx_pos_dict.items():
#     print(zzz)

#-------------------------------------------------------------------------------#

#先試著處裡x軸,套入四分位數公式
print(len(vtx_pos_dict))

def check_vtx(IQRscale):
    if IQRscale < 1.0 or IQRscale > 2.0:
        pm.select(clear=True)
        return
    x_fix_vtx = []
    y_fix_vtx = []
    z_fix_vtx = []
    #動態生成變數,將四分位數放入各自xyz變數
    for q in range(3):
        q = q + 1
        globals()["x_Q"+str(q)] = quantile_exc(x_list, q)
    for q in range(3):
        q = q + 1
        globals()["y_Q"+str(q)] = quantile_exc(y_list, q)
    for q in range(3):
        q = q + 1
        globals()["z_Q"+str(q)] = quantile_exc(z_list, q)
    #計算離群值
    x_IQR = x_Q3 - x_Q1
    y_IQR = y_Q3 - y_Q1
    z_IQR = z_Q3 - z_Q1
    print("x_IQR:",x_IQR)
    print("x_IQR:",y_IQR)
    print("x_IQR:",z_IQR)


    x_IQR_max = x_Q3 + (x_IQR) * IQRscale
    x_IQR_min = x_Q1 - (x_IQR) * IQRscale
    y_IQR_max = y_Q3 + (y_IQR) * IQRscale
    y_IQR_min = y_Q1 - (y_IQR) * IQRscale
    z_IQR_max = z_Q3 + (z_IQR) * IQRscale
    z_IQR_min = z_Q1 - (z_IQR) * IQRscale

    print("x_outliyer:",x_IQR_max,"|",x_IQR_min)
    print("y_outliyer:",y_IQR_max,"|",y_IQR_min)
    print("z_outliyer:",z_IQR_max,"|",z_IQR_min)
    
    #比對是否超出離群值,將超出的vtx加入需要修正的名單
    for p1 in vtx_pos_dict.items():
        if p1[1][0] > x_IQR_max or p1[1][0] < x_IQR_min :
            x_fix_vtx.append(p1[0])
        else:
            pass
    for p2 in vtx_pos_dict.items():
        if p2[1][1] > y_IQR_max or p2[1][1] < y_IQR_min :
            y_fix_vtx.append(p1[0])
        else:
            pass
    for p3 in vtx_pos_dict.items():
        if p3[1][2] > z_IQR_max or p3[1][2] < z_IQR_min :
            z_fix_vtx.append(p1[0])
        else:
            pass
    #合併xyz名單,刪除重複的vtx
    fix_vtx = set(x_fix_vtx + y_fix_vtx + z_fix_vtx)
    fix_vtx = list(fix_vtx)
    return fix_vtx
#-----------------------------------------------------------------------------------#

fixed_vtx = check_vtx(1.0)

print(fixed_vtx)
if fixed_vtx ==  None:
    pm.warning("IQRscale must 1.0 ~ 2.0 .")
else:
    pm.select(fixed_vtx)