/*
 class命名格式为 class-hunter-up-xx-type
 id命名格式为 class-hunter-up-xx-type
 */

/**
 * 加载pup.css
 */
function loadPupCss() {
    var css = `
    .ant-btn-primary-start {
            color: #fff;
            background-color: #1890ff;
            border-color: #1890ff;
            text-shadow: 0 -1px 0 rgba(0, 0, 0, 0.12);
            -webkit-box-shadow: 0 2px 0 rgba(0, 0, 0, 0.045);
            box-shadow: 0 2px 0 rgba(0, 0, 0, 0.045);
            margin-right: 8px;
            margin-bottom: 12px;
            line-height: 1.499;
            position: relative;
            display: inline-block;
            font-weight: 400;
            white-space: nowrap;
            text-align: center;
            background-image: none;
            border: 1px solid transparent;
            -webkit-box-shadow: 0 2px 0 rgba(0, 0, 0, 0.015);
            box-shadow: 0 2px 0 rgba(0, 0, 0, 0.015);
            cursor: pointer;
            -webkit-transition: all .3s cubic-bezier(.645, .045, .355, 1);
            transition: all .3s cubic-bezier(.645, .045, .355, 1);
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            -ms-touch-action: manipulation;
            touch-action: manipulation;
            height: 40px;
            padding: 0 15px;
            font-size: 14px;
            border-radius: 4px;
            color: rgba(0, 0, 0, 0.65);
            text-transform: none;
            color: #fff;
            background: #1890ff;
            margin-top: 6px;
        }
        .ant-btn-primary-start:hover {
            background-color: #0070d3;
        }
        .ant-btn-primary-start:focus {
            background-color: #0070d3;
        }
        .ant-btn-primary-start:active {
            background-color: #0070d3;
        }
    
    #dialog-hunter-upp-overlay {
            /* set it to fill the whil screen */
            width: 100%;
            height: 100%;
            /* transparency for different browsers */
            filter: alpha(opacity=50);
            -moz-opacity: 0.5;
            -khtml-opacity: 0.5;
            opacity: 0.5;
            background: #000;
            /* make sure it appear behind the dialog box but above everything else */
            position: absolute;
            top: 0;
            left: 0;
            z-index: 3000;
            /* hide it by default */
            display: none;
        }

        #dialog-hunter-upp-box {
            /* css3 drop shadow */
            -webkit-box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
            -moz-box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
            /* css3 border radius */
            -moz-border-radius: 5px;
            -webkit-border-radius: 5px;
            border-radius: 5px;
            background: #fff;
            /* styling of the dialog box, i have a fixed dimension for this demo */
            /*width: 328px;*/
            /* make sure it has the highest z-index */
            position: absolute;
            z-index: 5000;
            /* hide it by default */
            display: none;
        }

        #dialog-hunter-upp-box .dialog-hunter-upp-content {
            /* style the content */
            text-align: left;
            padding: 10px;
            margin: 13px;
            color: #666;
            font-family: arial;
            font-size: 11px;
            
            font-size: 14px;
            line-height: 1.5;
            word-wrap: break-word;
        }
        #dialog-hunter-upp-box #dialog-hunter-upp-content{
            font-size: 14px;
            line-height: 1.5;
            word-wrap: break-word;
            background: #fff;
            margin-top: 10px;
        }
        #dialog-hunter-upp-head {
        
        }
        #dialog-hunter-upp-title {
            padding: 16px 24px;
            color: rgba(0,0,0,.65);
            background: #fff;
            border-bottom: 1px solid #e8e8e8;
            border-radius: 4px 4px 0 0;
            margin: 0;
            color: rgba(0,0,0,.85);
            font-weight: 500;
            font-size: 16px;
            line-height: 22px;
        }
        
        
        #dialog-hunter-upp-message {
           /* style the message */
           font-size: 12px;
           color: rgba(0,0,0,.85);
           font-family: simsun;
           padding-left: 15px;
        }
        #dialog-hunter-upp-message .h2{
           /* style the message */
           font-size: 14px;
           color: #1d1c1c;
           font-family: simsun;
           padding-left: 15px; 
           margin-top: 0px;
        }
        #dialog-hunter-upp-message .h3{
           /* style the message */
           font-size: 13px;
           color: #1d1c1c;
           font-family: simsun;
           padding-left: 13px; 
           margin-top: 0px;
        }
        #dialog-hunter-upp-message .p{
           /* style the message */
           font-size: 13px;
           color: rgba(0,0,0,.85);
           font-family: simsun;
           padding-left: 15px;
           margin-bottom: 1px;
           line-height: 30px;
        }
        #dialog-hunter-upp-agree {
           /* style the message */
           font-size: 12px;
           color: #e40707;
           font-family: simsun;
           background: #FFFFFF;
           text-align: center;
        }
        #dialog-hunter-upp-area-div {
           font-size: 13px;
           color: rgba(0,0,0,.85);
           font-family: simsun;
           padding-left: 30px;
           margin-bottom: 1px;
           line-height: 30px;
           text-align: left;
        }
        .btn-hunter-stop {
            /* styles for button */
            margin: 10px auto 0 auto;
            text-align: center;
            background-image: linear-gradient(135deg, #90F7EC 0%, #32CCBC 100%);
            width: 50px;
            padding: 5px 10px 6px;
            color: #737171;
            text-decoration: none;
            font-weight: bold;
            -moz-border-radius: 5px;
            -webkit-border-radius: 5px;
            -webkit-box-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
            position: relative;
            cursor: pointer
        }

        .btn-hunter-stop:hover {
            background-image: linear-gradient(135deg, #30E3CA 0%, #11999E 100%);
        }

        /* extra styling */
        #dialog-hunter-upp-box .dialog-hunter-upp-content p {
            font-weight: 700;
            margin: 0;
        }

        #dialog-hunter-upp-box .dialog-hunter-upp-content ul {
            margin: 10px 0 10px 20px;
            padding: 0;
            height: 50px;
        }
        .wrap-dialog-hunter-stop {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            font-size: 16px;
            text-align: center;
            background-color: rgba(0, 0, 0, .4);
            z-index: 999;
            /*box-sizing: content-box;*/
        }
        .dialog-hunter-stop {
            position: relative;
            margin: 15% auto;
            width: 300px;
            background-color: #FFFFFF;
        }
        .dialog-hunter-stop .dialog-hunter-stop-header {
            /*height: 20px;*/
            padding: 10px;
            background-image: linear-gradient(135deg, #90F7EC 0%, #32CCBC 100%);
        }
        .dialog-hunter-stop .dialog-hunter-stop-body {
            /*height: 30px;*/
            padding: 20px;
        }
        .dialog-hunter-stop .dialog-hunter-stop-footer {
            padding: 8px;
            background-color: whitesmoke;
        }
        .dialog-hunter-stop .dialog-title {
            color: #807f7f;
        }
        .dialog-hunter-stop .dialog-message {
            color: #807f7f;
        }
        .dialog-message-hunter-stop {
            color:#fff;
        }
        .btn-hunter-stop {
            width: 70px;
            padding: 2px;
        }
        .hide-hunter-stop {
            display: none;
        }
        .ml50-hunter-stop {
            margin-left: 50px;
        }
    `;
    ($("head") || $("body")).append($("<style>").html(css));
}

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
var isLoadCss = false;

