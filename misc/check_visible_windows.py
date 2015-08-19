import win32gui
def window_enum_handler(hwnd, resultList):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

def get_app_list(handles=[]):
    mlst=[]
    win32gui.EnumWindows(window_enum_handler, handles)
    for handle in handles:
        mlst.append(handle)
    return mlst


appwindows = get_app_list()

for i in appwindows:


	if i[1].find("MPlay") != -1 :
		windowName = i[1]
		


handle = win32gui.FindWindow(None, windowName)

win32gui.ShowWindow(handle, 3)


print handle	