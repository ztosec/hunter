/*
 class命名格式为 class-hunter-up-xx-type
 id命名格式为 class-hunter-up-xx-type
 */

var content = `
        <div class="h2">一、总则</div>
        <div class="p">1.最终解释权归中通信息安全部所有</div>
        <div class="p">2.自你同意本协议后即代表你已经阅读并了解了使用规则和注意事项</div>
        <div class="h3">二、注意事项</div>
        <div class="p">1.hunter在线上环境跑容易产生脏数据，只能在测试环境使用</div>
        <div class="p">2.hunter研发的作用是用于中通系统安全检测，不可对其他互联网站点进行网络攻击，如出现此类情况，使用者负全责</div>
        <div class="p">3.线上环境时候产生脏数据和其他问题，请自行负责</div>
        <div class="p">4.自你同意本协议后,hunter有权截取你请求的任务网络请求</div>
        <div class="p" style="height: 30px"></div>
        <div class="p"></div>`;

var message = '你确认要终止本次任务?';

/**
 * 接受消息，主要作用就是弹出用户使用协议和停止任务
 * see https://blog.csdn.net/wanchupin/article/details/86485587
 */
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.cmd == "SHOW_AGREEMENT" && request.origin == ORIGINS.POPUP) {
        createDivNotice();
        showAgreement(content);
    } else if (request.cmd == "STOP_TASK" && request.origin == ORIGINS.POPUP) {
        createStopconfirm();
        showStopModal(message);
    }
    sendResponse('');
});
/**
 * 点击stop按钮后，弹出的confirm
 *
 */
function createStopconfirm() {
    var wrap_dialog = $("<div>", {
        "class": "wrap-dialog-hunter-stop hide-hunter-stop",
        "id": "wrap-dialog-hunter-stop"
    });
    var dialog = $("<div>", {"class": "dialog-hunter-stop"});
    var dialog_header = $("<div>", {"class": "dialog-hunter-stop-header"});
    var dialog_title = $("<span>", {"class": "dialog-title"}).html("任务提醒");
    dialog_header.append(dialog_title);
    var dialog_body = $("<div>", {"class": "dialog-hunter-stop-body"});
    var dialog_message = $("<span>", {"class": "dialog-message"});
    dialog_body.append(dialog_message);
    var dialog_footer = $("<div>", {"class": "dialog-hunter-stop-footer"});
    var buttom_confirm = $("<input>", {
        "type": "button",
        "class": "ant-btn-hunter-primary-stop",
        "id": "hunter-stop-confirm",
        "value": "确定"
    });
    var buttom_cancel = $("<input>", {
        "type": "button",
        "class": "ant-btn-hunter-primary-stop ml50-hunter-stop",
        "id": "hunter-stop-cancel",
        "value": "取消"
    });
    dialog_footer.append(buttom_confirm);
    dialog_footer.append(buttom_cancel);
    dialog.append(dialog_header);
    dialog.append(dialog_body);
    dialog.append(dialog_footer);
    wrap_dialog.append(dialog);
    if (document.getElementById("wrap-dialog-hunter-stop") == null) {
        $("html").append(wrap_dialog);
        // 确定按钮
        $('#hunter-stop-confirm').click(function () {
            $('.wrap-dialog-hunter-stop').addClass("hide-hunter-stop");
            chrome.runtime.sendMessage({cmd: 'STOP_TASK', origin: ORIGINS.CONTENT}, function (response) {
            });
        });
    }
}


/**
 * 创建标签并绑定css和click事件
 */
