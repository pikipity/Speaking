# encoding=utf-8
import Tkinter
import ttk
import threading
import Queue
import tkMessageBox
import time
import sys
import paramiko
import base64
import webbrowser
import os

Version="1.0"

############### Log in Window #################

def login():
    global loginwindow
    loginwindow=Tkinter.Toplevel()

    usrnameLabel=Tkinter.Label(loginwindow,text="Wang Ze Student ID: ",\
                               font="Times 15 bold")
    usrnameLabel.grid(row=0,column=0)
    global usrnameInput
    usrnameInput=Tkinter.Entry(loginwindow,font="Times 15 bold")
    usrnameInput.grid(row=0,column=1)
    usrnameInput.focus()
    usrnameInput.bind("<Return>",getnamepass)

    passwordLabel=Tkinter.Label(loginwindow,text="Wang Ze password: ",\
                           font="Times 15 bold")
    passwordLabel.grid(row=1,column=0)
    global passwordInput
    passwordInput=Tkinter.Entry(loginwindow,font="Times 15 bold",show="*")
    passwordInput.grid(row=1,column=1)
    passwordInput.bind("<Return>",getnamepass)

    EnterButton=Tkinter.Button(loginwindow,text="I know, I know",width=33,\
                               font="Times 15 bold",\
                               command=getnamepass)
    EnterButton.grid(row=2,column=0,columnspan=2)

    State.set("Please Login using Wang Ze's count")

def getnamepass(event=None):
    usrname=usrnameInput.get()
    password=passwordInput.get()
    usr.get()
    usr.get()
    usr.put(usrname)
    usr.put(password)
    if usrname == "db02906" and base64.encodestring(password) == 'ZGJnaGRiNjUwODAw\n':
        loginwindow.destroy()
        LoginThreading=threading.Thread(target=LoginThread)
        LoginThreading.daemon=True
        LoginThreading.start()
    else:
        tkMessageBox.showwarning("输入错误","你不知道我的学生证号和密码么？")
        usrnameInput.focus()

def LoginThread():
    usrname=usr.get()
    password=usr.get()
    usr.put(usrname)
    usr.put(password)
    global ssh
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    State.set("开始尝试连接到SSH服务器")
    N=0
    while N<10:
        try:
            N=N+1
            State.set("Try to connect SSH serve %s" % N)
            ssh.connect("umacux4.wkg1.umac.mo",22,usrname,password,timeout=5)
        except:
            pass
        else:
            break
    global ssh1
    ssh1=paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    State.set("开始尝试连接到SSH服务器")
    N=0
    while N<10:
        try:
            N=N+1
            State.set("Try to connect SSH serve %s" % N)
            ssh1.connect("umacux4.wkg1.umac.mo",22,usrname,password,timeout=5)
        except:
            pass
        else:
            break
    if (N<10):
        NowSend()
        Rotor=1
        while Rotor:
            try:
                State.set("开始接收数据")
                FileName=time.strftime("%Y-%m-%d",time.localtime(time.time()))
                IN,OUT,ADDR=ssh.exec_command("cat ~/speaking/"+FileName)
            except:
                State.set("连接错误，没能连接上网络，请重试。")
                usrname=usr.get()
                password=usr.get()
                usr.put("None")
                usr.put("None")
                Rotor=0
            else:
                State.set("接收成功")
                if OUT.readlines==[]:
                    time.sleep(1)
                else:
                    ReadText=OUT.readlines()
                    ReadTextpast=ReadQueue.get()
                    if ReadText <> ReadTextpast:
                        ReadQueue.put(ReadText)
                        MainText.delete("1.0","end")
                        M=0
                        for x in ReadText:
                            M=M+1
                            if(M==len(ReadText)):
                                x=x[0:len(x)-1]
                            MainText.insert("end",x)
                        MainText.yview("moveto",1.0)
                        time.sleep(1)
                    else:
                        ReadQueue.put(ReadTextpast)
                        time.sleep(1)
    else:
        State.set("连接错误，没能连接上网络，请重试。")
        usrname=usr.get()
        password=usr.get()
        usr.put("None")
        usr.put("None")
    
        
############### send to login 副程序 ######################

def Sending(event=None):
    usrname=usr.get()
    password=usr.get()
    usr.put(usrname)
    usr.put(password)
    if usrname <> "db02906" or base64.encodestring(password) <> 'ZGJnaGRiNjUwODAw\n':
        login()
    else:
        SendingNowThreading=threading.Thread(target=NowSend)
        SendingNowThreading.start()

