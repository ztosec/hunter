var requestQueue = new Queue();
/*var domain = "10.211.55.2";
var apiHost = `http://${domain}:8888`;
*/
chrome.runtime.onMessage.addListener(onMessageListenerEvent);
/**
 * hook rquests
 * */
function HookonBeforeRequest(details) {
    //getDataFromStorage("status").then((status) => {
    getDataFromStorage(LOCAL_STORAGES.STATUS.key).then((status) => {
        if (status == TASK_STATUS.ON) {
            //getDataFromStorage("filter_site").then((filter_site) => {
            getDataFromStorage(LOCAL_STORAGES.FILTER_SITE.key).then((filter_site) => {
                filter_site = filter_site.toString().replace(new RegExp("\\*", 'g'), "(.*)");
                //console.log(filter_site);
                var reg_exp = new RegExp(filter_site.toString());
                if (reg_exp.test(details.url) && details.url.indexOf(`${API_HOST}${API_PREFIX}${API_VERSION}/user/task`) == -1) {
                    req = {
                        'requestid': details.requestId,
                        'type': details.type,
                        'url': details.url,
                        'method': details.method.toLowerCase(),
                        'data': JSON.stringify(getData(details).data),
                        'data_type': getData(details).data_type,
                        'parser': 'chrome-plugin',
                    };
                    if (!requestQueue.has("requestid", details.requestId)) {
                        requestQueue.push({"requestid": details.requestId, "data": req});
                    }
                    //requestQueue.push({"requestid": details.requestId, "data": req});
                }
            });
        }
    });
}
/**
 * hook beforeSendHeadrs
 * hook beforeSendHeadrs
 * */
function HookonBeforeSendHeaders(details) {
    //getDataFromStorage("status").then((status) => {
      getDataFromStorage(LOCAL_STORAGES.STATUS.key).then((status) => {
        if (status == TASK_STATUS.ON) {
            getDataFromStorage(LOCAL_STORAGES.FILTER_SITE.key).then((filter_site) => {
            //getDataFromStorage("filter_site").then((filter_site) => {
                if (filter_site == undefined){return;}
                filter_site = filter_site.toString().replace(new RegExp("\\*", 'g'), "(.*)");
                var reg_exp = new RegExp(filter_site.toString());
                if (reg_exp.test(details.url) && details.url.indexOf(`${API_HOST}${API_PREFIX}${API_VERSION}/user/task`) == -1) {
                    requestid = details.requestId;

                    for (var i = 0; i < requestQueue.size(); i++) {
                        if (requestQueue.get(i).requestid == requestid) {
                            requestQueue.get(i).data.headers = JSON.stringify(getHeaders(details));
                            console.log("hunter-debug:发送到后端API的数据为" + JSON.stringify(requestQueue.get(i)));
                            sendDataToHunterServer(requestQueue.get(i).data);
                        }
                    }
                }
            });
        }
    });
}

/**
 * onMessage addListener事件 监听器,新增一个状态，为同意后不再显示该协议
 */
function onMessageListenerEvent(request, sender, sendResponse) {
    if (request.cmd == "CREATE_TASK" && request.origin == ORIGINS.CONTENT) {
            removeListener();
            creatTask(addListener);
        } else if (request.cmd == "STOP_TASK" && request.origin == ORIGINS.CONTENT) {
             console.log("hunter stop hook http request");
             stopTask();
             removeListener();
        } else if(request.cmd == "CONTINUE_TASK" && request.origin == ORIGINS.SETTING){
            //成功同步任务，由setting.js 发起
             removeListener();
             addListener();
        } else if(request.cmd == "REMOVE_LISTENER" && request.origin == ORIGINS.SETTING){
            //成功同步任务，但后台并无任务，由setting.js 发起
             removeListener();
        }
        console.log("onMessageListenerEvent");
    sendResponse("");
}
/**
 * 添加监听器
 */
function addListener() {
    chrome.webRequest.onBeforeRequest.addListener(HookonBeforeRequest, {urls: ["*://*/*"]}, ["blocking", "requestBody"]);
    //chrome.webRequest.onBeforeSendHeaders.addListener(HookonBeforeSendHeaders, {urls: ["*://*/*"]}, ["blocking", "requestHeaders"]);
    //@warnning chrome 72之后api变了，不然无法hook到cookie
    chrome.webRequest.onBeforeSendHeaders.addListener(HookonBeforeSendHeaders, {urls: ["*://*/*"]}, ["blocking", "requestHeaders", "extraHeaders"]);
}
/***
 * 移除监听器
 */
function removeListener() {
    chrome.webRequest.onBeforeRequest.removeListener(HookonBeforeRequest);
    chrome.webRequest.onBeforeSendHeaders.removeListener(HookonBeforeSendHeaders);
}

/**
 * 返回http 头, Content-Type尽量原格式, 有时候会变成 Content-type
 * @param details
 * @returns {*}
 */
