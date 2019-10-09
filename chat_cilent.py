import socket,threading
import tkinter as tk
import tkinter.messagebox
import json,os,sys,re,hashlib
import user_reg_login


def get_passwd_md5(passwd):
    m = hashlib.md5()  
    m.update(passwd.encode())    
    return m.hexdigest().upper()

def user_check(uname):
    '''
    用户名校验
    函数功能：检验用户名是否存在
    返回值：用户名存在返回1，不存在返回0，用户名不合法返回2
    '''
    global sock
    sock = socket.socket()  #创建套接字
    sock.connect((conf["ip地址"], conf["端口号"]))  #与目标服务器建立连接
    if not re.match("^[a-zA-Z0-9_]{6,15}$", uname):  #检验是否合法
        return 2

    a_rsp = {"op":3,"args":{"uname":uname}}
    a_rsp = json.dumps(a_rsp).encode()
    data_len = "{:<15}".format(len(a_rsp)).encode()
    sock.send(data_len)
    sock.send(a_rsp)

    len_rsq=sock.recv(15).decode().rstrip()
    rsq_msg = sock.recv(int(len_rsq)).decode()
    rsq_msg = json.loads(rsq_msg)
    sock.close() 

    if rsq_msg["error_code"] == 0:
  
        return 0    #用户名不存在
    else:
        return 1    #用户名存在
    

def reg_check(uname,passwd,phone,email):
    '''
    函数功能：用户注册验证函数
    参数描述：
        uname 用户名
        passwd 密码
        返回值，注册成功返回0，注册失败返回1
    '''
    global sock
    sock = socket.socket()  #创建套接字
    sock.connect((conf["ip地址"], conf["端口号"]))  #与目标服务器建立连接
    passwd = get_passwd_md5(passwd)
    a_rsp = {"op":2,"args":{"uname":uname,"passwd":passwd,"phone":phone,"email":email}}
    a_rsp = json.dumps(a_rsp).encode()
    data_len = "{:<15}".format(len(a_rsp)).encode()
    sock.send(data_len)
    sock.send(a_rsp)

    len_rsq=sock.recv(15).decode().rstrip()
    rsq_msg = sock.recv(int(len_rsq)) 
    rsq_msg = json.loads(rsq_msg)
    sock.close()
    if rsq_msg["error_code"] == 0:
        return 0   #注册成功
    else:
        return 1   #注册失败s

def login_check(uname,passwd):
    '''
    函数功能：用户登录验证函数
    参数描述：
        uname 用户名
        passwd 密码
        返回值，登录成功返回0，登录失败返回1
    '''

    global sock
    sock = socket.socket()  #创建套接字
    sock.connect((conf["ip地址"], conf["端口号"]))  #与目标服务器建立连接
    passwd = get_passwd_md5(passwd)         
    a_rsp = {"op":1,"args":{"uname":uname,"passwd":passwd}}
    a_rsp = json.dumps(a_rsp).encode()
    data_len = "{:<15}".format(len(a_rsp)).encode()


    sock.send(data_len)
    sock.send(a_rsp)

    len_rsq=sock.recv(15).decode().rstrip()
    
  
    rsq_msg = sock.recv(int(len_rsq)).decode()

    rsq_msg = json.loads(rsq_msg)
    
    if rsq_msg["error_code"] == 0:
        return 0   #登录成功
    else: 
        return 1   #登录失败


def on_send_msg():
    nick = json.load(open("user_info.json",encoding="utf-8")) #加载配置信息
    nick_name = nick["nick_name"]
    chat_msg = chat_msg_box.get(1.0,"end")
    if chat_msg == "\n":
        return
    chat_data = (nick_name + ":" + chat_msg).encode()
    data_len = "{:<15}".format(len(chat_data)).encode()
    try:
        sock.send(data_len)
        sock.send(chat_data)

    except:
        tkinter.messagebox.showerror("温馨提示","发送失败，请检查网络")
    else:
        chat_msg_box.delete(1.0,"end")
        chat_record_box.configure(state=tk.NORMAL)
        chat_record_box.insert("end",chat_data.decode()+"\n")
        chat_record_box.configure(state=tk.DISABLED)


def recv_chat_msg():
    global sock

    while True:
        try:
            while True:
                    msg_len_data = sock.recv(15)
                    if not msg_len_data:
                        break

                    msg_len = int(msg_len_data.decode().rstrip())
                    recv_size = 0
                    msg_content_data = b""
                    while recv_size < msg_len:
                        tmp_data = sock.recv(msg_len - recv_size)
                        if not tmp_data:
                            break
                        msg_content_data += tmp_data
                        recv_size += len(tmp_data)
                    else:
                        # 显示
                        chat_record_box.configure(state=tk.NORMAL)
                        chat_record_box.insert("end", msg_content_data.decode() + "\n")
                        chat_record_box.configure(state=tk.DISABLED)
                        continue
                    break
        finally:
                sock.close()
                sock = socket.socket()
                sock.connect((conf["ip地址"],conf["端口号"]))