############### Send 副程序 ##############################
def NowSend():
    TextSend=InText.get()
    title="\""+Name+" say "+time.strftime("%Y-%m-%d %A %H : %M : %S",time.localtime(time.time()))+"\""
    InputText=""""---> """+TextSend.replace("!","\!").encode("utf-8")+"""\""""
    try:
        State.set("开始发送数据")
        FileName=time.strftime("%Y-%m-%d",time.localtime(time.time()))
        ssh1.exec_command("echo %s >> ~/speaking/%s;echo %s >> ~/speaking/%s" % (title,FileName,InputText,FileName))
    except:
        InText.delete("0","end")
        State.set("连接错误，没能连接上网络，请重试。")
        usrname=usr.get()
        password=usr.get()
        usr.put("None")
        usr.put("None")
    else:
        State.set("发送成功")
        InText.delete("0","end")

############################################
def QuitFunction():
    root.quit()
    root.destroy()

def AboutFunction():
    AboutWin=Tkinter.Toplevel()
    AboutWin.title("Speaking About")
    TitleLabel=Tkinter.Label(AboutWin,text="Speaking",font="Times 30 bold",fg="#FF1493")
    TitleLabel.pack()
    VersionLabel=Tkinter.Label(AboutWin,text="Version "+Version,\
                               font="Times 15 bold")
    VersionLabel.pack()
    WriteLabel=Tkinter.Label(AboutWin,text="Writed by pikipity",\
                             font="Times 17 bold",fg="#008FFF")
    WriteLabel.pack()
    EmailLabel=Tkinter.Label(AboutWin,text="pikipity's emal: pikipityw@gmail.com",\
                            font="Times 17 bold",fg="#008FFF")
    EmailLabel.pack()
    BlogLabel=Tkinter.Label(AboutWin,text="pikipity's blog: pikipity.github.io",\
                            font="Times 17 bold",fg="#008FFF",cursor="hand2")
    BlogLabel.bind("<Button-1>",OpenBlog)
    BlogLabel.pack()
def OpenBlog(event="None"):
    webbrowser.open("pikipity.github.io")

def HelpFunction():
    #os.system("notepad "+ProgramPath+"Help")
    HelpWin=Tkinter.Toplevel()
    HelpWin.title('Help')
    fp=open(ProgramPath+"Help")
    HelpMain=fp.readlines()
    fp.close()
    HelpText=Tkinter.Text(HelpWin)
    HelpText.pack()
    for x in HelpMain:
        HelpText.insert('end',x.decode('gb2312'))

############### 主程序 #######################

ProgramPath=sys.argv[0][0:sys.argv[0].rfind('\\')+1]
Name="Wang Ze"
global usr
usr=Queue.Queue()
usr.put("None")
usr.put("None")

ReadQueue=Queue.Queue()
ReadQueue.put("None")
        
root=Tkinter.Tk()

Menubar=Tkinter.Menu(root)

filemenu=Tkinter.Menu(Menubar,tearoff=0)
filemenu.add_command(label="Download and Open History")
filemenu.add_command(label="Quit",command=QuitFunction)
Menubar.add_cascade(label="File",menu=filemenu)

Helpmenu=Tkinter.Menu(Menubar,tearoff=0)
Helpmenu.add_command(label="Help",command=HelpFunction)
Helpmenu.add_command(label="About",command=AboutFunction)
Menubar.add_cascade(label="Help",menu=Helpmenu)

root.config(menu=Menubar)

MainText=Tkinter.Text(root,width=60,height=20,border=5,font="Times 15 bold")
MainText.grid(row=1,column=0,columnspan=2)

InText=Tkinter.Entry(root,width=55,border=1,font="Times 15 bold")
InText.grid(row=2,column=0)
InText.bind("<Return>",Sending)
InText.focus()

SendButton=Tkinter.Button(root,width=6,height=1,text="Go",font="Times 12 bold",\
                          command=Sending)
SendButton.grid(row=2,column=1)

State=Tkinter.StringVar()
StateLabel=Tkinter.Label(root,width=87,textvariable=State,\
                         justify="left",\
                         font="Times 10 bold",\
                         anchor="w")
StateLabel.grid(row=3,column=0,columnspan=2)
State.set("Love You. Enjoy it")

root.mainloop()
