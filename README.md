# Violet-LogMin
一个基于 `tkinter` 和 `smtplib` 的日志自动分发系统 (实验室用)

## Features

- [x] 提供了用户界面来录入所有小组成员的日志，且界面的每个功能区均能自由改变大小
- [x] 自动编写并分发日志邮件，且接收者的日志自动置于所接收的日志列表首行
- [x] 界面包含了一个控制台用来输出操作状态信息，不再以令人目眩的弹窗显示
- [x] 邮件内容除了日志外，还添加了每日一句英语美文
- [x] 添加日志存储模块，保存所有小组成员每天的日志
- [x] 支持中文和英文
- [x] 只需修改配置文件中的发送者和接收者信息，即可推广至其他团队/组织使用
- [x] 接收到的邮件依辈分使用了敬语或正常语气

## Dependencies

```yaml
certifi==2020.12.5
chardet==4.0.0
idna==2.10
PyYAML==5.3.1
requests==2.25.1
urllib3==1.26.3
```

克隆本项目后，在根目录执行命令 `pip install -r requirements.txt` 即可导入项目运行所需的依赖

## Tutorial

本项目采用了 `violet_logmin.yaml` 配置文件集中管理所有配置信息，便于维护。

使用 `Violet-LogMin` 系统分发日志，需先在 `violet_logmin.yaml` 文件中填入发送者信息和接收者列表



1. 在 文件 `violet_logmin.yaml` 中找到 `sender` 项，填入发件邮箱地址、服务器及授权码。我使用的是 QQ 邮箱，其 smtp 服务器为 `smtp.qq.com`，授权码的获取方式参见 [什么是授权码，它又是如何设置？]( https://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=1001256)

   ```yaml
   sender:
     smtp_server: smtp.qq.com
     address: XXXXXXXX@qq.com
     authorization_code: XXXXXXXX
   ```

2. 找到 `receivers` 项，按以下格式编辑接收者列表

   ```yaml
     - sur_name: 张
       given_name: 全旦
       degree: Prof.
       address: 12345678900@163.com
       
   - sur_name: Kong
       given_name: Jimin
       degree: Bachelor.
       grade: 2017
       address: kong_jimin@qq.com
   
     - sur_name: 蔡
       given_name: 某鲲
       degree: Master.
       grade: 2020
       address: cai_xukun@qq.com
   ```

3. 在根目录下执行

   ```bash
   python3 violet_logmin.py
   ```

   这样便进入了用户界面

 

启动页

<img src="https://gitee.com/The-MinGo/MinGoBlog-Image/raw/master/Violet-LogMin//image-20210216150541256.png" alt="image-20210216150541256" style="zoom: 80%;" />

中文主界面

<img src="https://gitee.com/The-MinGo/MinGoBlog-Image/raw/master/Violet-LogMin//image-20210216151210405.png" alt="image-20210216151210405" style="zoom: 67%;" />

英文主界面

<img src="https://gitee.com/The-MinGo/MinGoBlog-Image/raw/master/Violet-LogMin//image-20210216151352267.png" alt="image-20210216151352267" style="zoom:67%;" />

填写日志后发送

<img src="https://gitee.com/The-MinGo/MinGoBlog-Image/raw/master/Violet-LogMin//image-20210216205307190.png" alt="image-20210216205307190" style="zoom:67%;" />

接收到的日志邮件

<img src="https://gitee.com/The-MinGo/MinGoBlog-Image/raw/master/Violet-LogMin//image-20210216205639685.png" alt="image-20210216205639685" style="zoom: 67%;" />