def chat_main():
    mainWnd = tk.Tk()
    mainWnd.title("P1901专属聊天室")

    global chat_record_box
    chat_record_box = tk.Text(mainWnd)
    chat_record_box.configure(state=tk.DISABLED)
    chat_record_box.pack(padx=10,pady=10)

    global chat_msg_box
    chat_msg_box = tk.Text(mainWnd)
    chat_msg_box.configure(width=65,height=5)
    chat_msg_box.pack(side=tk.LEFT,padx=10,pady=10)

    
    send_msg_btn = tk.Button(mainWnd,text="发送",command=on_send_msg)
    send_msg_btn.pack(side=tk.RIGHT,padx=10,pady=10,ipadx=15,ipady=15)

    threading.Thread(target=recv_chat_msg).start()

    mainWnd.mainloop()
        


conf = json.load(open("client_conf.json",encoding="utf-8")) #加载配置信息
sock = socket.socket()
sock.connect((conf["ip地址"],conf["端口号"]))

def reg_main():
    while True:
        user_name = input("请输入用户名（只能包含英文字母、数字或下划线，最短6位，最长15位）：")

        ret = user_check(user_name)
        if ret == 1:
            print("用户名已存在，请重新输入！")
        elif ret == 2:
            print("用户名格式错误，请重新输入！")
        else:
            break

    while True:
        while True:
            password = input("请输入密码：（只能包含英文字母、数字或下划线，最短6位，最长15位）：")

            ret = user_reg_login.check_password(password)

            if ret == 0:
                break
            else:
                print("密码格式错误，请重新输入！")

        confirm_pass = input("请再次输入密码：")

        if password == confirm_pass:
            break
        else:
            print("两次输入的密码不一致，请重新输入！")

    while True:
        phone = input("请输入手机号：")

        if user_reg_login.check_phone(phone):
            print("手机号输入错误，请重新输入！")
        else:
            break

    # verify_code = user_reg_login.send_sms_code(phone)

    # if verify_code:
    #     print("短信验证码已发送！")
    # else:
    #     print("短信验证码发送失败，请检查网络连接或联系软件开发商！")
    #     sys.exit(1)

    # while True:
    #     verify_code2 = input("请输入短信验证码：")

    #     if verify_code2 != verify_code:
    #         print("短信验证码输入错误，请重新输入！")
    #     else:
    #         break


    while True:
        email = input("请输入邮箱：")

        if user_reg_login.check_email(email):
            print("邮箱输入错误，请重新输入！")
        else:
            break

    # email_verify_code = user_reg_login.send_email_code(email)

    # if email_verify_code:
    #     print("邮箱验证码已发送！")
    # else:
    #     print("邮箱验证码发送失败，请检查网络连接或联系软件开发商！")
    #     sys.exit(1)

    # while True:
    #     email_verify_code2 = input("请输入邮箱验证码：")

    #     if email_verify_code2 != email_verify_code:
    #         print("短信验证码输入错误，请重新输入！")
    #     else:
    #         break
    # 校验邮箱的合法性
    # ...
    if reg_check(user_name,password,phone,email) == 0:
        return 0
    else:
        return 1
    



def login_main():
    '''
    函数功能：用户登录验证
    函数参数：无
    返回值：登录验证成功返回0，失败返回1
    '''
    while True:
        user_name = input("\n用户名：")
        ret = user_check(user_name)
        if ret == 0:
            print("用户名不存在，请重新输入！")
        elif ret == 2:
            print("用户名格式错误，请重新输入！")
        else:
            break
    #user_name = input("\n用户名：")    
    while True:
        password = input("\n密码：")
        ret = user_reg_login.check_password(password)
        if ret == 0:
            break
        else:
            print("密码格式错误，请重新输入！")

    if login_check(user_name,password) == 0:
        print("登录成功")
        return 0
    else:
        print("登录失败")
        return 1

def main():
    while True:
        print("请选择功能:")
        print("1.登录")
        print("2.注册")
        print("3.退出")
        com = input(">")
        if com == "1":
            if login_main() == 0:
                chat_main()
            else: 
                print("登录失败!")
            break

        elif com == "2":
            if reg_main() == 0 :
                continue
                
        elif com == "3":
       
            sys.exit()

if __name__ == "__main__":

    main()

sock.close()