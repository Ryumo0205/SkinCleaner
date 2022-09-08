import pymel.core as pm
import main

ui_file_path = pm.internalVar(usd=True) + r"Test/SkinWeightChecker.ui"
print(ui_file_path)
MainUI = pm.loadUI(uiFile=ui_file_path)

x_scale_num = 1.0
y_scale_num = 1.0
z_scale_num = 1.0
x_filter_num = 0.1
y_filter_num = 0.1
z_filter_num = 0.1

x_scale_value = pm.textField(MainUI + r"|x_scale_value", edit=True, text=x_scale_num)
y_scale_value = pm.textField(MainUI + r"|y_scale_value", edit=True, text=y_scale_num)
z_scale_value = pm.textField(MainUI + r"|z_scale_value", edit=True, text=z_scale_num)
x_filter_value = pm.textField(MainUI + r"|x_filter_value", edit=True, text=x_filter_num)
y_filter_value = pm.textField(MainUI + r"|y_filter_value", edit=True, text=y_filter_num)
z_filter_value = pm.textField(MainUI + r"|z_filter_value", edit=True, text=z_filter_num)

outliyer_list = pm.textScrollList(MainUI + r"|outliyer_list", edit=True, sc="get_list_selected()")

def ui_import_test():
    print("uiimporttest")

def x_scale_value_plus_cmd(ignoreInputs):
    global x_scale_num
    get_num = x_scale_value.getText()
    print("+0.1")
    x_scale_num = float(get_num) + 0.1
    if x_scale_num >= 5.0 or x_scale_num <= 1.0 :
        if x_scale_num < 0.0 :
            x_scale_num = 1.0
        else:
            x_scale_num = 5.0
        print(x_scale_num)
        pm.textField(x_scale_value, edit=True, text=x_scale_num)
        pm.warning("maximum 5.0")
        return
    else:
        print(x_scale_num)
        pm.textField(x_scale_value, edit=True, text=x_scale_num)

def x_scale_value_minus_cmd(ignoreInputs):
    global x_scale_num
    print("-0.1")
    get_num = x_scale_value.getText()
    x_scale_num = float(get_num) - 0.1
    if x_scale_num >= 5.0 or x_scale_num <= 1.0 :
        if x_scale_num > 5.0  :
            x_scale_num = 5.0
        else:
            x_scale_num = 1.0
        print(x_scale_num)
        pm.textField(x_scale_value, edit=True, text=x_scale_num)
        pm.warning("minimum 1.0",n=False)
        return
    else:
        print(x_scale_num)
        pm.textField(x_scale_value, edit=True, text=x_scale_num)

def y_scale_value_plus_cmd(ignoreInputs):
    global y_scale_num
    get_num = y_scale_value.getText()
    print("+0.1")
    y_scale_num = float(get_num) + 0.1
    if y_scale_num >= 5.0 or y_scale_num <= 1.0 :
        if y_scale_num < 0.0  :
            y_scale_num = 1.0
        else:
            y_scale_num = 5.0
        print(y_scale_num)
        pm.textField(y_scale_value, edit=True, text=y_scale_num)
        pm.warning("maximum 5.0")
        return
    else:
        print(y_scale_num)
        pm.textField(y_scale_value, edit=True, text=y_scale_num)

def y_scale_value_minus_cmd(ignoreInputs):
    print("-0.1")
    global y_scale_num
    get_num = y_scale_value.getText()
    y_scale_num = float(get_num) - 0.1
    if y_scale_num >= 5.0 or y_scale_num <= 1.0 :
        if y_scale_num > 5.0  :
            y_scale_num = 5.0
        else:
            y_scale_num = 1.0
        print(y_scale_num)
        pm.textField(y_scale_value, edit=True, text=y_scale_num)
        pm.warning("minimum 1.0")
        return
    else:
        print(y_scale_num)
        pm.textField(y_scale_value, edit=True, text=y_scale_num)

def z_scale_value_plus_cmd(ignoreInputs):
    print("+0.1")
    global z_scale_num
    get_num = z_scale_value.getText()
    z_scale_num = float(get_num) + 0.1
    if z_scale_num >= 5.0 or z_scale_num <= 1.0 :
        if z_scale_num < 0.0  :
            z_scale_num = 1.0
        else:
            z_scale_num = 5.0
        print(z_scale_num)
        pm.textField(z_scale_value, edit=True, text=z_scale_num)
        pm.warning("maximum 5.0")
        return
    else:
        print(z_scale_num)
        pm.textField(z_scale_value, edit=True, text=z_scale_num)

