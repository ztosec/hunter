API接口
======================

创建任务
---------------------

用于hunter-client向后端发送一个创建任务的请求

Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
请求数据包如下::

    POST /task/
    Content-Type: application/json; charset=utf-8

    {
        read_agreement: "true",
        hook_rule: "http://xx:8080/",
        receiver_email: "xx@xx.cn",
        task_name: "安全测试项目"
    }

请求参数说明

============== ======= =================== ===========================
参数            类型     样例                备注
============== ======= =================== ===========================
read_agreement  str    true                是否阅读并同意协议
hook_rule       str    http:\/\/xx:8080\/  hooke规则
receiver_email  str    xxxx@zto.cn         结束任务之后发送的邮箱
task_name       str    xx测试项目           任务名称
============== ======= =================== ===========================


**测试**:

  ..  http:example:: curl wget httpie python-requests

      POST /task/ HTTP/1.1
      Host: localhost:8080
      Accept: application/json

      {
        read_agreement: "true",
        hook_rule: "http://xx:8080/",
        receiver_email: "x@xx.cn",
        task_name: "安全测试项目"
      }


Response(200)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

创建任务成功::

    Content-Type: application/json; charset=utf-8
    {
        "create_time": "2018-08-30-12:10:24",
        "fullname": "小陈",
        "message": "创建任务成功",
        "status": 200,
        "task_access_key": "9d19c488xxx..",
        "task_id": 23
    }

================ ======= =================== ===========================
参数              类型     值                 备注
================ ======= =================== ===========================
create_time      str     2018-08-30-12:10:24 任务创建时间
fullname         str     小陈                 创建人
message          str     创建任务成功
status           int     200                 状态码
task_access_key  str     9d19c488xxx...      用于认证身份,SSO和task_access_key双因子认证
task_id          int     23                  任务ID
================ ======= =================== ===========================

Response(400)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

错误的请求::

    Content-Type: application/json; charset=utf-8
    {
        "message": "创建任务失败",
        "status": 400,
        "extra_info": "新建任务时没有设置网址正则或任务名称",
    }

================ ======= ==================================== ===========================
参数              类型     值                                   备注
================ ======= ==================================== ===========================
message          str     创建任务失败
status           int     400                                  状态码
extra_info       str     新建任务时没有设置网址正则或任务名称      错误信息
================ ======= ==================================== ===========================

Response(403)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

错误的请求::

    Content-Type: application/json; charset=utf-8
    {
        "message": "创建任务失败",
        "status": 403,
        "extra_info": "认证失败,请重新登录进行授权",
        "site": "http://127.0.0.1:8888/authorization/"
    }

================ ======= ==================================== ===========================
参数              类型     值                                   备注
================ ======= ==================================== ===========================
message          str     创建任务失败
status           int     403                                  状态码
extra_info       str     新建任务时没有设置网址正则或任务名称      错误信息
site             str     http://127.0.0.1:8888/authorization/ 跳转网址
================ ======= ==================================== ===========================


Response(500)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

错误的请求::

    Content-Type: application/json; charset=utf-8
    {
        "message": "创建任务失败",
        "status": 500,
        "extra_info": "请检查插件权限是否能获取cookie",
        "site": "http://127.0.0.1:8888/authorization/"
    }

================ ======= ============================================================== ===========================
参数              类型     值                                                            备注
================ ======= ============================================================== ===========================
message          str     创建任务失败
status           int     400                                                            状态码
extra_info       str     请检查插件权限是否能获取cookie或者sso认证接口超时,请稍后重试          错误信息
site             str     http://127.0.0.1:8888/authorization/                           跳转网址
================ ======= ============================================================== ===========================



结束任务
---------------------

用于hunter-client向后端发送一个结束任务的请求

Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
请求数据包如下::

    DELETE /task/
    Content-Type: application/json; charset=utf-8
    {
        "task_id": 23,
        "task_access_key": "9d19c488218fe5...",
    }

请求参数说明

================ ======= =================== ===========================
参数              类型     值                  备注
================ ======= =================== ===========================
task_id          int     23                  任务ID
task_access_key  str     9d19c488218fe5...   认证key,不能结束别人的任务
================ ======= =================== ===========================


**测试**:

  ..  http:example:: curl wget httpie python-requests

      DELETE /task/ HTTP/1.1
      Host: localhost:8080
      Accept: application/json

      {
        "task_id": 23,
        "task_access_key": "9d19c488218fe5...",
      }


