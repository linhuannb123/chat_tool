#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import sys
import os
import threading
import hashlib
import json
import user_reg_login


# UDP打洞
# 定长包头(15B) + 变长聊天消息(昵称:聊天内容)

def client_chat(sock_conn, client_addr,user_name):
    try:
        while True:
                msg_len_data = sock_conn.recv(15)
                if not msg_len_data:
                    break

                msg_len = int(msg_len_data.decode().rstrip())
                recv_size = 0
                msg_content_data = b""
                while recv_size < msg_len:
                    tmp_data = sock_conn.recv(msg_len - recv_size)
                    if not tmp_data:
                        break
                    msg_content_data += tmp_data
                    recv_size += len(tmp_data)
                else:
                    # 发送给其他所有在线的客户端
                    for sock_tmp, tmp_addr in client_socks: 
                        if sock_tmp is not sock_conn:
                            try:
                                sock_tmp.send(msg_len_data)
                                sock_tmp.send(msg_content_data)
                            except:
                                client_socks.remove((sock_tmp, tmp_addr))
                                sock_tmp.close()
                    continue
                break
    finally:
            client_socks.remove((sock_conn, client_addr))
            sock_conn.close()


def user_service_thread(sock_conn, client_addr):
    try:
        data_len = sock_conn.recv(15).decode().rstrip()
        if len(data_len) > 0:
            data_len = int(data_len)

            recv_size = 0
            json_data = b""
            while recv_size < data_len:
                tmp = sock_conn.recv(data_len - recv_size)
                if tmp == 0:
                    break
                json_data += tmp
                recv_size += len(tmp)
            
            json_data = json_data.decode()
            req = json.loads(json_data)

            if req["op"] == 1:
                # 登录校验
                rsp = {"op": 1, "error_code": 0}

                if user_reg_login.check_uname_pwd(req["args"]["uname"], req["args"]["passwd"]):
                    rsp["error_code"] = 1
                
                header_data = json.dumps(rsp).encode()
                data_len = "{:<15}".format(len(header_data)).encode()
                sock_conn.send(data_len)
                sock_conn.send(header_data)

                if not rsp["error_code"]:
                    print("用户%s登录成功，" % req["args"]["uname"])
                    client_chat(sock_conn, client_addr,req["args"]["uname"])

            elif req["op"] == 2:
                # 用户注册
                rsp = {"op": 2, "error_code": 0}
                if not user_reg_login.user_reg(req["args"]["uname"], req["args"]["passwd"], req["args"]["phone"], req["args"]["email"]):
                    # 注册失败
                    rsp["error_code"] = 1
                else:
                    print("用户%s注册成功！" % req["args"]["uname"])

                rsp = json.dumps(rsp).encode()
                data_len = "{:<15}".format(len(rsp)).encode()
                sock_conn.send(data_len)
                sock_conn.send(rsp)            

            elif req["op"] == 3:
                # 校验用户名是否存在
                rsp = {"op": 3, "error_code": 0}

                ret = user_reg_login.check_user_name(req["args"]["uname"])
                if ret == 2:
                    rsp["error_code"] = 1
                    print("校验用户名%s失败！" % req["args"]["uname"])
                else:
                    print("校验用户名%s成功！" % req["args"]["uname"])
                
                rsp = json.dumps(rsp).encode()
                data_len = "{:<15}".format(len(rsp)).encode()
                sock_conn.send(data_len)
                sock_conn.send(rsp)            
    finally:
        print("客户端(%s:%s)断开连接！" % client_addr)
        sock_conn.close()



sock_listen = socket.socket()
sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_listen.bind(("0.0.0.0", 9999))
sock_listen.listen(5)

client_socks = []

while True:
    sock_conn, client_addr = sock_listen.accept()
    client_socks.append((sock_conn, client_addr))
    threading.Thread(target=user_service_thread, args=(sock_conn, client_addr)).start()