def z_scale_value_minus_cmd(ignoreInputs):
    print("-0.1")
    global z_scale_num
    get_num = z_scale_value.getText()
    z_scale_num = float(get_num) - 0.1
    if z_scale_num >= 5.0 or z_scale_num <= 1.0 :
        if z_scale_num > 5.0  :
            z_scale_num = 5.0
        else:
            z_scale_num = 1.0
        print(z_scale_num)
        pm.textField(z_scale_value, edit=True, text=z_scale_num)
        pm.warning("minimum 1.0")
        return
    else:
        print(z_scale_num)
        pm.textField(z_scale_value, edit=True, text=z_scale_num)

def x_filter_value_plus_cmd(ignoreInputs):
    print("+0.1")
    global x_filter_num
    get_num = x_filter_value.getText()
    x_filter_num = float(get_num) + 0.1
    if x_filter_num >= 0.5 :
        x_filter_num = 0.5
        print(x_filter_num)
        pm.textField(x_filter_value, edit=True, text=x_filter_num)
        pm.warning("maximum 0.5")
        return
    else:
        print(x_filter_num)
        pm.textField(x_filter_value, edit=True, text=x_filter_num)

def x_filter_value_minus_cmd(ignoreInputs):
    print("-0.1")
    global x_filter_num
    get_num = x_filter_value.getText()
    x_filter_num = float(get_num) - 0.1
    if x_filter_num <= 0.1 :
        x_filter_num = 0.1
        print(x_filter_num)
        pm.textField(x_filter_value, edit=True, text=x_filter_num)
        pm.warning("minimum 0.1")
        return
    else:
        print(x_filter_num)
        pm.textField(x_filter_value, edit=True, text=x_filter_num)

def y_filter_value_plus_cmd(ignoreInputs):
    print("+0.1")
    global y_filter_num
    get_num = y_filter_value.getText()
    y_filter_num = float(get_num) + 0.1
    if y_filter_num >= 0.5 :
        y_filter_num = 0.5
        print(y_filter_num)
        pm.textField(y_filter_value, edit=True, text=y_filter_num)
        pm.warning("maximum 0.5")
        return
    else:
        print(y_filter_num)
        pm.textField(y_filter_value, edit=True, text=y_filter_num)

def y_filter_value_minus_cmd(ignoreInputs):
    print("-0.1")
    global y_filter_num
    get_num = y_filter_value.getText()
    y_filter_num = float(get_num) - 0.1
    if y_filter_num <= 0.1 :
        y_filter_num = 0.1
        print(y_filter_num)
        pm.textField(y_filter_value, edit=True, text=y_filter_num)
        pm.warning("minimum 0.1")
        return
    else:
        print(y_filter_num)
        pm.textField(y_filter_value, edit=True, text=y_filter_num)

def z_filter_value_plus_cmd(ignoreInputs):
    print("+0.1")
    global z_filter_num
    get_num = z_filter_value.getText()
    z_filter_num = float(get_num) + 0.1
    if z_filter_num >= 0.5 :
        z_filter_num = 0.5
        print(z_filter_num)
        pm.textField(z_filter_value, edit=True, text=z_filter_num)
        pm.warning("maximum 0.5")
        return
    else:
        print(z_filter_num)
        pm.textField(z_filter_value, edit=True, text=z_filter_num)

def z_filter_value_minus_cmd(ignoreInputs):
    print("-0.1")
    global z_filter_num
    get_num = z_filter_value.getText()
    z_filter_num = float(get_num) - 0.1
    if z_filter_num <= 0.1 :
        z_filter_num = 0.1
        print(z_filter_num)
        pm.textField(z_filter_value, edit=True, text=z_filter_num)
        pm.warning("minimum 0.1")
        return
    else:
        print(z_filter_num)
        pm.textField(z_filter_value, edit=True, text=z_filter_num)

def run_cmd(ignoreInputs):
    print("Run ! ")
    ##################影響名稱放到字典裡就沒辦法索引幹############
    global query_dict
    query_dict = {}


    getlist = main.run()
    print(getlist)
    for iq in getlist:
        if iq[1] == None :
            pass
        else:
            #print(iq[0])
            pm.textScrollList(outliyer_list , edit=True, append=iq[0])
            query_dict[iq[0]]=iq[1]
    
    


def get_list_selected():
    
    get_name = pm.textScrollList(outliyer_list, q=True, si=True)
    print(get_name)

    for i in query_dict.items():
        if get_name[0] == i[0] :
            pm.select(i[1])
            break
        else:
            pass

if __name__ == "__main__":
    window = pm.showWindow(MainUI)