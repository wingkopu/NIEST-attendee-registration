# -*- coding: utf-8 -*-
import Tkinter as tk
import tkMessageBox,sys
from time import sleep
from readthaiid import *

class FullScreenApp(object):

    def check(self,changed,after):
        group=['1','2','3','4','5','6','7','8','9','0']
        if changed not in group:
            return False
        current=self.e.get()
        
        if len(after)>13:
            return False
        
        return True
    
    def __init__(self, master, **kwargs):
        self.master=master
        self.cid=tk.StringVar(master)
        pad=3
        self._geom='320x240+0+0'
        #master.overrideredirect(1)
        #master.geometry("{0}x{1}+0+0".format(
        #    master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.geometry("{0}x{1}+0+0".format(
            320-pad, 240-pad))
        master.bind('<Escape>',self.toggle_geom)
        master.wm_state('normal')
        cmd=master.register(self.check)
        self.e=tk.Entry(master,bd=2,font=("Helvetica", 22),justify=tk.CENTER,width=17,textvariable=self.cid,validate='key',validatecommand=(cmd,'%S','%P'))
        self.e.pack()
        self.e.bind("<Key>",self.senddata)
        self.e.place(x=20,y=50)

        self.notice=tk.StringVar(master)
        self.l=tk.Label(master,text="",font=("Helvetica", 10),justify=tk.CENTER,textvariable=self.notice)
        self.l.pack()
        self.l.place(x=55,y=100)

        reload(sys)
        sys.setdefaultencoding("utf-8")
        self.retry=0
        
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

    def senddata(self,event):
        #tkMessageBox.showinfo("",event.keycode)
        if event.keycode==104:
            if len(self.cid.get())==13:
                print self.cid.get()
                quit()
            else:
                return False

    def readfromcard(self):
        if self.retry<=3:
            self.notice.set('โปรดเสียบบัตรประจำตัวประชาชน')
            sleep(2)
            self.master.update()
            try:
                scard=thaiNationIDCard()
                self.notice.set("กำลังรอข้อมูล")
                self.master.update()
                self.cid.set(scard.getCitizenID())
            except:
                self.retry+=1
                self.notice.set("อ่านข้อมูลไม่สำเร็จ")
                self.master.update()
                self.master.after(1000,self.readfromcard())
                return
            print self.cid.get()
            self.notice.set('กด Enter เพื่อทำงานต่อ')
        else:
            self.notice.set('โปรดใช้แป้นพิมพ์ตัวเลข\nในการกรอกข้อมูลรหัสประจำตัวประชาชน')

        
root=tk.Tk()
app=FullScreenApp(root)
root.after(1000,app.readfromcard())
root.mainloop()
