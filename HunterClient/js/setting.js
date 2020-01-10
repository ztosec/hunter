$(document).ready(function () {
    showVersion();
    showManageHostname();
    showLoadTaskTips();
    showHookRuleAndEmail();
    $("#advanced-setting-save-button").click(saveTaskInfoListener);
    $("#load-task-button").click(loadTaskInfo);

});

/**
 * 显示云同步更新提示
 */
function showLoadTaskTips() {
    var x = 10;
    var y = 20;
    $("#load-task-button").mouseover(function (e) {
        this.myTitle = this.title;
        this.title = "";
        var tooltip = "<div id='tooltip'>" + this.myTitle + "<\/div>"; //创建 div 元素 文字提示
        $("body").append(tooltip);	//把它追加到文档中
        $("#tooltip").css({
            "top": (e.pageY + y) + "px",
            "left": (e.pageX + x) + "px"
        }).show("fast");	  //设置x坐标和y坐标，并且显示
    }).mouseout(function () {
        this.title = this.myTitle;
        $("#tooltip").remove();   //移除
    }).mousemove(function (e) {
        $("#tooltip").css({
            "top": (e.pageY + y) + "px",
            "left": (e.pageX + x) + "px"
        });
    });
}

/**
 * 显示等级
 */
function showVersion() {
    var manifestData = chrome.runtime.getManifest();
    var currentVersion = manifestData.version;
    $('#version-info').html(currentVersion);
}

/**
 * 显示后台地址
 */
function showManageHostname() {
    var link = $("<a>", {"href": HOST_NAME, "class": "report", "style": "color: #1A90FF;", "target": "_blank"});
    link.append(document.createTextNode(HOST_NAME));
    $('#manage-hostname').append(link);
}

/**
 * 保存到localStorage
 * 增加必选和可选提示
 */
function saveTaskInfoListener() {
    /*
    saveDataToStorage("filter_site", $("#advanced-setting-site-input").val());
    saveDataToStorage("receiver_email", $("#advanced-setting-email-input").val());
    saveDataToStorage("task_name", $("#advanced-setting-task-name-input").val());
    */
    if ($("#advanced-setting-site-input").val() === undefined || $("#advanced-setting-site-input").val() == ""){
        var ipane = $("<i>", {"class": "fa fa-exclamation-circle fa-lg","style": "color: #dc0000", "aria-hidden": "true"});
        ipane.append("&nbsp;&nbsp;");
        showSaveTip(ipane, "网址不能为空");
        setTimeout(function () {
            $('#save-error-notify-panel').remove();
        }, 800);
        return;
    } else if ($("#advanced-setting-site-input").val().length > 50){
        var ipane = $("<i>", {"class": "fa fa-exclamation-circle fa-lg","style": "color: #dc0000", "aria-hidden": "true"});
        ipane.append("&nbsp;&nbsp;");
        showSaveTip(ipane, "网址长度不能超过50");
        setTimeout(function () {
            $('#save-error-notify-panel').remove();
        }, 800);
        return;
    }

    if ($("#advanced-setting-task-name-input").val() === undefined || $("#advanced-setting-task-name-input").val() == "") {
        var ipane = $("<i>", {"class": "fa fa-exclamation-circle fa-lg","style": "color: #dc0000", "aria-hidden": "true"});
        ipane.append("&nbsp;&nbsp;");
        showSaveTip(ipane, "任务名不能为空");
        setTimeout(function (){
            $('#save-error-notify-panel').remove();
        }, 800);
        return;
    }else if($("#advanced-setting-task-name-input").val().length > 20){
        var ipane = $("<i>", {"class": "fa fa-exclamation-circle fa-lg","style": "color: #dc0000", "aria-hidden": "true"});
        ipane.append("&nbsp;&nbsp;");
        showSaveTip(ipane, "任务名长度不能超过20");
        setTimeout(function () {
            $('#save-error-notify-panel').remove();
        }, 800);
        return;
    }

    if ($("#advanced-setting-email-input").val() != undefined && $("#advanced-setting-email-input").val().length > 0){
        //console.log($("#advanced-setting-email-input").val());
        var reg = new RegExp("^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$");
        if (!reg.test($("#advanced-setting-email-input").val())){
            var ipane = $("<i>", {"class": "fa fa-exclamation-circle fa-lg","style": "color: #dc0000", "aria-hidden": "true"});
            ipane.append("&nbsp;&nbsp;");
            showSaveTip(ipane, "请输入正确的邮箱格式");
            setTimeout(function () {
                $('#save-error-notify-panel').remove();
            }, 800);
            return;
        }
    }

    saveDataToStorage(LOCAL_STORAGES.FILTER_SITE.key, $("#advanced-setting-site-input").val());
    saveDataToStorage(LOCAL_STORAGES.RECEIVER_EMAIL.key, $("#advanced-setting-email-input").val());
    saveDataToStorage(LOCAL_STORAGES.TASK_NAME.key, $("#advanced-setting-task-name-input").val());
    $('#save-success-notify-panel').css('display', "");
    setTimeout(function () {
        $('#save-success-notify-panel').css('display', "none");
    }, 800);
}

