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
    if x_IQRscale < 1.0 or x_IQRscale > 30:
        pm.select(clear=True)
        return
    if y_IQRscale < 1.0 or y_IQRscale > 30:
        pm.select(clear=True)
        return
    if z_IQRscale < 1.0 or z_IQRscale > 30:
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
    # #計算離群值
    x_IQR = x_Q3 - x_Q1
    y_IQR = y_Q3 - y_Q1
    z_IQR = z_Q3 - z_Q1
    print("x_IQR:",x_IQR)
    print("y_IQR:",y_IQR)
    print("z_IQR:",z_IQR)

    ######為求精準此處應加入Q1Q3的象限判別#######
    x_IQR_max = (x_Q3 + x_IQR) * x_IQRscale
    x_IQR_min = (x_Q1 - x_IQR) * (1.0 / x_IQRscale)
    y_IQR_max = (y_Q3 + y_IQR) * y_IQRscale
    y_IQR_min = (y_Q1 - y_IQR) * (1.0 / y_IQRscale)
    z_IQR_max = (z_Q3 + z_IQR) * z_IQRscale
    z_IQR_min = (z_Q1 - z_IQR) * (1.0 / z_IQRscale)

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
    fix_vtx = set(x_fix_vtx + y_fix_vtx + z_fix_vtx)
    fix_vtx = list(fix_vtx)
    return fix_vtx
#-----------------------------------------------------------------------------------#


#fixed_vtx = check_vtx(1.3,1.5,1.0,"L_Arm")
#執行方法,得到有問題的vtx的list
for one_inf in inf_list:
    print(one_inf)
    fixed_vtx = check_vtx(1.3,1.5,1.0,one_inf)
    print(one_inf, fixed_vtx)

#選擇並顯示有問題的點
if fixed_vtx ==  None:
    pm.warning("IQRscale must 1.0 ~ 2.0 .")
else:
    pass
    #pm.select(fixed_vtx)