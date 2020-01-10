### 安装说明

####  安装SqlMapCelery

```
pip install -r requirements.txt
```

SqlMapCelery中自带sqlmap，正常情况下如果不想升级sqlmap的话，可以不做任何操作，如果想升级sqlmap可见下文。

####  更新sqlmap

#####  1.替换至最新sqlmap

```
cd SqlmapCelery
rm -rf sqlmap
git clone https://github.com/sqlmapproject/sqlmap
```

#####  2.安装补丁

```
bash patch.sh -action install
```

#####  3.补丁说明
为了新增一个参数 —celery， 在sqlmap/lib/parse/cmdline.py 加入 parser.add_option("--celery", dest="celery", help=SUPPRESS_HELP)

检测到了注入，会运行到lib/controller/controller.py _formatInjection函数，在这里做入库操作