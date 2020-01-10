$(document).ready(function () {
    showViewBystatus();
    changeStatusByUrl();
});

/**
 * 开启任务事件监听器
 * 如果是已经点击了==》同意后不再提示该协议，则不需要显示
 */
function createTaskListener() {
    getDataFromStorage(LOCAL_STORAGES.READED_AGREEMENTS.key).then((value) => {
        if (value == undefined || value != READED_AGREEMENTS.READED){
            sendMessageToContentScript({cmd: "SHOW_AGREEMENT", origin: ORIGINS.POPUP}, (response) => {
                if(!chrome.runtime.lastError) {
                    console.log("SHOW_AGREEMENT SUCCESS");
                }
            });
        }else {
            //直接创建任务
            sendMessageToBackGroundScript({cmd: "CREATE_TASK", origin: ORIGINS.CONTENT}, (response) => {
                 if(!chrome.runtime.lastError) {
                    console.log("CREATE_TASK SUCCESS");
                 }
            });
        }
    });
}

/**
 * 结束任务事件监听器
 */
function stopTaskListener() {
    sendMessageToContentScript({cmd: "STOP_TASK", origin: ORIGINS.POPUP}, (response) => {
        if (!chrome.runtime.lastError) {
            console.log("STOP_TASK SUCCESS");
        }
    });
}
/**
 * 根据status的值来显示按钮的状态
 */
function showViewBystatus() {
    //getDataFromStorage("status").then((value) => {
      getDataFromStorage(LOCAL_STORAGES.STATUS.key).then((value) => {
        if (value == undefined || value == TASK_STATUS.OFF) {
            $("#stop-task-button").hide();
            $("#create-task-button").show();
        } else if (value == TASK_STATUS.ON) {
            $("#create-task-button").hide();
            $("#stop-task-button").show();
        }
    });
}

/**
 * 判断当前打开的url
 */
function changeStatusByUrl() {
    chrome.tabs.query({'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT}, function(tabs){
        var currentUrl = tabs[0].url;
        var params = /(http|https):\/\/([\w.]+\/?)\S*/;
        if (!params.test(currentUrl))
        {
            //显示灰色，按钮不可点击
            $("#popup-title").html("请打开正常URL");
            $("#create-task-button").css("background-color", "#939698");
            $("#stop-task-button").css("background-color", "#939698");
        }else {
            //currentUrl == undefined || currentUrl == "chrome://newtab/"
            //正常颜色并显示按钮
            $("#create-task-button").click(createTaskListener);
            $("#stop-task-button").click(stopTaskListener);
        }
    });
}