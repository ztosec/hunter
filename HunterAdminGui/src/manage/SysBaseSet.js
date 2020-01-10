import React, {Component} from 'react';
import {request, STATUS_CODES} from '../utils/request';
import SysEmailSetForm from './SysEmailSet';
import SysProxyBaseSetForm from './SysProxySet';
import {Col, Row, Collapse, Card, Tooltip, Icon, Form, Input, Button, Checkbox, message} from 'antd';

const {TextArea} = Input;

/**
 * 设置黑白名单抓取规则规则，socketlog地址等
 */
export default class SysBaseSetPage extends Component {

    render() {
        const WrappedSysBaseSetForm = Form.create({name: 'SysBaseSet'})(WebBaseSetForm);
        const WrappedSysEmailSetForm = Form.create({name: 'SysEmailSet'})(SysEmailSetForm);
        const WrappedSysProxySetForm = Form.create({name: 'SysProxySet'})(SysProxyBaseSetForm);
        return (
            <div>
                <Row>
                    <Col span={2}/>
                    <Col span={20}>
                        <Card title="基础设置">
                            < WrappedSysBaseSetForm />
                        </Card>
                    </Col>
                    <Col span={2}/>
                </Row>
                <br/>
                <Row>
                    <Col span={2}/>
                    <Col span={20}>
                        <Card title="邮件设置">
                            < WrappedSysEmailSetForm />
                        </Card>
                    </Col>
                    <Col span={2}/>
                </Row>
                <br/>
                <Row>
                    <Col span={2}/>
                    <Col span={20}>
                        <Card title="网络代理设置">
                            < WrappedSysProxySetForm />
                        </Card>
                    </Col>
                    <Col span={2}/>
                </Row>
            </div>
        );
    }
}

/**
 * 后台设置表单，发送保存请求
 */
class WebBaseSetForm extends Component {
    /**
     * 构造
     * @param props
     */
    constructor(props) {
        super(props);
        this._isMounted = true;
        this.state = {
            noticeMessage: '',
        };
    }

    /**
     * 刷新加载时
     */
    componentWillMount() {
        this.onLoadData();

    };

    /**
     * 卸载时
     */
    componentWillUnmount() {
        this._isMounted = false;
    };

    /**
     * 加载数据
     */
    async onLoadData() {
        const result = await request("/admin/setting/base/", false);
        this.props.form.setFieldsValue(result.data);
    }

    /**
     * 发送数据
     */
    async putData(values) {
        await request("/admin/setting/base/", true, {method: 'PUT', body: JSON.stringify(values)});
    };

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                console.log('Received values of form: ', values);
                this.putData(values);
            }
        });
    };

    render() {
        const {getFieldDecorator} = this.props.form;
        const data = this.state;
        console.log(data);
        const formItemLayout = {
            labelCol: {
                xs: {span: 8},
                sm: {span: 4},
            },
            wrapperCol: {
                xs: {span: 12},
                sm: {span: 16},
            },
        };
        return (
            <Form onSubmit={this.handleSubmit} {...formItemLayout}>
                <Form.Item label="系统公告">
                    {getFieldDecorator('notice_message', {
                        initialValue: data.noticeMessage,
                        rules: [{required: true, message: '请输入系统通知!'}],
                    })(
                        <TextArea rows={4} placeholder="发放系统banner通知，不想显示可以用null"></TextArea>,
                    )}
                    <br/>
                    <Button type="primary" htmlType="submit" style={{width: '100%'}}>
                        提交保存
                    </Button>
                </Form.Item>
            </Form>
        )
    }

}