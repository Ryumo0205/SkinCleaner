import pymel.core as pm


ui_file_path = pm.internalVar(usd=True) + r"Test/SkinWeightChecker.ui"
print(ui_file_path)
MainUI = pm.loadUI(uiFile=ui_file_path)


x_scale_num = 1.0

x_scale_value = pm.textField(MainUI + r"|x_scale_value", edit=True,text=x_scale_num)
y_scale_value = pm.textField(MainUI + r"|y_scale_value", edit=True)
z_scale_value = pm.textField(MainUI + r"|z_scale_value", edit=True)
x_filter_value = pm.textField(MainUI + r"|x_filter_value", edit=True)
y_filter_value = pm.textField(MainUI + r"|y_filter_value", edit=True)
z_filter_value = pm.textField(MainUI + r"|z_filter_value", edit=True)


def x_scale_value_plus_cmd(ignoreInputs):
    print("+0.1")
    global x_scale_num
    x_scale_num = x_scale_num + 0.1
    print(x_scale_num)
    pm.textField(x_scale_value, edit=True, text=x_scale_num)

def x_scale_value_minus_cmd(ignoreInputs):
    print("-0.1")
    global x_scale_num
    x_scale_num = x_scale_num - 0.1
    print(x_scale_num)
    pm.textField(x_scale_value, edit=True, text=x_scale_num)



pm.showWindow(MainUI)