from tkinter import *
class UserDialog:
    _Ip = ''
    _port = 0
    _nickname = ''
    def __init__(self):
        pass


    @classmethod
    def getUserInputIp(cls):

        def getUserIpAndPort():
            cls._Ip = e1.get()
            cls._port = int(e2.get())
            ClientWindow.destroy()

        ClientWindow = Tk()

        Label(ClientWindow,text='请输入IP').grid(row=0)
        Label(ClientWindow,text='Ip').grid(row=1)
        Label(ClientWindow,text='Port').grid(row=2)

        e1 = Entry(ClientWindow)
        e1.grid(row=1,column = 1)
        e2 = Entry(ClientWindow)
        e2.grid(row=2,column = 1)

        button = Button(ClientWindow)
        button.config(text='ok',command = getUserIpAndPort)
        button.grid(row=3,column=0)

        ClientWindow.mainloop()

    @classmethod
    def getUserNickName(cls):
        def getUserNickNameInner():
            cls._nickname = e1.get()
            ClientWindow.destroy()

        ClientWindow = Tk()

        Label(ClientWindow, text='请输入昵称').grid(row=0)
        Label(ClientWindow, text='昵称').grid(row=1)

        e1 = Entry(ClientWindow)
        e1.grid(row=1, column=1)

        button = Button(ClientWindow)
        button.config(text='ok', command=getUserNickNameInner)
        button.grid(row=2, column=0)

        ClientWindow.mainloop()
if __name__ == '__main__':
    UserDialog.getUserInputIp()
    print(UserDialog._Ip)
    print(UserDialog._port)