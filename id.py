import Tkinter as tk
import tkMessageBox

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
        self._geom='200x200+0+0'
        #master.overrideredirect(1)
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        master.wm_state('normal')
        cmd=master.register(self.check)
        self.e=tk.Entry(master,bd=2,justify=tk.CENTER,width=17,textvariable=self.cid,validate='key',validatecommand=(cmd,'%S','%P'))
        self.e.pack()
        self.e.bind("<Key>",self.senddata)
        self.e.focus_set()
        
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
        
root=tk.Tk()
app=FullScreenApp(root)
root.mainloop()
