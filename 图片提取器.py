import PySimpleGUI as sg
from PIL import ImageGrab
import win32com.client as win32
import os
import zipfile
from PIL import Image
import fitz
import re
sg.ChangeLookAndFeel('GreenTan')
menu_def = [['&使用说明', ['&注意']]]
layout = [
    [sg.Menu(menu_def, tearoff=True)],
    [sg.Frame(layout=[
    [sg.Radio('Excel1', "RADIO1",size=(10,1),key="Excel1"),  sg.Radio('Word', "RADIO1",default=True,key="Word")],
    [sg.Radio('Excel2', "RADIO1", enable_events=True, size=(10,1),key="Excel2"), sg.Radio('PDF', "RADIO1",key="PDF")]], title='选项',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
    [sg.Text('文件位置', size=(8, 1), auto_size_text=False, justification='right'),
     sg.InputText(enable_events=True,key="lujing"), sg.FolderBrowse()],
    [sg.Text('文件名字', size=(8, 1), justification='right'),
     sg.InputText(enable_events=True,key="wenjian")],
    [sg.Submit(tooltip='文件'), sg.Cancel()]]

window = sg.Window('图片提取器', layout, default_element_size=(40, 1), grab_anywhere=False)
#event, values = window.read()
while True:
    event, values = window.read()
    if event == "Submit":
        if values["Excel2"] == True:
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            f = values["lujing"] + '/' + values["wenjian"]
            f.replace('/','//')
            workbook = excel.Workbooks.Open(f)
            num = 1
            for sheet in workbook.Worksheets:
                for i, shape in enumerate(sheet.Shapes):
                    print(i)
                    print(shape.Name)
                    if shape.Name.startswith('Picture'):
                        shape.Copy()
                        image = ImageGrab.grabclipboard()
                        image.convert('RGB').save(values["lujing"]+'\{}.jpg'.format(num), 'jpeg')
                        num+=1
            excel.Quit()
            sg.Popup("提取成功")


        if values["Excel1"] == True:
            path = values["lujing"]
            count = 1
            for file in os.listdir(path):
                new_file = file.replace(".xlsx",".zip")
                os.rename(os.path.join(path,file),os.path.join(path,new_file))
                count+=1      
            number = 0
            craterDir = values["lujing"] + '/'  
            saveDir = values["lujing"] + '/' 
             
            list_dir = os.listdir(craterDir) 
            for i in range(len(list_dir)):
                if 'zip' not in list_dir[i]:
                    list_dir[i] = ''
            while '' in list_dir:
                list_dir.remove('')                            
            for zip_name in list_dir:
                print(zip_name)
                # 默认模式r,读
                azip = zipfile.ZipFile(craterDir + zip_name)
                # 返回所有文件夹和文件
                namelist = (azip.namelist())
             
                for idx in range(0,len(namelist)):
                    if namelist[idx][:9] == 'xl/media/':
                        img_name = saveDir + str(number)+'.jpg'
                        f = azip.open(namelist[idx])
                        img = Image.open(f)
                        img = img.convert("RGB")
                        img.save(img_name,"JPEG")
                        number += 1
            azip.close()  
            sg.Popup("提取成功")
        if values["Word"] == True:
            path = values["lujing"]
            count = 1
            for file in os.listdir(path):
                new_file = file.replace(".docx",".zip")
                os.rename(os.path.join(path,file),os.path.join(path,new_file))
                count+=1      
            number = 0
            craterDir = values["lujing"] + '/'  
            saveDir = values["lujing"] + '/' 
             
            list_dir = os.listdir(craterDir) 
            for i in range(len(list_dir)):
                if 'zip' not in list_dir[i]:
                    list_dir[i] = ''
            while '' in list_dir:
                list_dir.remove('')                            
            for zip_name in list_dir:
                # 默认模式r,读
                azip = zipfile.ZipFile(craterDir + zip_name)
                # 返回所有文件夹和文件
                namelist = (azip.namelist())             
                for idx in range(0,len(namelist)):
                    if namelist[idx][:11] == 'word/media/':#图片是在这个路径下
                        img_name = saveDir + str(number)+'.jpg'
                        f = azip.open(namelist[idx])
                        img = Image.open(f)
                        img = img.convert("RGB")
                        img.save(img_name,"JPEG")
                        number += 1
            azip.close()  #关闭文件，必须有，释放内存
            sg.Popup("提取成功") 
        if values["PDF"] == True:
            def pdf2pic(path, pic_path):
                # 打开pdf
                doc = fitz.open(path)
                nums = doc._getXrefLength()
                imgcount = 0 
                for i in range(1, nums):
                    text = doc._getXrefString(i)
                    if ('Width 2550' in text) and ('Height 3300' in text) or ('thumbnail' in text):
                        continue
                    checkXO = r"/Type(?= */XObject)"
                    checkIM = r"/Subtype(?= */Image)"
                    isXObject = re.search(checkXO, text)
                    isImage = re.search(checkIM, text)
                    if not isXObject or not isImage:
                        continue
                    imgcount += 1
                    pix = fitz.Pixmap(doc, i)
                    img_name = "img{}.png".format(imgcount)
                    if pix.n < 5:
                        try:
                            pix.writePNG(os.path.join(pic_path, img_name))
                            pix = None
                        except:
                            pix0 = fitz.Pixmap(fitz.csRGB, pix)
                            pix0.writePNG(os.path.join(pic_path, img_name))
                            pix0 = None
            if __name__ == '__main__':
                path = values["lujing"]+ '/' + values["wenjian"]
                pic_path = values["lujing"]
                pdf2pic(path, pic_path)
            sg.Popup("提取成功")
    if event == "Cancel" or event == sg.WIN_CLOSED:
        break    
    if event == "注意":
        sg.Popup("作用讲解：",
                 "Excel1 ：解析选定位置中所有的Excel文件，无需在文件名处填写",
                 "Excel2 ：解析选定位置中单个指定的Excel文件，需在文件名处填写",
                 "Word ：  解析选定位置中单个指定的docx结尾的文件，无需在文件名处填写",
                 "PDF ：   解析选定位置中单个指定的PDF文件，需在文件名处填写")            