/**
 * 显示保存提示,标签和提示信息
 */

function showSaveTip(ipane, message) {
    var save_tip_tr = $("<tr>", {"id": "save-error-notify-panel"});
    var blank_td = $("<td>");
    save_tip_tr.append(blank_td);
    var notify_td = $("<td>");
    var notify_td_div = $("<div>", {"class": "notify"});
    notify_td_div.append(ipane);
    notify_td_div.append(document.createTextNode(message));
    notify_td.append(notify_td_div);
    save_tip_tr.append(notify_td);
    if ( $("#save-error-notify-panel").length <= 0 ) {
         $("#setting").append(save_tip_tr);
    }
}

/**
 * 显示hook_rule和email
 */
function showHookRuleAndEmail() {
    //getDataFromStorage("filter_site").then((value) => {
    getDataFromStorage(LOCAL_STORAGES.FILTER_SITE.key).then((value) => {
        if (value == undefined) {
            $("#advanced-setting-site-input").val("");
        } else {
            $("#advanced-setting-site-input").val(value);
        }
    });
    //getDataFromStorage("receiver_email").then((value) => {
    getDataFromStorage(LOCAL_STORAGES.RECEIVER_EMAIL.key).then((value) => {
        if (value == undefined) {
            $("#advanced-setting-email-input").val("");
        } else {
            $("#advanced-setting-email-input").val(value);
        }
        /**
         * 动态显示是否可以编辑
         */
        //getDataFromStorage("status").then((value) => {
        getDataFromStorage(LOCAL_STORAGES.STATUS.key).then((value) => {
            if (value == TASK_STATUS.ON) {
                $("#advanced-setting-email-input").attr("disabled", true);
                $("#advanced-setting-email-input").css('border', '1px solid #c7c9ca');
                $("#advanced-setting-task-name-input").attr("disabled", true);
                $("#advanced-setting-task-name-input").css('border', '1px solid #c7c9ca');
            }
        });
    });
    //getDataFromStorage("task_name").then((value) => {
    getDataFromStorage(LOCAL_STORAGES.TASK_NAME.key).then((value) => {
        if (value != undefined) {
            $("#advanced-setting-task-name-input").val(value);
        }
    });
}
/**
 * 1.弹出浮窗
 * 2.加载接口
 * 3.保存到本地
 * 4.按钮变色，status变成ON 修改监听器同步任务bug
 */