Response(200)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

结束任务成功::

    Content-Type: application/json; charset=utf-8
    {
        "message": "结束任务成功",
        "status": 200,
        "fullname": "小陈",
        "extra_info": "一旦扫描结束会立即通知你的邮箱，请注意查收"
    }

================ ======= ========================================= ===========================
参数              类型     值                                        备注
================ ======= ========================================= ===========================
message          str     结束任务成功 任务创建时间
status           str     200                                        状态码
fullname         str     小陈                                        创建人
extra_info       str     一旦扫描结束会立即通知你的邮箱,请注意查收
================ ======= ========================================= ===========================

Response(400)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

结束任务失败::

    Content-Type: application/json; charset=utf-8
    {
        "message": "结束任务失败",
        "status": 400,
        "extra_info": "task_id和access_key缺失,无法结束任务",
        "site": "http://127.0.0.1:8888/authorization/"
    }

================ ======= ==================================== ===========================
参数              类型     值                                   备注
================ ======= ==================================== ===========================
message          str     创建任务失败
status           int     400                                  状态码
extra_info       str     新建任务时没有设置网址正则或任务名称      错误信息
site             str     跳转网址
================ ======= ==================================== ===========================

Response(403)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

结束任务失败::

    Content-Type: application/json; charset=utf-8
    {
        "message": "结束任务失败",
        "status": 403,
        "extra_info": "task_id和task_access_key映射关系不对",
        "site": "http://127.0.0.1:8888/authorization/"
    }

================ ======= ==================================================================================== ===========================
参数              类型     值                                                                                   备注
================ ======= ==================================================================================== ===========================
message          str     创建任务失败
status           int     403                                                                                  状态码
extra_info       str     新建任务时没有设置网址正则或任务名称或者请注销登录或者清除cookie之后重新登录                   错误信息
site             str     http://127.0.0.1:8888/authorization/                                                 跳转网址
================ ======= ==================================================================================== ===========================




发送捕获到的数据
---------------------

用于hunter-client向后端发送一个自身HOOK到的数据

Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
请求数据包如下::

    POST /task/<int:task_id>/url/task_access_key/<string:task_access_key>
    Content-Type: application/json; charset=utf-8
    {
        "data": {
            "requestid": "2319",
            "type": "xmlhttprequest",
            "url": "http://xxxxx/ajax_link.php?id=1&t=0.7082074613901739",
            "method": "post",
            "headers": "{\"Origin\":\"xxxxx\",\"User-Agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36\",\"Accept\":\"*/*\",\"Referer\":\"http://xx.xx.cn/\",\"Accept-Encoding\":\"gzip, deflate\",\"Accept-Language\":\"zh-CN,zh;q=0.9\",\"Cookie\":\"u=guest\"}"
        }
    }


.. note::
    上面data为捕获到的具体数据包,比较复杂这里不展开，具体可以看chrome官方文档 `Link experimental webRequest API <https://developer.chrome.com/extensions/webRequest>`_

请求参数说明

================ ======= =================== ===========================
参数              类型     值                  备注
================ ======= =================== ===========================
task_id          int     24                  任务ID
task_access_key  str     9d19c488218fe5...   认证key,不能结束别人的任务
================ ======= =================== ===========================


**测试**:

  ..  http:example:: curl wget httpie python-requests

      POST /task/26/url/task_access_key/790bd30811ada91../ HTTP/1.1
      Host: localhost:8080
      Accept: application/json

        {
            "data": {
                "requestid": "2319",
                "type": "xmlhttprequest",
                "url": "http://xxxxx/ajax_link.php?id=1&t=0.7082074613901739",
                "method": "post",
                "headers": "{\"Origin\":\"xxxxx\",\"User-Agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36\",\"Accept\":\"*/*\",\"Referer\":\"http://demo.aisec.cn/demo/aisec/\",\"Accept-Encoding\":\"gzip, deflate\",\"Accept-Language\":\"zh-CN,zh;q=0.9\",\"Cookie\":\"u=guest\"}"
            }
        }




Response(200)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

发送成功::

    Content-Type: application/json; charset=utf-8
    {
        "message": "发送url成功",
        "status": 200,
    }


