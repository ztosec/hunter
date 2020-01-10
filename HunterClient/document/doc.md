rc版本，优化代码，去掉重复冗余的代码
### 细节文档
#### 插件推送更新细节
1.本地配置文件保存插件的版本 保存在manifest.json中  
2.插件自动连接上stomp服务器
    2.1建立那种只可以消费队列的账户  
    2.2或者不需要建立的账户  
3.服务端推送message到mq中  
    3.1新建一个低权限的账户



### 启动新建一个任务

#### 请求方式 POST
#### 请求URL /task/
#### 请求BODY
    {
    	"cookie": "xxx",
    	"date": "2018-12-23",
    	"time": "2018-12-13-14-12",
    	"hook_rule": "xxsx",
    	"read_agreement": "true"
    }

###### 字段说明
    cookie  cookie,用来验证内部身份,不保存(由插件获得)
    date    日期，任务的创建日期(服务器来生成)
    time    时间，任务创建的具体时间(服务器来生成)
    hook_rule hook的正则表达式
    read_agreement 是否阅读用户协议

#### 响应BODY
    创建成功    {"code": "200", "message": "创建任务成功", task_id": "xxx", "access_key": "xxx"}
    创建失败    {"code": "400", "message": "创建任务失败"}

#### 说明
    task_id和access_key由服务器生成发送，access_key是用服务器ase加密之后的密文，用于验证task_id和access_key的绑定关系
    成功创建任务得到taskid之后,应该将task_id和access_key写入到localstore,这样再下一次的时候能够将url和task绑定起来
    创建失败后，浏览器插件应该通知下用户
