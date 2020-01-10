/**
 * Created by b5mali4 on 2019/3/11.
 * 公共函数
 */

var TASK_STATUS = {"ON":"on", "OFF": "off"};//任务状态，决定了按钮的颜色
var ORIGINS = {"POPUP": "popup", "CONTENT": "content-script", "BACKGROUND": "background", "SETTING": "settinng"};//origin源
var READED_AGREEMENTS = {"READED": "true", "UNREADED": "false"};
var DOMAIN = "127.0.0.1";
var API_HOST = `http://${DOMAIN}:8888`;
const API_PREFIX = "/api/";
const API_VERSION = "v1";
var TIME_OUT = 10*1000;
var HOST_NAME = "http://127.0.0.1:3000";

//储存到localstorage中的所有字段名字和值(枚举类型)
var LOCAL_STORAGES = {
    "STATUS": {"key": "status", "value": TASK_STATUS.OFF},
    "TASK_ID": {"key": "task_id", "value": undefined},
    "TASK_ACCESS_KEY": {"key": "task_access_key", "value": undefined},
    "FILTER_SITE": {"key": "filter_site", "value": ""},
    "RECEIVER_EMAIL": {"key": "receiver_email", "value": undefined},
    "TASK_NAME": {"key": "task_name", "value": undefined},
    "READED_AGREEMENTS": {"key": "readed_agreements", "value": READED_AGREEMENTS.UNREADED},
};

/**
 * 切换到插件初始化状态，插件为off状态
 * 1.所有字段变成初始化状态
 * 2.图标变成待运行状态
 * 2.移除所有监听器
 */
function switchOffStatus() {
    saveDataToStorage(LOCAL_STORAGES.STATUS.key, TASK_STATUS.OFF);
    saveDataToStorage(LOCAL_STORAGES.TASK_ID.key, undefined);
    saveDataToStorage(LOCAL_STORAGES.TASK_ACCESS_KEY.key, LOCAL_STORAGES.TASK_ACCESS_KEY.value);
    saveDataToStorage(LOCAL_STORAGES.FILTER_SITE.key, undefined);
    saveDataToStorage(LOCAL_STORAGES.RECEIVER_EMAIL.key, undefined);
    saveDataToStorage(LOCAL_STORAGES.TASK_NAME.key, undefined);
    //saveDataToStorage(LOCAL_STORAGES.READED_AGREEMENTS.key, READED_AGREEMENTS.READED);
    chrome.browserAction.setIcon({path: 'images/logo_off.png'});//更换logo
    //移除监听器,第一次安装的时候移除会出错
    sendMessageToBackGroundScript({"cmd": "REMOVE_LISTENER", "origin":ORIGINS.SETTING}, (responnse)=>{
        if(!chrome.runtime.lastError){
            console.log("REMOVE_LISTENER SUCCESS");
        }
    });
    //chrome.webRequest.onBeforeRequest.removeListener(HookonBeforeRequest);
    //chrome.webRequest.onBeforeSendHeaders.removeListener(HookonBeforeSendHeaders);
}

/**
 * 切换到开启状态
 * 1.图标变成待运行状态
 * 2.激活所有监听器
 */
function switchOnStatus() {
    chrome.browserAction.setIcon({path: 'images/logo_on.png'});//更换logo
    //激活background监听器
    sendMessageToBackGroundScript({"cmd": "CONTINUE_TASK", "origin":ORIGINS.SETTING}, (responnse)=>{
        if(!chrome.runtime.lastError){
            console.log("CONTINUE_TASK SUCCESS");
        }
    });
}

/**
 * 保存值到Storage中
 * @param field
 * @param value
 */
function saveDataToStorage(field, value) {
    var data = {};
    data[field] = value;
    chrome.storage.local.set(data, function () {
        if (chrome.runtime.error) {
            console.log("Runtime error.");
        }
    });
}

/**
 * 根据字段名字从本地储存中获取数据
 * @param field
 */
function getDataFromStorage(field) {
    return new Promise((resolve, reject) => {
            chrome.storage.local.get(field, function (items) {
            if (!chrome.runtime.error) {
                resolve(items[field]);
            }
        });
});}

/**
 * 发送消息给ContentScript
 * @param message
 * @param callback
 */
function sendMessageToContentScript(message, callback) {
    chrome.tabs.query({active: true, currentWindow: true}, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, message, function (response) {
            if (callback) callback(response);
        });
    });
}

/**
 *  发送消息给background
 * @param message
 * @param callback
 */
function sendMessageToBackGroundScript(message, callback) {
    chrome.runtime.sendMessage(message, function (response) {
        if (callback) callback(response);
    });
}
