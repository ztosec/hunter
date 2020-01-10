/**
 * Created by b5mali4 on 2019/3/12.
 */
chrome.devtools.panels.create("hunter", "../images/logo.png", "panel.html", function(panel){
    //加载成功之后的回调
    console.log("hunter devTool加载panel成功");
});
