import math
import pymel.core as pm


selected_skin = pm.ls(sl=True)
get_history = pm.listHistory(selected_skin, lv=0)
skin_name = pm.ls(get_history, type="skinCluster")  
inf_list = pm.skinCluster(skin_name, query=True, weightedInfluence=True)
print(inf_list)


def quantile_exc(data, n):
    data.sort()
    position = (len(data))*n/4
    #print("pos",position)
    pos_integer = int(math.modf(position)[1])
    pos_decimal = position - pos_integer
    quartile = data[pos_integer - 1] + (data[pos_integer] - data[pos_integer -1]) * pos_decimal
    return quartile




#-------------------------------------------------------------------------------#

#套入四分位數公式

def check_vtx(x_IQRscale,y_IQRscale,z_IQRscale,InfluencesName=str):
    """
    使用迴圈填入參數,能一次遍歷所有骨架影響
    """
    print("Go!")
    if x_IQRscale < 1.0 or x_IQRscale > 10:
        pm.select(clear=True)
        return
    if y_IQRscale < 1.0 or y_IQRscale > 10:
        pm.select(clear=True)
        return
    if z_IQRscale < 1.0 or z_IQRscale > 10:
        pm.select(clear=True)
        return


    vtx_pos_dict = {}
    x_list = []
    y_list = []
    z_list = []

    x_fix_vtx = []
    y_fix_vtx = []
    z_fix_vtx = []

    #取得受影響的vtx
    pm.skinCluster(skin_name[0], edit=True, selectInfluenceVerts=InfluencesName)
    inf_vtx = pm.filterExpand(sm=31)
    if inf_vtx == None:
        return

    inf_vtx_len = len(inf_vtx)
    print("inf_vtx_len:",inf_vtx_len)


    #取得受影響的vtx的xyz座標
    for i in inf_vtx:
        inf_vtx_pos = pm.pointPosition(i,w=True)
        vtx_pos_dict[i] = inf_vtx_pos
        #print(inf_vtx_pos)
        x_list.append(inf_vtx_pos[0])
        y_list.append(inf_vtx_pos[1])
        z_list.append(inf_vtx_pos[2])


    #動態生成變數,將四分位數放入各自xyz變數
    for qx in range(3):
        qx = qx + 1
        globals()["x_Q"+str(qx)] = quantile_exc(x_list, qx)
    for qy in range(3):
        qy = qy + 1
        globals()["y_Q"+str(qy)] = quantile_exc(y_list, qy)
    for qz in range(3):
        qz = qz + 1
        globals()["z_Q"+str(qz)] = quantile_exc(z_list, qz)
    
    #計算四分位距
    x_IQR = x_Q3 - x_Q1
    y_IQR = y_Q3 - y_Q1
    z_IQR = z_Q3 - z_Q1
    print("x_Q3:",x_Q3,"x_Q1:",x_Q1)
    print("y_Q3:",y_Q3,"y_Q1:",y_Q1)
    print("z_Q3:",z_Q3,"z_Q1:",z_Q1)

    print("x_IQR:",x_IQR)
    print("y_IQR:",y_IQR)
    print("z_IQR:",z_IQR)

    #計算離群值乘上倍率
    x_IQR_max = (x_Q3 + (x_IQR * x_IQRscale))
    x_IQR_min = (x_Q1 - (x_IQR * x_IQRscale))
    y_IQR_max = (y_Q3 + (y_IQR * y_IQRscale))
    y_IQR_min = (y_Q1 - (y_IQR * y_IQRscale))
    z_IQR_max = (z_Q3 + (z_IQR * z_IQRscale))
    z_IQR_min = (z_Q1 - (z_IQR * z_IQRscale))

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
            y_fix_vtx.append(p2[0])
        else:
            pass
  
    for p3 in vtx_pos_dict.items():
        if p3[1][2] > z_IQR_max or p3[1][2] < z_IQR_min :
            z_fix_vtx.append(p3[0])
        else:
            pass

    #合併xyz名單,刪除重複的vtx,返回一個被檢測出有問題的vtx的list
    print(x_fix_vtx)
    print(y_fix_vtx)
    print(z_fix_vtx)
    fix_vtx = set(x_fix_vtx + y_fix_vtx + z_fix_vtx)
    fix_vtx = list(fix_vtx)
    return fix_vtx , inf_vtx_len
#-----------------------------------------------------------------------------------#
checked_vtx_list = []

# 執行迴圈檢查所有的骨架
for one_inf in inf_list:

    #檢測第一次 該次檢測的影響沒有權重就沒有資料輸出,就加入None
    checked_data = check_vtx(1.0, 1.0, 1.0, one_inf)
    if checked_data == None :
        temp_list = [one_inf,None]
        checked_vtx_list.append(temp_list)
        continue
    else:
        # 取得vtx編號跟列表長度
        fix_vtx = checked_data[0]
        data_len = checked_data[1]
        x_att , y_att ,z_att = 1.0, 1.0, 1.0
        #print(len(fix_vtx) / float(data_len))

        # 用迴圈來檢查是否異常點過多,過多的話就放寬數值進下一次迴圈,直到異常點的數量是檢測點數量的1%以下
        while True:
            if data_len < 3 :   #####這邊有問題,不能用點來判斷會除不盡
                temp_list = [one_inf,None]
                checked_vtx_list.append(temp_list)
                break
            else:
                pass
            if len(fix_vtx) / float(data_len) > 0.01 :
                x_att += 0.2
                y_att += 0.2
                z_att += 0.2
                checked_data = check_vtx(x_att, y_att, z_att, one_inf)
                fix_vtx = checked_data[0]
                data_len = checked_data[1]
                # print(len(fix_vtx))
                # print(data_len)
                print(len(fix_vtx) / float(data_len))
                print("smooth!")
            else:
                break
        # 如果沒有檢測出異常點就加入none
        if fix_vtx == [] :
            temp_list = [one_inf,None]
            checked_vtx_list.append(temp_list)
        else:
            globals()[one_inf+"_vtx_list"] = fix_vtx
            temp_list = [one_inf,globals()[one_inf + "_vtx_list"]]
            checked_vtx_list.append(temp_list)

print("OK!")
print(L_Arm_list)

for iq in checked_vtx_list:
    if iq[1] == None :
        pass
    else:
        print(iq)
# checked_data = check_vtx(1.0, 1.0, 1.0, "L_Arm")
# fix_vtx = checked_data[0]
# data_len = checked_data[1]

# print(len(fix_vtx))
# print(data_len)
# print(len(fix_vtx) / float(data_len))



# 執行方法,得到有問題的vtx的list
# for one_inf in inf_list:
#     print(one_inf)
#     checked_data = check_vtx(1.3,1.5,1.0,one_inf) 
#     print(one_inf, checked_data)




#選擇並顯示有問題的點
# if fix_vtx ==  None:
#     pm.warning("IQRscale must 1.0 ~ 2.0 .")
# else:
#     pass
#     pm.select(fix_vtx)