function getHeaders(details) {
    var result = {};
    if (details.requestHeaders != undefined) {
        details.requestHeaders.forEach(function (item, index) {
            if (item.name.toLowerCase() == "content-type") {
                result["content-type"] = item.value;
            } else {
                result[item.name] = item.value;
            }
        });
        return result;
    }
    return undefined;
}
/**
 * 返回http 请求数据
 * @param details
 * @returns {*}
 */
function getData(details) {
    var result = {};
    //console.log(details.requestBody);
    if (details.requestBody != undefined) {
        try {
            data = decodeURIComponent(String.fromCharCode.apply(null,
                new Uint8Array(details.requestBody.raw[0].bytes)));
            return {data: data, data_type: 'raw'};
        }
        catch (e) {
            //form 表单
            if (e instanceof TypeError) {
                for (var key in details.requestBody.formData) {
                    details.requestBody.formData[key].forEach(function (value, index) {
                        result[key] = value;
                    });
                }
            }
            return {data: result, data_type: 'form_data'};
        }
    }
    return {data: undefined, data_type: undefined};
}
/**
 * 新建任务，启动一个新任务,v2版本删除ztoAccess，采用cookie的方式
 */
function creatTask(callback) {
    var status = false;
    console.log("hunter-debug: 正在创建一个任务");
    var postData = {};
    postData.read_agreement = "true";
    //var hookRulePromise = getDataFromStorage("filter_site");
    var hookRulePromise = getDataFromStorage(LOCAL_STORAGES.FILTER_SITE.key);
    hookRulePromise.then((filter_site) => {
        postData.hook_rule = filter_site;
    });
    //var receviceEmailPromise = getDataFromStorage("receiver_email");
    var receviceEmailPromise = getDataFromStorage(LOCAL_STORAGES.RECEIVER_EMAIL.key);
    receviceEmailPromise.then((receiver_email) => {
        postData.receiver_email = receiver_email;
    });
    //var taskNamePromise = getDataFromStorage("task_name");
    var taskNamePromise = getDataFromStorage(LOCAL_STORAGES.TASK_NAME.key);
    taskNamePromise.then((task_name) => {
        postData.task_name = task_name;
    });
    Promise.all([hookRulePromise, receviceEmailPromise, taskNamePromise]).then(value => {
            $.ajax({
                type: "post",
                dataType: "json",
                url: `${API_HOST}${API_PREFIX}${API_VERSION}/user/tasks/`,
                timeout: 10000,
                contentType: "application/json",
                data: JSON.stringify(postData),
                success: function (message) {
                    console.log("hunter-debug:创建任务服务器响应为" + JSON.stringify(message));
                    if (message.status == "200") {
                        chrome.notifications.create(null, {
                            type: 'basic',
                            iconUrl: 'images/icon.png',
                            title: `${message.data.full_name},你好`,
                            message: `创建时间: ${message.data.create_time}`,
                            contextMessage: '创建任务成功',
                        });
                        /*
                        saveDataToStorage("status", TASK_STATUS.ON);
                        saveDataToStorage("task_id", message.task_id);
                        saveDataToStorage("task_access_key", message.task_access_key);
                        */
                        saveDataToStorage(LOCAL_STORAGES.STATUS.key, TASK_STATUS.ON);
                        saveDataToStorage(LOCAL_STORAGES.TASK_ID.key, message.data.task_id);
                        saveDataToStorage(LOCAL_STORAGES.TASK_ACCESS_KEY.key, message.data.task_access_key);

                        status = true;
                        //更换图标
                        chrome.browserAction.setIcon({path: 'images/logo_on.png'});
                        callback();

                    } else {
                        chrome.notifications.create(null, {
                            type: 'basic',
                            iconUrl: 'images/icon.png',
                            title: '你好',
                            message: `${message.data.extra_info}`,
                            contextMessage: "创建任务失败",
                        });
                        if (message.status == "403") {
                            chrome.tabs.create({url: message.data.site});
                        }
                        status = false;
                    }
                    return status;
                },
                error: function (message) {
                    chrome.notifications.create(null, {
                        type: 'basic',
                        iconUrl: 'images/icon.png',
                        title: '你好',
                        message: `服务器没有响应`,
                        contextMessage: "创建任务失败",
                    });
                }
            });
        }
    );
}

/**
 * 停止任务，结束一个任务，废除ZtoAccessKey
 */
