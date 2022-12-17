# coding=utf-8
from aip import AipSpeech
import tkinter as tk
from PIL import ImageTk
import easygui
from tkinter import filedialog
import pygame

window = tk.Tk()  # 注册窗体
window.title('语音合成器')  # 设置标题
window.resizable(False, False)  # 设置窗口大小不可变
window.geometry("1000x600")  # 设置窗口大小


def change():  # 定义点击转换按钮后的事件
    audio_name = easygui.enterbox(title='请选择', msg='请输入文件名（默认audio.mp3）') or 'audio.mp3'  # 询问合成的音频名称，默认为audio.mp3
    global writing_board  # 将writing_board定义为全局变量
    change_text = writing_board.get('1.0', tk.END)  # 获取文本框里的内容
    writing_board.destroy()  # 销毁文本框
    writing_board = tk.Text(master=window, width=56, height=16, font=('font/simhei.ttf', 18))  # 创建新文本框
    writing_board.place(x=162, y=85)  # 放置文本框（这三步为重置文本框）
    window.mainloop(1)  # 更新窗口
    final_data = ''
    for i in change_text:
        if i == '\n' or i == '\t' or i == '\r':  # 过滤特殊字符
            continue
        else:
            final_data += i
    with open(file='APIThings/appid.txt', mode='r', encoding='UTF-8') as f:  # 读取AppId
        app_id = f.read()
    with open(file='APIThings/APIKey.txt', mode='r', encoding='UTF-8') as f:  # 读取APIKey
        api_key = f.read()
    with open(file='APIThings/secretKey.txt') as f:  # 读取SecretKey
        secret_key = f.read()
    client = AipSpeech(appId=app_id, apiKey=api_key, secretKey=secret_key)  # 生成客户端
    result = client.synthesis(final_data, 'zh', 1, {'per': 3})  # 进行请求
    if not isinstance(result, dict):  # 如果返回数据类型不是字典（即成功合成语音）
        file_dir = tk.filedialog.askdirectory(title='请选择文件的保存路径', initialdir='./audio')  # 询问保存地址
        file_path = file_dir + '/' + audio_name  # 生成文件绝对路径
        with open(file_path, 'wb') as f:  # 写入二进制数据
            f.write(result)
        play_audio = easygui.boolbox('音频合成成功，是否播放？', choices=['是', '否'])  # 询问是否播放合成的音频
        if play_audio:  # 如果确定要播放
            pygame.init()  # 初始化pygame
            audio_play_window = pygame.display.set_mode((500, 500))  # 注册窗体
            pygame.display.set_caption('播放音频')  # 设置标题
            status_code = True  # 定义一个布尔值，以确定现在是否在播放音乐
            play_audio_bg = pygame.image.load('images/pause_music.jpg')  # 挂载背景图片
            pygame.mixer.init()  # 初始化pygame.mixer
            pygame.mixer.music.load(file_path)  # 挂载音频文件
            pygame.mixer.music.play()
            while True:
                audio_play_window.blit(play_audio_bg, (0, 0))  # 绘制背景图片
                for event in pygame.event.get():  # 监听事件
                    if event.type == pygame.QUIT:  # 如果事件类型为退出事件
                        pygame.quit()  # 则退出当前pygame窗体
                    if event.type == pygame.MOUSEBUTTONDOWN:  # 如果事件类型为鼠标按下事件
                        if status_code:  # 如果当前正在播放音乐
                            status_code = False  # 将当前状态设定为已暂停播放
                            pygame.mixer.music.pause()  # 暂停播放
                        else:  # 如果现在没有播放音乐
                            status_code = True  # 则将当前状态设定为继续播放
                            pygame.mixer.music.unpause()  # 继续播放
                pygame.display.update()  # 更新pygame窗体
    else:  # 如果出现异常
        print(result)  # 则打印出异常信息


write_bg_image = ImageTk.PhotoImage(file='./images/writing_bg.jpg')  # 挂载背景图片
write_bg = tk.Label(master=window, image=write_bg_image)  # 生成背景的Label标签组件
write_bg.pack()  # 放置背景图片
save_btn = tk.Button(master=window, text='转换', width=25, height=3, command=change)  # 加载“转换“按钮
save_btn.place(x=415, y=515)  # 放置”转换“按钮
writing_board = tk.Text(master=window, width=56, height=16, font=('font/simhei.ttf', 18))  # 加载文本输入框
writing_board.place(x=162, y=85)  # 放置文本输入框
window.mainloop()  # 循环更新窗体