function createDivNotice() {
    var dialog_overlay = $("<div>", {id: "dialog-hunter-upp-overlay",});
    var dialog_box = $("<div>", {id: "dialog-hunter-upp-box",});
    var dialog_content = $("<div>", {id: "dialog-hunter-upp-content",});
    //<i class="fa fa-times" aria-hidden="true"></i>
    var dialog_header = $("<div>", {id: "dialog-hunter-upp-head",});
    var dialog_header_close_button = $("<div>", {id: "dialog-hunter-upp-head-button-close", "class": "dialog-hunter-upp-head-close", "style": "float: right;"});//关闭按钮
    var dialog_title = $("<div>", {id: "dialog-hunter-upp-title",});
    dialog_title.html(("用户协议"));
    dialog_header.append(dialog_header_close_button);
    dialog_header.append(dialog_title);
    var dialog_message = $("<div>", {id: "dialog-hunter-upp-message",});
    /*表示阅读该协议*/

    var dialog_agree = $("<div>", {id: "dialog-hunter-upp-agree",});
    //show_agreement 同意之后不再显示该协议
    var dialog_agree_check_area = $("<div>", {id: "dialog-hunter-upp-area-div",});
    var dialog_agree_check = $("<input>", {id: "hunter-upp-agree-checkbox", type: "checkbox"});
    dialog_agree_check_area.append(dialog_agree_check);
    dialog_agree_check_area.append(document.createTextNode("不再提示该协议，如想提示只能卸载重装插件"));
    var dialog_agree_button = $("<button>", {id: "hunter-upp-agree-button", "class": "ant-btn-primary-start"});//我已阅读并同意按钮
    dialog_content.append(dialog_message);
    dialog_box.append(dialog_header);
    dialog_box.append(dialog_content);
    dialog_agree.append(dialog_agree_check_area);//同意之后不再显示该协议
    dialog_agree.append(dialog_agree_button);//我已阅读并同意按钮
    dialog_agree_button.append(document.createTextNode("我已阅读并同意协议"));
    dialog_box.append(dialog_agree);
    if (document.getElementById("dialog-hunter-upp-overlay") == null) {
        $("html").append(dialog_overlay);
    }
    if (document.getElementById("dialog-hunter-upp-box") == null) {
        $("html").append(dialog_box);
        //同意之后不再提示该协议
        $('#hunter-upp-agree-checkbox').click(function () {
            if ($(this).attr('checked') == 'checked') {
                $(this).removeAttr('checked');
            } else {
                $(this).attr('checked', 'checked');
            }
            return true;
        });
        //点击同意按钮
        $('#hunter-upp-agree-button').click(function () {
            if ($("#hunter-upp-agree-checkbox").attr('checked') == "checked"){
                //saveDataToStorage("CHECKED_AGREEMENTS", CHECKED_AGREEMENTS.CHECKED);////已经勾选同意过
                saveDataToStorage(LOCAL_STORAGES.READED_AGREEMENTS.key, READED_AGREEMENTS.READED);////已经勾选同意过
            }
            $('#dialog-hunter-upp-overlay, #dialog-hunter-upp-box').hide();
                //chrome.runtime.sendMessage({cmd: "CREATE_TASK", origin: ORIGINS.CONTENT}, function (response) {
            //});
            sendMessageToBackGroundScript({"cmd": "CREATE_TASK", "origin":ORIGINS.CONTENT}, (responnse)=>{});
            return true;
        });
        //关闭弹窗事件
        $('#dialog-hunter-upp-head-button-close').click(function () {
         $('#dialog-hunter-upp-overlay, #dialog-hunter-upp-box').hide();
         return false;
         });
    }

}

/**
 * 展现用户协议
 * @param message
 */
function showAgreement(message) {

    // get the screen height and width
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();

    // calculate the values for center alignment
    var dialogHeight = $('#dialog-hunter-upp-box').outerHeight();
    var dialogWidth = $('#dialog-hunter-upp-box').outerWidth();

    // assign values to the overlay and dialog box
    $('#dialog-hunter-upp-overlay').css({height: maskHeight, width: maskWidth}).show();
    $('#dialog-hunter-upp-box').css({
        "top": "10%",
        "margin-left": maskWidth * 0.25,
        "width": maskWidth * 0.5,
        "position": "fixed",
        "box-sizing": "content-box",
    }).show();

    // display the message
    $('#dialog-hunter-upp-message').html(message);

}
/**
 * 显示stop按钮
 * @param message
 */
function showStopModal(message) {
    if (message) {
        $('.dialog-message').html(message);
    }
    // 显示遮罩和对话框
    $('.wrap-dialog-hunter-stop').removeClass("hide-hunter-stop");
    // 取消按钮
    $('#hunter-stop-cancel').click(function () {
        $('.wrap-dialog-hunter-stop').addClass("hide-hunter-stop");
    });
}