/**
 * 接受消息，主要作用就是弹出用户使用协议和停止任务
 */
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (!isLoadCss) {
        isLoadCss = true;
        loadPupCss();
    }
    if (request.cmd == "pup" && request.origin == "popup") {
        createDivNotice();
        showPup(content);
    } else if (request.cmd == "stop" && request.origin == "popup") {
        createStopconfirm();
        showStop(message);
    }
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
        "class": "btn-hunter-stop",
        "id": "hunter-stop-confirm",
        "value": "确定"
    });
    var buttom_cancel = $("<input>", {
        "type": "button",
        "class": "btn-hunter-stop ml50-hunter-stop",
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
            chrome.runtime.sendMessage({cmd: 'stop', origin: 'content-script'}, function (response) {
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
    var dialog_header = $("<div>", {id: "dialog-hunter-upp-head",});
    var dialog_title = $("<div>", {id: "dialog-hunter-upp-title",});
    dialog_title.html(("用户协议"));
    dialog_header.append(dialog_title);
    var dialog_message = $("<div>", {id: "dialog-hunter-upp-message",});
    /*表示阅读该协议*/

    var dialog_agree = $("<div>", {id: "dialog-hunter-upp-agree",});
    //show_agreement 同意之后不再显示该协议
    var dialog_agree_check_area = $("<div>", {id: "dialog-hunter-upp-area-div",});
    var dialog_agree_check = $("<input>", {id: "hunter-upp-agree-checkbox", type: "checkbox"});
    dialog_agree_check_area.append(dialog_agree_check);
    dialog_agree_check_area.append(document.createTextNode("同意后不再提示该协议"));
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
            console.log("===hunter-upp-agree-checkbox===");
            if ($(this).attr('checked') == 'checked') {
                $(this).removeAttr('checked');
            } else {
                $(this).attr('checked', 'checked');
            }
            return true;
        });
        //点击同意按钮
        $('#hunter-upp-agree-button').click(function () {
            console.log("===hunter-upp-agree-button===");
            if ($("#hunter-upp-agree-checkbox").attr('checked') == "checked"){
                //saveDataToStorage("readed", "true");//已经同意过
                saveDataToStorage(LOCAL_STORAGES.READED_AGREEMENTS.key, READED_AGREEMENTS.READED);//已经同意过
            }
            $('#dialog-hunter-upp-overlay, #dialog-hunter-upp-box').hide();
                chrome.runtime.sendMessage({cmd: 'start', origin: 'content-script'}, function (response) {
            });
            return true;
        });
        //关闭弹窗事件
        $('#dialog-hunter-upp-title, #dialog-hunter-upp-content').click(function () {
         $('#dialog-hunter-upp-overlay, #dialog-hunter-upp-box').hide();
         return false;
         });
    }

}

/**
 * 展现用户协议
 * @param message
 */
function showPup(message) {

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
function showStop(message) {
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
    });
}