================ ======= ========================================= ===========================
参数              类型     值                                        备注
================ ======= ========================================= ===========================
message          str     发送url成功
status           int     200                                        状态码
================ ======= ========================================= ===========================

Response(403)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

发送失败::

    Content-Type: application/json; charset=utf-8
    {
        "message": "taskid或者accesskey不正确",
        "status": 403,
    }


================ ======= ==================================== ===========================
参数              类型     值                                   备注
================ ======= ==================================== ===========================
message          str     taskid或者accesskey不正确
status           int     403                                  状态码
================ ======= ==================================== ===========================


查看扫描历史任务
---------------------

登录成功之后获得个人所有扫描记录

Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
请求数据包如下::
    GET /scanrecord/


**测试**:

  ..  http:example:: curl wget httpie python-requests

      GET /scanrecord/ HTTP/1.1
      Host: localhost:8080

Response(200)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

查询成功::

    Content-Type: application/json; charset=utf-8
    {
        "data": [{
            "task": {
                "create_time": "2018-08-07-13:19:02",
                "dept_name": "信息安全部",
                "fullname": "小朱",
                "id": "8",
                "task_name": "test",
                "username": "XXX"
            },
            "url": {
                "num": 7
            },
            "vul": {
                "details": [
                    "{\"id\": \"35\", \"task_id\": \"8\", \"info\": \"http://XXXXX/ajax_link.php\存\在\一\个sql\注\入\漏\洞\", \"path\": \"\", \"payload\": \"Parameter: id (GET)\\n    Type: boolean-based blind\\n    Title: AND boolean-based blind - WHERE or HAVING clause\\n    Payload: id=1 AND 1414=1414&t=0.2564469418404698\", \"imp_version\": \"\所\有\版\本\", \"error\": \"\", \"repair\": \"\过\滤\掉sql\恶\意\字\符\", \"type\": \"sql_inject\", \"chinese_type\": \"sql\注\入\", \"description\": \"Sql \注\入\攻\击\是\通\过\将\恶\意\的 Sql \查\询\或\添\加\语\句\插\入\到\应\用\的\输\入\参\数\中\，\再\在\后\台 Sql \服\务\器\上\解\析\执\行\进\行\的\攻\击\，\它\目\前\黑\客\对\数\据\库\进\行\攻\击\的\最\常\用\手\段\之\一\。\参\考\连\接http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21741806\", \"level\": \"high\"}",
                    "{\"id\": \"36\", \"task_id\": \"8\", \"info\": \"http://XXXXX//js_link.php?id=2&msg=abc\存\在\一\个xss\漏\洞\", \"path\": \"\", \"payload\": \"[{'url': u'http://XXXXXX/js_link.php?msg='><xss></xss>//&id='><xss></xss>//', 'data': None}]\", \"imp_version\": \"\所\有\版\本\", \"error\": \"\", \"repair\": \"\过\滤\掉<,>,',\等\特\殊\字\符\", \"type\": \"xss\", \"chinese_type\": \"xss\跨\站\脚\本\攻\击\", \"description\": \"XSS\攻\击\全\称\跨\站\脚\本\攻\击\，XSS\是\一\种\在web\应\用\中\的\计\算\机\安\全\漏\洞\，\它\允\许\恶\意web\用\户\将\代\码\植\入\到\提\供\给\其\它\用\户\使\用\的\页\面\中m\，\详\情\请\参\考http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21743578\", \"level\": \"high\"}",
                    "{\"id\": \"37\", \"task_id\": \"8\", \"info\": \"http://XXXXX//js_link.php\存\在\一\个sql\注\入\漏\洞\", \"path\": \"\", \"payload\": \"Parameter: id (GET)\\n    Type: boolean-based blind\\n    Title: AND boolean-based blind - WHERE or HAVING clause\\n    Payload: id=2 AND 7328=7328&msg=abc\", \"imp_version\": \"\所\有\版\本\", \"error\": \"\", \"repair\": \"\过\滤\掉sql\恶\意\字\符\", \"type\": \"sql_inject\", \"chinese_type\": \"sql\注\入\", \"description\": \"Sql \注\入\攻\击\是\通\过\将\恶\意\的 Sql \查\询\或\添\加\语\句\插\入\到\应\用\的\输\入\参\数\中\，\再\在\后\台 Sql \服\务\器\上\解\析\执\行\进\行\的\攻\击\，\它\目\前\黑\客\对\数\据\库\进\行\攻\击\的\最\常\用\手\段\之\一\。\参\考\连\接http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21741806\", \"level\": \"high\"}"
                ],
                "level": {
                    "high": 3,
                    "low": 0,
                    "middle": 0
                },
                "num": 3,
                "risk_level": "high",
                "type": {
                    "cmdect": 0,
                    "cors": 0,
                    "crlf": 0,
                    "csrf": 0,
                    "ddos": 0,
                    "file_include": 0,
                    "file_read": 0,
                    "file_upload": 0,
                    "hidden_danger": 0,
                    "info_leak": 0,
                    "jsonp": 0,
                    "other": 0,
                    "sql_inject": 2,
                    "weak_pwd": 0,
                    "xss": 1,
                    "xxe": 0
                }
            }
        }],
        "message": "查询成功",
        "status": 200
    }



