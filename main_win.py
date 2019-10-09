import tkinter 
import tkinter.messagebox
import sys
import json
import chat_cilent





def login_win():

    def login():
        username = username_input.get()
        password = password_input.get()
        
        username_input.delete(0,"end")
        password_input.delete(0,"end")

      
        nicks = json.load(open("user_info.json",encoding="utf-8"))
        nicks["nick_name"] = username

        with open("user_info.json","w") as w:
            w.write(json.dumps(nicks))


        
        if chat_cilent.login_check(username,password) == 0:
            top.destroy()
            chat_cilent.chat_main()
            sys.exit()
            return 0
        else:
            tkinter.messagebox.showerror("温馨提示","登录失败，请检查用户名或密码")
            return 1

    def reg():
        

        def commit():
            username = username_reg_input.get()
            password = password_reg_input.get()
            phone = phone_reg_input.get()
            email = email_reg_input.get()

            username_reg_input.delete(0,"end")
            password_reg_input.delete(0,"end")
            phone_reg_input.delete(0,"end")
            email_reg_input.delete(0,"end")

            if chat_cilent.reg_check(username,password,phone,email) == 0:
                tkinter.messagebox.showinfo("温馨提示","恭喜你注册成功")
                
            else:
                tkinter.messagebox.showerror("温馨提示","注册失败")
                return 1

        def black():
            reg_win.quit()


        reg_win = tkinter.Tk()
        reg_win.title("注册")

        username_reg_lable = tkinter.Label(reg_win,text = '用户名:',font = ('楷体','18'))
        username_reg_lable.grid(row = 0,column = 0)

        password_reg_label = tkinter.Label(reg_win,text = '密码:',font = ('楷体','18'))#集合为另一种形式的字典
        password_reg_label .grid(row = 1 ,column = 0)

        phone_reg_label = tkinter.Label(reg_win,text = '电话:',font = ('楷体','18'))#集合为另一种形式的字典
        phone_reg_label .grid(row = 2 ,column = 0)

        email_reg_label = tkinter.Label(reg_win,text = '邮箱:',font = ('楷体','18'))#集合为另一种形式的字典
        email_reg_label .grid(row = 3 ,column = 0)

        
        username_reg_input = tkinter.Entry(reg_win,font = ('楷体','18'))
        username_reg_input.grid(row = 0,column = 1)
        

        password_reg_input = tkinter.Entry(reg_win,font = ('楷体','18'),show = '*')
        password_reg_input.grid(row = 1,column = 1)

        phone_reg_input = tkinter.Entry(reg_win,font = ('楷体','18'))
        phone_reg_input.grid(row = 2,column = 1)
        

        email_reg_input = tkinter.Entry(reg_win,font = ('楷体','18'))
        email_reg_input.grid(row = 3,column = 1)
        

        login_button = tkinter.Button(reg_win,text = '确定',font = ('楷体','18'),command = commit)
        login_button.grid(row = 4,column = 0,padx = 50,pady = 10)

        reg_button = tkinter.Button(reg_win,text = '返回',font = ('楷体','18'),command = black)
        reg_button.grid(row = 4,column = 1,padx = 50,pady = 10)


        


    top = tkinter.Tk()
    top.title("登录")

    username_lable = tkinter.Label(top,text = '用户名:',font = ('楷体','18'))
    username_lable.grid(row = 0,column = 0)

    password_label = tkinter.Label(top,text = '密码:',font = ('楷体','18'))#集合为另一种形式的字典
    password_label .grid(row = 1 ,column = 0)

    v = tkinter.StringVar()
    username_input = tkinter.Entry(top,font = ('楷体','18'),textvariable = v,validate = 'focusout',)
    username_input.grid(row = 0,column = 1)
    username_input.focus_force()

    password_input = tkinter.Entry(top,font = ('楷体','18'),show = '*')
    password_input.grid(row = 1,column = 1)

    login_button = tkinter.Button(top,text = '登陆',font = ('楷体','18'),command = login)
    login_button.grid(row = 2,column = 0,padx = 50,pady = 10)

    reg_button = tkinter.Button(top,text = '注册',font = ('楷体','18'),command = reg)
    reg_button.grid(row = 2,column = 1,padx = 50,pady = 10)


    info_lable = tkinter.Label(top,text = '帅帅的wwt',font = ('华文新魏','16'),relief = 'ridge',width = 30)
    info_lable.grid(row = 3,column = 0,padx = 10,pady = 10,columnspan = 2,sticky = 's')

    top.mainloop()


login_win()

