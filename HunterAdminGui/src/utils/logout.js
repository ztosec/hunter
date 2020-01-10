import {host, request} from '../utils/request';
/**
 * 向sso发送一个删除session的请求
 * @returns {Promise.<void>}
 */
export default async function logout() {
    /*const response = await fetch(host + '/logout/', {
        credentials: "include",
        cache: "default",
        method: "GET",
    });*/

    const response = request('/user/logout/', true, {
        credentials: "include",
        cache: "default",
        method: "GET",
    })
    const result = await response.json();
    if (result.status === 403 || result.status === 200) {
        window.location.href = result.site;
    }
}