function loadTaskInfo() {
    showOverLayerBox();
    $.ajax({
        type: "get",
        url: `${API_HOST}${API_PREFIX}${API_VERSION}/user/current_task/`,
        timeout: TIME_OUT,
        success: function (message) {
            console.log("hunter-debug:加载最新任务成功,服务器响应为" + JSON.stringify(message));
            //设置加载的结果
            if (message.status == 200 && message.data !=undefined){

                if (message.data.task_id == undefined){//如果为空，则表示没有正在进行的任务
                    chrome.notifications.create(null, {
                        type: 'basic',
                        iconUrl: 'images/icon.png',
                        title: '你好',
                        message: '当前不存在待运行任务',
                        contextMessage: "加载最新任务失败",
                    });
                    switchOffStatus();//切换到初始化状态
                }else {
                    chrome.notifications.create(null, {
                        type: 'basic',
                        iconUrl: 'images/icon.png',
                        title: `${message.data.user_name}`,
                        message: `${message.message}`,
                        contextMessage: "加载最新任务成功",
                    });
                    if (message.data.hook_rule != undefined){
                        //saveDataToStorage("filter_site", message.data.hook_rule);//任务正则
                        saveDataToStorage(LOCAL_STORAGES.FILTER_SITE.key, message.data.hook_rule);//任务正则
                    }
                    if (message.data.receiver_emails != undefined){
                        //saveDataToStorage("receiver_email", message.data.receiver_emails);//任务邮件组
                        saveDataToStorage(LOCAL_STORAGES.RECEIVER_EMAIL.key, message.data.receiver_emails);//任务邮件组
                    }
                    if (message.data.task_name != undefined){
                        //saveDataToStorage("task_name", message.data.task_name);//任务名
                        //saveDataToStorage("status", TASK_STATUS.ON);//设置插件状态
                        saveDataToStorage(LOCAL_STORAGES.TASK_NAME.key, message.data.task_name);//任务名
                        saveDataToStorage(LOCAL_STORAGES.STATUS.key, TASK_STATUS.ON);//设置插件状态
                    }
                    if (message.data.task_id != undefined){
                        //saveDataToStorage("task_id", message.data.task_id);//任务id
                        saveDataToStorage(LOCAL_STORAGES.TASK_ID.key, message.data.task_id);//任务id
                    }
                    if (message.data.task_access_key != undefined){
                        //saveDataToStorage("task_access_key", message.data.task_access_key);//任务 accesskey
                        saveDataToStorage(LOCAL_STORAGES.TASK_ACCESS_KEY.key, message.data.task_access_key);//任务 accesskey
                    }
                    switchOnStatus();//切换到开启状态
                }
            }else if (message.status == 403 || message.status == 500){
                chrome.notifications.create(null, {
                    type: 'basic',
                    iconUrl: 'images/icon.png',
                    title: '你好',
                    message: `${message.extra_info}`,
                    contextMessage: "加载最新任务失败",
                });
                if (message.status == "403") {
                    chrome.tabs.create({url: message.site});
                }
            }else if(message.status == 400){
                chrome.notifications.create(null, {
                    type: 'basic',
                    iconUrl: 'images/icon.png',
                    title: '你好',
                    message: `${message.extra_info}`,
                    contextMessage: "当前不存在最新任务",
                });
                switchOffStatus();//切换到关闭状态
            }
            setTimeout(function () {
                hideOverLayerBox();
            }, TIME_OUT/10);

        },
        error: function (message) {
            chrome.notifications.create(null, {
                type: 'basic',
                iconUrl: 'images/icon.png',
                title: '你好',
                message: `${message.extra_info}`,
                contextMessage: "加载最新任务失败",
            });
            setTimeout(function () {
                hideOverLayerBox();
            }, TIME_OUT/10);
        },
        complete: function (XMLHttpRequest, status) {
            if (status == "timeout") {
                chrome.notifications.create(null, {
                    type: 'basic',
                    iconUrl: 'images/icon.png',
                    title: '你好',
                    message: `网络超时,请检查网络情况`,
                    contextMessage: "加载最新任务超时",
                });
            }
            setTimeout(function () {
                hideOverLayerBox();
            }, TIME_OUT/10);
        }
    });
}

/**
 * 显示浮窗和背景
 */
function showOverLayerBox() {
    var popBox = document.getElementById("hunter-set-pop-box");
    var popOverLayer = document.getElementById("hunter-set-pop-overLayer");
    popBox.style.display = "block";
    popOverLayer.style.display = "block";
}

function hideOverLayerBox() {
    var popBox = document.getElementById("hunter-set-pop-box");
    var popOverLayer = document.getElementById("hunter-set-pop-overLayer");
    popBox.style.display = "none";
    popOverLayer.style.display = "none";
    location.reload();
}