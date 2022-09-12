import math
import pymel.core as pm
import sys
sys.path.append(r'D:/file/Code/MayaCode/SkinCleaner')

#output = pm.cmdFileOutput(open=r"D:\file\Code\MayaCode\SkinCleaner\log.txt")

def getinfo():
    selected_skin = pm.ls(sl=True)
    get_history = pm.listHistory(selected_skin, lv=0)
    skin_name = pm.ls(get_history, type="skinCluster")  
    inf_list = pm.skinCluster(skin_name, query=True, weightedInfluence=True)
    return skin_name, inf_list


def quantile_exc(data, n):
    """
    
    """
    data.sort()
    position = (len(data))*n/4
    #print("pos",position)
    pos_integer = int(math.modf(position)[1])
    pos_decimal = position - pos_integer
    quartile = data[pos_integer - 1] + (data[pos_integer] - data[pos_integer -1]) * pos_decimal
    return quartile


def check_vtx(x_IQRscale,y_IQRscale,z_IQRscale,InfluencesName=str):
    """
    
    """
    data = getinfo()
    skin_name = data[0]

    print("Checking...",InfluencesName)
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

    #
    pm.skinCluster(skin_name[0], edit=True, selectInfluenceVerts=InfluencesName)
    inf_vtx = pm.filterExpand(sm=31)
    if inf_vtx == None:
        return

    inf_vtx_len = len(inf_vtx)
    print("inf_vtx_len:",inf_vtx_len,)


    #
    for i in inf_vtx:
        inf_vtx_pos = pm.pointPosition(i,w=True)
        vtx_pos_dict[i] = inf_vtx_pos
        #print(inf_vtx_pos)
        x_list.append(inf_vtx_pos[0])
        y_list.append(inf_vtx_pos[1])
        z_list.append(inf_vtx_pos[2])


    #
    for qx in range(3):
        qx = qx + 1
        globals()["x_Q"+str(qx)] = quantile_exc(x_list, qx)
    for qy in range(3):
        qy = qy + 1
        globals()["y_Q"+str(qy)] = quantile_exc(y_list, qy)
    for qz in range(3):
        qz = qz + 1
        globals()["z_Q"+str(qz)] = quantile_exc(z_list, qz)
    
    #
    x_IQR = x_Q3 - x_Q1
    y_IQR = y_Q3 - y_Q1
    z_IQR = z_Q3 - z_Q1
    print("x_Q3:",x_Q3,"x_Q1:",x_Q1)
    print("y_Q3:",y_Q3,"y_Q1:",y_Q1)
    print("z_Q3:",z_Q3,"z_Q1:",z_Q1)

    print("x_IQR:",x_IQR)
    print("y_IQR:",y_IQR)
    print("z_IQR:",z_IQR)

    #
    x_IQR_max = (x_Q3 + (x_IQR * x_IQRscale))
    x_IQR_min = (x_Q1 - (x_IQR * x_IQRscale))
    y_IQR_max = (y_Q3 + (y_IQR * y_IQRscale))
    y_IQR_min = (y_Q1 - (y_IQR * y_IQRscale))
    z_IQR_max = (z_Q3 + (z_IQR * z_IQRscale))
    z_IQR_min = (z_Q1 - (z_IQR * z_IQRscale))

    print("x_outliyer:",x_IQR_max,"|",x_IQR_min)
    print("y_outliyer:",y_IQR_max,"|",y_IQR_min)
    print("z_outliyer:",z_IQR_max,"|",z_IQR_min)
    
    #
    
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

    #
    fix_vtx = set(x_fix_vtx + y_fix_vtx + z_fix_vtx)
    fix_vtx = list(fix_vtx)
    return fix_vtx , inf_vtx_len

#-----------------------------------------------------------------------------------#
def run(scale_value=list, filter_value=list):
    """
    
    """
    output = pm.cmdFileOutput(open=r"D:\file\Code\MayaCode\SkinCleaner\log.txt")
    # from string to float
    scale_list = scale_value
    scale_list = map(float,scale_value)

    filter_list = filter_value
    filter_list = map(float,filter_value)

    print("main:",scale_list)
    print("main:",filter_list)
    #================================#
    data = getinfo()
    inf_list = data[1]

    checked_vtx_list = []
    # 
    for one_inf in inf_list:

        #
        checked_data = check_vtx(scale_list[0], scale_list[1], scale_list[2], one_inf)
        if checked_data == None :
            temp_list = [one_inf,None]
            checked_vtx_list.append(temp_list)
            continue
        else:
            # 
            fix_vtx = checked_data[0]
            data_len = checked_data[1]
            x_att , y_att ,z_att = scale_list[0], scale_list[1], scale_list[2]
            #print(len(fix_vtx) / float(data_len))

            # 
            counter = 0
            while counter < 5 :
                print(counter)
                counter += 1
                if len(fix_vtx) / float(data_len) > 0.01 :
                    x_att += filter_list[0]
                    y_att += filter_list[1]
                    z_att += filter_list[2]
                    checked_data = check_vtx(x_att, y_att, z_att, one_inf)
                    fix_vtx = checked_data[0]
                    data_len = checked_data[1]
                    # print(len(fix_vtx))
                    # print(data_len)
                    print(len(fix_vtx) / float(data_len))
                    print("smooth!")
                else:
                    break
            # 
            if fix_vtx == [] :
                temp_list = [one_inf,None]
                checked_vtx_list.append(temp_list)
            else:
                globals()[one_inf+"_vtx_list"] = fix_vtx
                temp_list = [one_inf,globals()[one_inf + "_vtx_list"]]
                checked_vtx_list.append(temp_list)

    pm.cmdFileOutput(closeAll=True)
    print("all finished ! ")
    return checked_vtx_list



#pm.cmdFileOutput(closeAll=True)
if __name__ == "__main__":
    print("please use GUI")
else:
    pass

# getlist = run()
# for iq in getlist:
#     print(iq[0])
#     if iq[1] == None :
#         pass
#     else:
#         print(iq)



#
# if fix_vtx ==  None:
#     pm.warning("IQRscale must 1.0 ~ 2.0 .")
# else:
#     pass
#     pm.select(fix_vtx)

#pm.showWindow(UI_fn.MainUI)