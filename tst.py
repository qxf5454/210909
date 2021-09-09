import cv2
import numpy as np
import sys,os

from PySide2.QtCore import (Signal,Slot,Property, QEasingCurve, QObject, QPropertyAnimation,
                            QPoint, QPointF, QRect, QRectF, QSize, Qt)
from PySide2.QtGui import (QBrush, QColor, QIcon, QLinearGradient, QPainter,
                           QPainterPath, QPen, QPixmap)
from PySide2.QtWidgets import (QApplication, QGraphicsPixmapItem,
                               QGraphicsItem, QGraphicsScene, QGraphicsView,
                               QListWidget, QListWidgetItem, QWidget)
from numpy import mat, matrix
import cv2 as cv
from numpy.core.fromnumeric import size
from PIL import Image
from PIL import ImageQt
from ui3 import *



# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'
sys.path.append("../MvImport")
from MvCameraControl_class import *
from CamOperation_class import *



class Work_thread(QThread):

    

    updatepic=Signal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self,parent)
        
        #self.signal.connect(parent.start)

    def run(self):
        stOutFrame = MV_FRAME_OUT()  
        img_buff = None
        buf_cache = None
        numArray = None
        global obj_cam_operation
        
        

        
        while True:
            
            ret = obj_cam_operation.obj_cam.MV_CC_GetImageBuffer(stOutFrame, 1000)
            if 0 == ret:
                if None == buf_cache:
                    buf_cache = (c_ubyte * stOutFrame.stFrameInfo.nFrameLen)()
                #获取到图像的时间开始节点获取到图像的时间开始节点
                obj_cam_operation.st_frame_info = stOutFrame.stFrameInfo
                cdll.msvcrt.memcpy(byref(buf_cache), stOutFrame.pBufAddr, obj_cam_operation.st_frame_info.nFrameLen)
                print ("get one frame: Width[%d], Height[%d], nFrameNum[%d]"  % (obj_cam_operation.st_frame_info.nWidth, obj_cam_operation.st_frame_info.nHeight, obj_cam_operation.st_frame_info.nFrameNum))
                obj_cam_operation.n_save_image_size = obj_cam_operation.st_frame_info.nWidth * obj_cam_operation.st_frame_info.nHeight * 3 + 2048
                if img_buff is None:
                    img_buff = (c_ubyte * obj_cam_operation.n_save_image_size)()
                
                if True == obj_cam_operation.b_save_jpg:
                    obj_cam_operation.Save_jpg(buf_cache) #ch:保存Jpg图片 | en:Save Jpg
                if True == obj_cam_operation.b_save_bmp:
                    obj_cam_operation.Save_Bmp(buf_cache) #ch:保存Bmp图片 | en:Save Bmp
            else:
                print("no data, nret = "+obj_cam_operation.To_hex_str(ret))
                continue
            
            #转换像素结构体赋值
            stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
            memset(byref(stConvertParam), 0, sizeof(stConvertParam))
            stConvertParam.nWidth = obj_cam_operation.st_frame_info.nWidth
            stConvertParam.nHeight = obj_cam_operation.st_frame_info.nHeight
            stConvertParam.pSrcData = cast(buf_cache, POINTER(c_ubyte))
            stConvertParam.nSrcDataLen = obj_cam_operation.st_frame_info.nFrameLen
            stConvertParam.enSrcPixelType = obj_cam_operation.st_frame_info.enPixelType 

            

            #if PixelType_Gvsp_Mono8 == obj_cam_operation.st_frame_info.enPixelType:
            #    numArray=CameraOperation.Mono_numpy(obj_cam_operation,buf_cache,obj_cam_operation.st_frame_info.nWidth,obj_cam_operation.st_frame_info.nHeight)
                
            # RGB直接显示
            if PixelType_Gvsp_RGB8_Packed == obj_cam_operation.st_frame_info.enPixelType:
                numArray = CameraOperation.Color_numpy(obj_cam_operation,buf_cache,obj_cam_operation.st_frame_info.nWidth,obj_cam_operation.st_frame_info.nHeight)

            #如果是彩色且非RGB则转为RGB后显示
            else:
                nConvertSize = obj_cam_operation.st_frame_info.nWidth * obj_cam_operation.st_frame_info.nHeight * 3
                stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
                stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
                stConvertParam.nDstBufferSize = nConvertSize
                time_start=time.time()
                ret = obj_cam_operation.obj_cam.MV_CC_ConvertPixelType(stConvertParam)
                time_end=time.time()
                print('MV_CC_ConvertPixelType:',time_end - time_start) 
                if ret != 0:
                    print('show error','convert pixel fail! ret = '+obj_cam_operation.To_hex_str(ret))
                    continue
                cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
                numArray = CameraOperation.Color_numpy(obj_cam_operation,img_buff,obj_cam_operation.st_frame_info.nWidth,obj_cam_operation.st_frame_info.nHeight)

            current_image = Image.fromarray(numArray).resize((800, 600), Image.ANTIALIAS)
            print(type(numArray))
            print(numArray.shape)
            print(numArray.dtype)

            picc=cv.imread("C:\\Users\\QXF\\Desktop\\mer\\mm.PNG",cv2.IMREAD_GRAYSCALE)
            im=Image.fromarray(picc)
            picc2=current_image.toqpixmap()


            #cv.imshow("sdadas",numArray)
            #print(numArray.shape)
            #cv.imshow("fsd",imgp)
            #imgs=np.asarray(current_image)

            #current_image = cv.resize(numArray,(450,300))
            #print(numArray)
            #cv.imshow("fsd",imgs)
            #piccc=ImageQt.toqpixmap(current_image)
            self.updatepic.emit(picc2)

            nRet = obj_cam_operation.obj_cam.MV_CC_FreeImageBuffer(stOutFrame)
            if obj_cam_operation.b_exit == True:
                if img_buff is not None:
                    del img_buff
                if buf_cache is not None:
                    del buf_cache
                break
        sys.exit(-1)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #self.ui.lbPic.setPixmap("C:\\Users\\QXF\\Desktop\\mer\\mm.PNG")
        
        self.th=Work_thread(self)
        self.th.updatepic.connect(self.setpic)
        #self.ps=PicSignal()
        #self.ps.show_pic.connect()
        
        self.ui.pbEnumDev.clicked.connect(self.enum_devices)
        self.ui.pbConnectCam.clicked.connect(self.open_device)
        self.ui.pbCloseCam.clicked.connect(self.close_device)
        self.ui.pbStartGrab.clicked.connect(self.start)
        self.ui.pbStopGrab.clicked.connect(self.stopgrab)
        self.ui.pbGrabSingle.clicked.connect(self.trigger_once)
        self.ui.pbTrain.clicked.connect(self.imgtest)
        self.ui.pbMatch.clicked.connect(self.showsinglecolor)
        #ui.pbSelectROI.clicked.connect()
        #ui.pbOCR.clicked.connect()
    
    @Slot()
    def start(self):
        self.th.start()

    @Slot(QPixmap)
    def setpic(self, pic):
        self.ui.lbPic.setPixmap(pic)

    
    @Slot()
    def stopgrab(self):
        self.th.terminate()

    @Slot()
    def imgtest(self):
        picc=cv.imread("C:\\Users\\QXF\\Desktop\\mer\\mm.PNG")
        cv.imshow("sdss",picc)
        print(type(picc))
        print(picc.shape)
        print(picc.dtype)
    @Slot()
    def showsinglecolor(self):
        img=np.zeros((450,300,3),dtype='uint8')
        img[:,:,0]=200
        cv.imshow("sdfsd",img)

    def showmat(self):
        print("called")

    #ch:枚举相机 | en:enum devices
    def enum_devices(self):
        global deviceList
        global obj_cam_operation
        deviceList = MV_CC_DEVICE_INFO_LIST()
        tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
        if ret != 0:
            print("enum devices fail! ret = ")

        if deviceList.nDeviceNum == 0:
            print("find no device!")

        print ("Find %d devices!" % deviceList.nDeviceNum)

        devList = []
        for i in range(0, deviceList.nDeviceNum):
            mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                print ("\ngige device: [%d]" % i)
                chUserDefinedName = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chUserDefinedName:
                    if 0 == per:
                        break
                    chUserDefinedName = chUserDefinedName + chr(per)
                print ("device model name: %s" % chUserDefinedName)

                nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
                print ("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
                devList.append("["+str(i)+"]GigE: "+ chUserDefinedName +"("+ str(nip1)+"."+str(nip2)+"."+str(nip3)+"."+str(nip4) +")")
            elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                print ("\nu3v device: [%d]" % i)
                chUserDefinedName = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chUserDefinedName:
                    if per == 0:
                        break
                    chUserDefinedName = chUserDefinedName + chr(per)
                print ("device model name: %s" % chUserDefinedName)

                strSerialNumber = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    strSerialNumber = strSerialNumber + chr(per)
                print ("user serial number: %s" % strSerialNumber)
                devList.append("["+str(i)+"]USB: "+ chUserDefinedName +"(" + str(strSerialNumber) + ")")

    
    
    #ch:打开相机 | en:open device
    def open_device(self):
        global deviceList
        global nSelCamIndex
        global obj_cam_operation
        global b_is_run
        if True == b_is_run:
            print("Camera is Running!")
            return
        obj_cam_operation = CameraOperation(cam,deviceList,nSelCamIndex)
        ret = obj_cam_operation.Open_device()
        if  0!= ret:
            b_is_run = False
        else:
            obj_cam_operation.Set_trigger_mode("triggermode")
            b_is_run = True
        obj_cam_operation.obj_cam.MV_CC_StartGrabbing()

    # ch:开始取流 | en:Start grab image
    def start_grabbing(self):
        global obj_cam_operation
        obj_cam_operation.Start_grabbing(MainWindow,panel)

    # ch:停止取流 | en:Stop grab image
    def stop_grabbing(self):
        global obj_cam_operation
        obj_cam_operation.Stop_grabbing()    

    # ch:关闭设备 | Close device   
    def close_device(self):
        global b_is_run
        global obj_cam_operation
        obj_cam_operation.Close_device()
        b_is_run = False 
        

    
    #ch:设置触发模式 | en:set trigger mode
    def set_triggermode(self):
        global obj_cam_operation
        
        obj_cam_operation.Set_trigger_mode("triggermode")
        

    #ch:设置触发命令 | en:set trigger software
    def trigger_once(self):
        
        global obj_cam_operation
        obj_cam_operation.Trigger_once(1)
        
    
    #ch:保存bmp图片 | en:save bmp image
    def bmp_save(self):
        global obj_cam_operation
        obj_cam_operation.b_save_bmp = True

    #ch:保存jpg图片 | en:save jpg image
    def jpg_save(self):
        global obj_cam_operation
        obj_cam_operation.b_save_jpg = True



if __name__ == '__main__':

    global deviceList 
    deviceList = MV_CC_DEVICE_INFO_LIST()
    global tlayerType
    tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
    global cam
    cam = MvCamera()
    global nSelCamIndex
    nSelCamIndex = 0
    global obj_cam_operation
    obj_cam_operation = 0
    global b_is_run
    b_is_run = False    

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

