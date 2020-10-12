# 喜马拉雅极速版

开个新坑

喜马拉雅**极速版**自动化脚本

暂时无法每天签到

 [xmly_speed](xmly_speed.py) 


### 邀请任务
[注册链接直达](https://service-6q5z0csv-1301215769.bj.apigw.tencentcs.com/release/xmly1) (手机号注册)  
如果你不介意，并且之前没有注册过喜马拉雅的话，可以帮我完成一个邀请任务，感谢。



### 运行方案

1、GitHub action自动运行，账号信息读取自`Repo-Setting-Secrets`  

- cookie 信息抓包自手机app，域名为 `m.ximalaya.com`的可以
- fork 本项目
- Secrets 新增 `XMLY_SPEED_COOKIE`，填入cookie信息 ，多账号换行
- star一下，立即执行，观察运行情况
-  **必须**  *修改*一次文件（比如[README.md](README.md)文件）才能定时运行   (！！！！不要再问为什么不能自动运行;不懂不要修改cron )

2、下载到本地运行   
   需要两个第三方库 `rsa`和 `requests`  
   

### 查看

点击 Actions -Workflows

### Note
- 部分新手任务接口没有抓到，需要手动完成  
- **有些游戏 (比如猜拳) 第一次需要手动运行**
- 暂时无法每天签到
- 脚本会刷收听时长，因此而黑号的，本人概不负责，请知悉
- 刚注册的账号最好不要立刻跑脚本
- 不要询问 **可以通过简单搜索就可以知道答案** 的问题
