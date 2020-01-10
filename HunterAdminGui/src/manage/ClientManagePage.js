/**
 * Created by b5mali4 on 2018/12/5.
 */
import React, {Component} from 'react';
import {Card, Icon, Avatar, Row, Col, Button, Modal, Upload, message} from 'antd';
import ProxyClientPng from "../assets/proxy-client.jpg";
import chromeClientPng from "../assets/chrome-client.png";
import {request, STATUS_CODES, host, api_prefix, api_version} from '../utils/request';
const {Meta} = Card;
/**
 * 客户端管理页面
 */
export default class ClientManagePage extends Component {
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
    state = {visible: false};

    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    handleOk = (e) => {
        this.setState({
            visible: false,
        });
    };


    handleCancel = (e) => {
        this.setState({
            visible: false,
        });
    };

    render() {
        const props = {
            name: 'file',
            multiple: false,
            action: `${host}${api_prefix}${api_version}/admin/client/`,
            withCredentials: true,
            onChange(info) {
                const {status} = info.file;
                if (status !== 'uploading') {
                    console.log(info.file, info.fileList);
                }
                if (status === 'done') {
                    message.success(`${info.file.name} file uploaded successfully.`);
                } else if (status === 'error') {
                    message.error(`${info.file.name} file upload failed.`);
                }
            },
        };
        return (
            <div>
                <Card
                    style={{width: 300}}
                    cover={
                        <img
                            alt="chrome-plugin"
                            src={chromeClientPng}
                            style={{height: 160}}
                        />
                    }
                    actions={[
                        <Button icon="cloud-upload" onClick={this.showModal}></Button>,
                        <Button icon="edit" disabled={true}></Button>,
                        <a href={`${host}${api_prefix}${api_version}/user/client/`} target="_blank">
                            <Button icon="cloud-download"></Button>
                        </a>,
                    ]}
                >
                    <Meta
                        title="chrome客户端"
                        description="下载安装chrome插件，即可使用hunter服务"
                    />
                </Card>
                <Modal
                    title="上传chrome客户端"
                    visible={this.state.visible}
                    onOk={this.handleOk}
                    onCancel={this.handleCancel}
                    width="40%"
                >
                    <Upload.Dragger {...props}>
                        <p className="ant-upload-drag-icon">
                            <Icon type="inbox"/>
                        </p>
                        <p className="ant-upload-text">点击或者拖拽文件到此处上传</p>
                        <p className="ant-upload-hint">
                            上传chrome插件将覆盖原有版本
                        </p>
                    </Upload.Dragger>
                </Modal>
            </div>
        );
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
                <Button icon="cloud-upload" disabled={true}></Button>,
                <Button icon="edit" disabled={true}></Button>,
                <Button icon="cloud-download" disabled={true}></Button>,
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
    state = {visible: false};

    showModal = () => {
        this.setState({
            visible: true,
        });
    };

    handleOk = (e) => {
        this.setState({
            visible: false,
        });
    };


    handleCancel = (e) => {
        this.setState({
            visible: false,
        });
    };

    render() {

        return (<div>
            <Card
                style={{width: 300}}
                cover={
                    <img
                        alt="chrome-plugin"
                        src={ProxyClientPng}
                        style={{height: 160}}
                    />
                }
                actions={[
                    <Button icon="cloud-upload" disabled={true}></Button>,
                    <Button icon="edit" disabled={true}></Button>,
                    <Button icon="cloud-download" disabled={true}></Button>,
                ]}
            >
                <Meta
                    title="代理根证书"
                    description="如果需要安装根证书，请设置代理之后, 访问http://hunterca/下载证书"
                />
            </Card>
        </div>);
    }
}