/**
 * Created by b5mali4 on 2018/7/17.
 */
//import fetch from 'whatwg-fetch';
import {message} from 'antd';


const host = "http://127.0.0.1:8888";
const api_prefix = "/api/";
const api_version = "v1";
global.host = host;


/**
 * HTTP 异步请求
 * @param url
 * @param reload 是否重新刷新页面
 * @param options
 * @returns {Promise.<*>}
 */
async function request(url, reload = false, options) {
    var fetchOptions = {credentials: "include", cache: "default",}
    var method = "get";

    if (!url.startsWith("http")) {
        url = host + api_prefix + api_version + url;
    }
    if (options !== undefined) {
        Object.keys(options).forEach(function (key) {
            fetchOptions[key] = options[key];
            if (key === "method") {
                method = options[key];
            }
        });
    }

    const response = await fetch(url, fetchOptions);
    const result = await response.json();
    //前端MSG提醒
    if (result !== undefined && reload !== undefined) {
        //reload
        if (reload) {
            if (result.status == STATUS_CODES.HTTP_OK && method !== "get") {
                if (result.data.site !== undefined) {
                    message.success(result.message).then(() => (window.location.href = result.data.site));
                } else {
                    message.success(result.message).then(() => (window.location.reload()));
                }
            } else if (result.status == STATUS_CODES.HTTP_INTERNAL_SERVER_ERROR || result.status == STATUS_CODES.HTTP_BAD_REQUEST) {
                message.error(result.message + "," + result.data.extra_info).then(() => (window.location.reload()));
            } else if (result.status == STATUS_CODES.HTTP_FORBIDDEN) {
                message.warn(result.message + "," + result.data.extra_info).then(() => (window.location.href = result.data.site));
            }
        } else {
            if (result.status == STATUS_CODES.HTTP_OK && method !== "get") {
                message.success(result.message);
            } else if (result.status == STATUS_CODES.HTTP_INTERNAL_SERVER_ERROR || result.status == STATUS_CODES.HTTP_BAD_REQUEST) {
                message.error(result.message + "," + result.data.extra_info);
            } else if (result.status == STATUS_CODES.HTTP_FORBIDDEN) {
                message.warn(result.message + "," + result.data.extra_info).then(() => (window.location.href = result.data.site));
            }
        }
    }
    return result;
}

const STATUS_CODES = {
    HTTP_OK: 200,
    HTTP_CREATED: 201,
    HTTP_NO_CONTENT: 204,
    HTTP_BAD_REQUEST: 400,
    HTTP_UNAUTHORIZED: 401,
    HTTP_FORBIDDEN: 403,
    HTTP_NOT_FOUND: 404,
    HTTP_METHOD_NOT_ALLOWED: 405,
    HTTP_CONFLICT: 409,
    HTTP_UNSUPPORTED_MEDIA_TYPE: 415,
    HTTP_INTERNAL_SERVER_ERROR: 500,
    HTTP_BAD_GATEWAY: 502,
    HTTP_SERVICE_UNAVAILABLE: 503,
};
export {request, STATUS_CODES, host, api_prefix, api_version}