function stopTask() {
    var postData = {};
    //var taskIdPromise = getDataFromStorage("task_id");
    var taskIdPromise = getDataFromStorage(LOCAL_STORAGES.TASK_ID.key);
    taskIdPromise.then((taskid) => {
        postData.task_id = taskid;
    });
    //var taskAccessKeyPromise = getDataFromStorage("task_access_key");
    var taskAccessKeyPromise = getDataFromStorage(LOCAL_STORAGES.TASK_ACCESS_KEY.key);
    taskAccessKeyPromise.then((task_access_key) => {
        postData.task_access_key = task_access_key;
    });

    Promise.all([taskIdPromise, taskAccessKeyPromise]).then(value => {
        $.ajax({
            type: "delete",
            dataType: "json",
            url: `${API_HOST}${API_PREFIX}${API_VERSION}/user/tasks/`,
            contentType: "application/json",
            timeout: 10000,
            data: JSON.stringify(postData),
            success: function (message) {
                console.log("hunter-debug:结束任务服务器响应为" + JSON.stringify(message));
                if (message.status == "200") {
                    console.log(message);
                    chrome.notifications.create(null, {
                        type: 'basic',
                        iconUrl: 'images/icon.png',
                        title: `${message.data.full_name},你好`,
                        message: `结束时间: ${message.data.stop_time} ${message.data.extra_info}`,
                        contextMessage: '结束任务成功',
                    });
                    //saveDataToStorage("status", TASK_STATUS.OFF);
                    saveDataToStorage(LOCAL_STORAGES.STATUS.key, TASK_STATUS.OFF);
                    chrome.browserAction.setIcon({path: 'images/logo_off.png'});
                } else {
                    chrome.notifications.create(null, {
                        type: 'basic',
                        iconUrl: 'images/icon.png',
                        title: '你好',
                        message: message.data.extra_info,
                        contextMessage: '结束任务失败',
                    });
                    if (message.status == "403") {
                        chrome.tabs.create({url: message.site});
                    }
                }
            }, error: function (message) {
                chrome.notifications.create(null, {
                    type: 'basic',
                    iconUrl: 'images/icon.png',
                    title: '你好',
                    message: `服务器没有响应`,
                    contextMessage: "结束任务失败",
                });
            }

        });
    });
}

/***
 * 将url发送到hunter server后端api，task和taskaccesskey必须相互绑定匹配，解决url可以发送到任意任务的问题
 * 修复平台上关闭任务
 */
function sendDataToHunterServer(urlData) {
    var postData = {};
    //var taskIdPromise = getDataFromStorage("task_id");
    var taskIdPromise = getDataFromStorage(LOCAL_STORAGES.TASK_ID.key);
    taskIdPromise.then((task_id) => {
        postData.task_id = task_id;
    });

    //var taskAccessKeyPromise = getDataFromStorage("task_access_key");
    var taskAccessKeyPromise = getDataFromStorage(LOCAL_STORAGES.TASK_ACCESS_KEY.key);
    taskAccessKeyPromise.then((task_access_key) => {
        postData.task_access_key = task_access_key;
    });

    Promise.all([taskIdPromise, taskAccessKeyPromise]).then(value => {
        var url = `${API_HOST}${API_PREFIX}${API_VERSION}/user/task/${postData.task_id}/url/task_access_key/${postData.task_access_key}`;
        //console.log(url);
        var data = {};
        data.data = urlData;
        $.ajax({
            type: "post",
            dataType: "json",
            url: url,
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function (message) {
                console.log("hunter-debug:发送到api待接口为"+JSON.stringify(data) )
                if (message.status == "403") {
                    chrome.notifications.create(null, {
                        type: 'basic',
                        iconUrl: 'images/icon.png',
                        title: `你好`,
                        message: `${message.data.extra_info}`,
                        contextMessage: `${message.message}`,
                    });
                    chrome.tabs.create({url: message.data.site});
                    switchOffStatus();//切换状态
                } else if (message.status == "400"){
                    //不需要重复提醒哦
                    chrome.notifications.create(null, {
                        type: 'basic',
                        iconUrl: 'images/icon.png',
                        title: `你好`,
                        message: "检测到任务已经结束,插件可以同步一次最新任务",
                        contextMessage: `${message.message}`,
                    });
                    chrome.tabs.create({url: message.data.site});
                    switchOffStatus();//切换状态
                }
                console.log("hunter-debug:api响应结果为" + JSON.stringify(message));
            }

        });
    });
}

/**
 * 定义队列
 * @param size
 * @constructor
 */
function Queue(size) {
    var list = [];

    //向队列中添加数据
    this.push = function (data) {
        if (data == null) {
            return false;
        }
        //如果传递了size参数就设置了队列的大小
        if (size != null && !isNaN(size)) {
            if (list.length == size) {
                this.pop();
            }
        }
        list.unshift(data);
        return true;
    };

    //从队列中取出数据
    this.pop = function () {
        return list.pop();
    };

    //返回队列的大小
    this.size = function () {
        return list.length;
    };

    //返回队列的内容
    this.quere = function () {
        return list;
    };
    //获取某个位置的值
    this.get = function (index) {
        return list[index];
    }
    //判断某一个字段的值是否出现过
    this.has = function (field, value) {
        for (var i = 0; i < this.size(); i++) {
            if (this.get(i)[field] == value) {
                return true;
            }
        }
        return false;
    }
}