================ ======= ========================================= ===========================
参数              类型     值                                        备注
================ ======= ========================================= ===========================
data             list    [{"task":TASK, "url": URL, "vul": VULN}]  比较复杂，可见下表
message          str     查询成功
status           int     200                                        状态码
================ ======= ========================================= ===========================

TASK实体

================ ======= ====================== ===========================
参数             类型    值                     备注
================ ======= ====================== ===========================
create_time      str     2018-08-07-13:19:02    任务创建时间
dept_name        str     信息安全部             所属部门
fullname         str     小朱                   中文名
id               str     8                      任务ID
task_name        str     test                   任务名称
username         str     XXX                    中天用户名
================ ======= ====================== ===========================

URL实体

======= ======= ===== ===========================
参数     类型    值    备注
======= ======= ===== ===========================
num      int    7     当前任务的URL数量
======= ======= ===== ===========================

VULN实体

.. list-table:: VULN
    :widths: 15 10 30 30

    * - 参数
      - 类型
      - 值
      - 备注
    * - details
      - list
      - VULN_DETAIL
      - 具体漏洞实体
    * - level
      - map
      - {"high": 3,"low": 0,"middle": 0}
      - high,low,middle分别为高中低的数量
    * - num
      - int
      - 3
      - 漏洞总数
    * - risk_level
      - high
      - 3
      - 本次任务风险等级
    * - type
      - map
      - {"cmdect": 0, "cors": 0, "crlf": 0, "csrf": 0, "ddos": 0, "file_include": 0, "file_read": 0, "file_upload": 0, "hidden_danger": 0,"info_leak": 0, "jsonp": 0, "other": 0, "sql_inject": 2, "weak_pwd": 0, "xss": 1, "xxe": 0}
      - 各种漏洞类型对于的数量


VULN_DETAIL实体

.. list-table:: VULN_DETAIL
    :widths: 15 10 30 30

    * - 参数
      - 类型
      - 值
      - 备注
    * - id
      - str
      - 35
      - 漏洞ID
    * - task_id
      - str
      - 8
      - 漏洞所对应的任务ID
    * - info
      - str
      - http://xxxxxx/ajax_link.php存在一个sql注入漏洞
      - 漏洞概述
    * - payload
      - str
      - Parameter: id (GET)\n    Type: boolean-based blind\n    Title: AND boolean-based blind - WHERE or HAVING clause\n    Payload: id=1 AND 1414=1414&t=0.2564469418404698
      - 漏洞攻击载荷
    * - error
      - str
      -
      - 错误信息
    * - imp_version
      - str
      - 所有版本
      - 漏洞影响版本
    * - repair
      - str
      - 修复建议
      - 过滤掉sql恶意字符
    * - type
      - str
      - sql_inject
      - 漏洞类型
    * - chinese_type
      - str
      - sql注入
      - 漏洞类型中文名
    * - description
      - str
      - 漏洞参考信息
      - Sql 注入攻击是通过将恶意的 Sql 查询或添加语句插入到应用的输入参数中，再在后台 Sql 服务器上解析执行进行的攻击，它目前黑客对数据库进行攻击的最常用手段之一。参考连接http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21741


查看一次具体的扫描任务
---------------------------------------

传入id可以查看具体的结果

Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
请求数据包如下::
    GET /vulnerability/details/filter/?taskid={taskid}

请求参数说明

================ ======= =================== ===========================
参数              类型     值                  备注
================ ======= =================== ===========================
taskid           int     8                   任务ID
================ ======= =================== ===========================


