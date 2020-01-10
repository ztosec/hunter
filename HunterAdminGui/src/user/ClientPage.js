/**
 * Created by b5mali4 on 2018/12/5.
 */
import React, {Component} from 'react';
import {Card, Icon, Avatar, Row, Col, Button} from 'antd';
import ProxyClientPng from "../assets/proxy-client.jpg";
import chromeClientPng from "../assets/chrome-client.png";
import {request, STATUS_CODES, host, api_prefix, api_version} from '../utils/request';
const {Meta} = Card;
/**
 * 用户下载页面
 */
export default class ClientDownloadPage extends Component {
    render() {
        return (
            <Row>
                <Col span={8}><ChromeClient/></Col>
                <Col span={8}><ProxyCert/></Col>
                <Col span={8}><FireFoxClient/></Col>
            </Row>
        );
    }
}
/**
 * chrome浏览器插件
 */
class ChromeClient extends Component {
    render() {
        return (<Card
            style={{width: 300}}
            cover={
                <img
                    alt="chrome-plugin"
                    src={chromeClientPng}
                    style={{height: 160}}
                />
            }
            actions={[
                <a href={`${host}${api_prefix}${api_version}/user/client/`} target="_blank">
                    <Button type="primary" shape="round" icon="download">
                        Download
                    </Button>
                </a>,
            ]}
        >
            <Meta
                title="chrome客户端"
                description="下载安装chrome插件，即可使用hunter服务"
            />
        </Card>);
    }
}
/**
 * firefox浏览器插件
 */
class FireFoxClient extends Component {
    render() {
        return (<Card
            style={{width: 300}}
            cover={
                <img
                    src=""
                    style={{height: 160}}
                />
            }
            actions={[
                <Button type="primary" shape="round" icon="download" disabled={true}>
                    Download
                </Button>,
            ]}
        >
            <Meta
                title="firefox"
                description="火狐浏览器插件暂不支持，后续版本可能会支持"
            />
        </Card>);
    }
}
/**
 * 网络代理证书
 */
class ProxyCert extends Component {
    render() {
        return (<Card
            style={{width: 300}}
            cover={
                <img
                    alt="proxy"
                    src={ProxyClientPng}
                    style={{height: 160}}
                />
            }
            actions={[
                <Button type="primary" shape="round" icon="download" disabled={true}>
                    Download
                </Button>,
            ]}
        >
            <Meta
                title="代理证书"
                description={`如果需要安装根证书，请设置代理之后, 访问http://hunterca/下载证书`}
            />
        </Card>);
    }
}