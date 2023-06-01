import socket
import select
import sys
import msvcrt
from input_mode import Text2speech, Speech2text, ChatGPT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))

user_name, input_content= None, None
text_flag = 'Text'

while True:
    read, write, fail = select.select((s,), (), (), 1)
    if msvcrt.kbhit():  read.append(sys.stdin)

    for desc in read:
        if desc == s:
            data = s.recv(4096)
            print(f'{data.decode()}')   # 메시지 출력

            if user_name is None:    # 첫 접속
                user_name = data.decode()
                s.send(f'**{user_name} is connected!**'.encode())
                print(f'너의 이름은 -> {data.decode()} [1.텍스트모드(/텍스트) 2.음성모드(/음성) 3.GPT모드(/GPT)]')

        else:
            if text_flag == 'Text': # 입력을 텍스트로 받는 경우
                msg = desc.readline()
                msg = msg.replace('\n', '')
                if msg == '/음성':  # msg가 '/음성'인 경우 음성으로 이동
                    text_flag = 'Voice'
                    continue
                elif msg =='/GPT':  # msg가 '/GPT'인 경우 GPT로 이동
                    text_flag = 'GPT'
                    continue

            elif text_flag == 'Voice':  # 입력을 음성으로 받는 경우
                msg = Speech2text()
                if msg =='/텍스트':  # msg가 '/텍스트'인 경우 텍스트로 이동
                    text_flag = 'Text'
                    continue
                elif msg =='/GPT':  # msg가 '/GPT'인 경우 GPT로 이동
                    text_flag = 'GPT'
                    continue

            elif text_flag == 'GPT': # GPT 질문으로 넘어갈 경우
                msg = ChatGPT()
                if msg == '/텍스트': # msg가 '/텍스트'인 경우 텍스트로 이동
                    text_flag = 'Text'
                    continue
                elif msg == '/음성':  # msg가 '/음성'인 경우 음성으로 이동
                    text_flag = 'Voice'
                    continue
                elif msg == '':   # GPT의 답변을 전송하지 않았던 경우 텍스트로 이동
                    text_flag = 'Text'
                    continue
                        
            s.send(f'{user_name} {msg}'.encode())
            Text2speech(user_name, msg)
            continue