**测试**:

  ..  http:example:: curl wget httpie python-requests

      GET /vulnerability/details/filter/?taskid=8/ HTTP/1.1
      Host: localhost:8080

Response(200)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
查询成功::

    {
        "message": "查询成功",
        "status": 200,
        "vlun": {
            "details": [
                "{\"id\": \"35\", \"url_id\": \"999999999\", \"task_id\": \"8\", \"info\": \"http://xxxxxx/ajax_link.php\存\在\一\个sql\注\入\漏\洞\", \"path\": \"\", \"payload\": \"Parameter: id (GET)\\n    Type: boolean-based blind\\n    Title: AND boolean-based blind - WHERE or HAVING clause\\n    Payload: id=1 AND 1414=1414&t=0.2564469418404698\", \"imp_version\": \"\所\有\版\本\", \"error\": \"\", \"repair\": \"\过\滤\掉sql\恶\意\字\符\", \"type\": \"sql_inject\", \"chinese_type\": \"sql\注\入\", \"description\": \"Sql \注\入\攻\击\是\通\过\将\恶\意\的 Sql \查\询\或\添\加\语\句\插\入\到\应\用\的\输\入\参\数\中\，\再\在\后\台 Sql \服\务\器\上\解\析\执\行\进\行\的\攻\击\，\它\目\前\黑\客\对\数\据\库\进\行\攻\击\的\最\常\用\手\段\之\一\。\参\考\连\接http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21741806\", \"level\": \"high\"}",
                "{\"id\": \"36\", \"url_id\": \"999999999\", \"task_id\": \"8\", \"info\": \"http://xxxxx/js_link.php?id=2&msg=abc\存\在\一\个xss\漏\洞\", \"path\": \"\", \"payload\": \"[{'url': u'http://xxxxxxxx/js_link.php?msg='><xss></xss>//&id='><xss></xss>//', 'data': None}]\", \"imp_version\": \"\所\有\版\本\", \"error\": \"\", \"repair\": \"\过\滤\掉<,>,',\等\特\殊\字\符\", \"type\": \"xss\", \"chinese_type\": \"xss\跨\站\脚\本\攻\击\", \"description\": \"XSS\攻\击\全\称\跨\站\脚\本\攻\击\，XSS\是\一\种\在web\应\用\中\的\计\算\机\安\全\漏\洞\，\它\允\许\恶\意web\用\户\将\代\码\植\入\到\提\供\给\其\它\用\户\使\用\的\页\面\中m\，\详\情\请\参\考http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21743578\", \"level\": \"high\"}",
                "{\"id\": \"37\", \"url_id\": \"999999999\", \"task_id\": \"8\", \"info\": \"http://xxxxxxxx/js_link.php\存\在\一\个sql\注\入\漏\洞\", \"path\": \"\", \"payload\": \"Parameter: id (GET)\\n    Type: boolean-based blind\\n    Title: AND boolean-based blind - WHERE or HAVING clause\\n    Payload: id=2 AND 7328=7328&msg=abc\", \"imp_version\": \"\所\有\版\本\", \"error\": \"\", \"repair\": \"\过\滤\掉sql\恶\意\字\符\", \"type\": \"sql_inject\", \"chinese_type\": \"sql\注\入\", \"description\": \"Sql \注\入\攻\击\是\通\过\将\恶\意\的 Sql \查\询\或\添\加\语\句\插\入\到\应\用\的\输\入\参\数\中\，\再\在\后\台 Sql \服\务\器\上\解\析\执\行\进\行\的\攻\击\，\它\目\前\黑\客\对\数\据\库\进\行\攻\击\的\最\常\用\手\段\之\一\。\参\考\连\接http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21741806\", \"level\": \"high\"}"
            ],
            "level": {
                "high": 3,
                "low": 0,
                "middle": 0
            },
            "num": 3,
            "risk_level": "high",
            "type": {
                "cmdect": 0,
                "cors": 0,
                "crlf": 0,
                "csrf": 0,
                "ddos": 0,
                "file_include": 0,
                "file_read": 0,
                "file_upload": 0,
                "hidden_danger": 0,
                "info_leak": 0,
                "jsonp": 0,
                "other": 0,
                "sql_inject": 2,
                "weak_pwd": 0,
                "xss": 1,
                "xxe": 0
            }
        }
    }
字段意义和可参考上一小节 查看扫描历史任务