/**
 * Created by b5mali4 on 2018/12/5.
 */
import React, {Component} from 'react';
import {
    Table,
    Upload,
    Select,
    Row,
    Col,
    Collapse,
    Card,
    Input,
    Button,
    Switch,
    Icon,
    Form,
    Modal,
    Dropdown,
    Menu,
    Progress,
    message,
} from 'antd';
import {Redirect} from "react-router-dom";
import {WaterWave} from 'ant-design-pro/lib/Charts';
import {request, STATUS_CODES, host, api_prefix, api_version} from '../utils/request';
import {BrowserRouter as Router, Route, Link, NavLink} from "react-router-dom";
import plugin1png from '../assets/plugin1.png';
import plugin2png from '../assets/plugin2.png';
import plugin3png from '../assets/plugin3.png';
const Option = Select.Option;
const FormItem = Form.Item;
const confirm = Modal.confirm;
const {Panel} = Collapse;

//插件管理
export default class PluginManagement extends Component {
    constructor(props) {
        super(props);
        this.state = {
            checkerInfoList: [],
            hightLevelCheckerNum: 0,
            middleLevelCheckerNum: 0,
            lowLevelCheckerNum: 0,
        };
    }

    componentWillMount() {
        this.onLoadData();
    };

    /**
     * 加载当前任务 currenttasks
     * @returns {Promise.<void>}
     */
    async onLoadData() {
        const result = await request("/admin/plugins/", false);
        this.setState({
            checkerInfoList: result.data.checker_info_list,
            hightLevelCheckerNum: result.data.hight_num,
            middleLevelCheckerNum: result.data.middle_num,
            lowLevelCheckerNum: result.data.low_num,
        });

    };

    render() {
        const checkerInfoList = this.state.checkerInfoList;
        const hightLevelCheckerNum = this.state.hightLevelCheckerNum;
        const middleLevelCheckerNum = this.state.middleLevelCheckerNum;
        const lowLevelCheckerNum = this.state.lowLevelCheckerNum;

        return (
            <Row>
                {
                    //显示插件等级以及数量start
                }
                <Row style={{background: '#fff'}}>
                    <TopArea hightLevelCheckerNum={hightLevelCheckerNum} middleLevelCheckerNum={middleLevelCheckerNum}
                             lowLevelCheckerNum={lowLevelCheckerNum}> </TopArea>
                </Row>
                {
                    //显示插件等级以及数量end
                }
                {
                    //新增插件start
                }
                <Row style={{background: '#fff', marginTop: 25}}>
                    <AddPluginModal />
                </Row>
                {
                    //新增插件end
                }
                {
                    //插件信息展示start
                }
                <Row style={{marginTop: 25}}>
                    {checkerInfoList.map((item, index) => {
                        const header = (item) => (
                            <span>
                                <Icon type="bug" theme="twoTone" style={{
                                    color: "#5fc7fa",
                                    size: "12px"
                                }}/>&nbsp;{item.tag}&nbsp;{item.type}&nbsp;
                            </span>
                        );

                        /**
                         * 删除插件和禁用插件按钮
                         */
                        const genExtra = (checker_name, checked) => (
                            <Row>
                                <Switch name={checker_name} checked={checked} size="small"
                                        onChange={changePluginUseAble} checkedChildren="开" unCheckedChildren="关"/>
                                &nbsp;&nbsp;
                                <Icon name={checker_name} type="close-circle" theme="twoTone" style={{color: "#ff0100"}}
                                      onClick={deletePlugin}/>
                            </Row>
                        );

                        /**
                         * 是否禁用插件
                         * @param checker_name
                         * @param checked
                         */
                        async function deletePlugin(event) {
                            //console.log(`switch to ${checked}`);
                            const checker_name = event.target.parentNode.parentNode.getAttribute("name");
                            console.log(event.target.parentNode.parentNode);
                            console.log(checker_name);
                            await request('/admin/plugins/', true, {
                                method: "DELETE",
                                body: JSON.stringify({"name": checker_name})
                            })
                        }

                        /**
                         * 是否禁用插件
                         * @param checker_name
                         * @param checked
                         */
                        async function changePluginUseAble(checked, event) {
                            //console.log(`switch to ${checked}`);
                            var checker_name = event.target.name;
                            if (checker_name === undefined){
                                checker_name = event.target.parentNode.getAttribute("name")
                            }
                            console.log(event.target);
                            await request('/admin/plugins/', true, {
                                method: "PUT",
                                body: JSON.stringify({"name": checker_name, "switch": checked})
                            })
                        }


                        return (
                            <Col span={8} key={index}>
                                <Collapse bordered={true}>
                                    <Panel header={header(item)} key={index} extra={genExtra(item.name, item.useable)}>
                                        <div>
                                            <Icon type="code" theme="twoTone"/>&nbsp;&nbsp;{item.tag}
                                        </div>
                                        <div>
                                            <Icon type="security-scan" theme="twoTone"/>&nbsp;&nbsp;{item.name}
                                        </div>
                                        <div>
                                            <Icon type="thunderbolt" theme="twoTone"/>&nbsp;&nbsp;{item.level}
                                        </div>
                                        <div>
                                            <Icon type="tags" theme="twoTone"/>&nbsp;&nbsp;{item.imp_version}
                                        </div>
                                        <div>
                                            <Icon type="tag" theme="twoTone"/>&nbsp;&nbsp;{item.type}
                                        </div>
                                    </Panel>
                                </Collapse>
                            </Col>
                        );
                    })}
                </Row>
                {
                    //插件信息展示end
                }
            </Row>
        )
    }
}
/**
 *展示当前任务详情
 */
class TopArea extends Component {

    constructor(props) {
        super(props);
        this.props = props;
    }

    render() {
        const hightLevelCheckerNum = this.props.hightLevelCheckerNum;
        const middleLevelCheckerNum = this.props.middleLevelCheckerNum;
        const lowLevelCheckerNum = this.props.lowLevelCheckerNum;
        return (
            <Row>
                <Col span={8}>
                    <Row>
                        <Col span={12} style={{textAlign: 'right'}}>
                            <img src={plugin1png} style={{marginTop: '20px', marginBottom: '20px', width: '74px'}}/>
                        </Col>
                        <Col span={12}>
                            <div style={{
                                position: 'relative',
                                textAlign: 'center',
                                marginTop: 20,
                                marginBottom: 20,
                                borderRight: '1px solid rgb(232, 232, 232)'
                            }}>
                                <span>危害等级:高</span>
                                <p style={{
                                    color: 'rgba(0,0,0,.85)',
                                    fontSize: 24,
                                    lineHeight: 2,
                                    margin: 0
                                }}>{hightLevelCheckerNum}个插件</p>
                            </div>
                        </Col>
                    </Row>
                </Col>
                <Col span={8}>
                    <Row>
                        <Col span={12} style={{textAlign: 'right'}}>
                            <img src={plugin2png} style={{marginTop: '20px', marginBottom: '20px', width: '74px'}}/>
                        </Col>
                        <Col>
                            <div style={{
                                position: 'relative',
                                textAlign: 'center',
                                marginTop: 20,
                                marginBottom: 20,
                                borderRight: '1px solid rgb(232, 232, 232)'
                            }}>
                                <span>危害等级:中</span>
                                <p style={{
                                    color: 'rgba(0,0,0,.85)',
                                    fontSize: 24,
                                    lineHeight: 2,
                                    margin: 0
                                }}>{middleLevelCheckerNum}个插件</p>
                            </div>
                        </Col>
                    </Row>
                </Col>
                <Col span={8}>
                    <Row>
                        <Col span={12} style={{textAlign: 'right'}}>
                            <img src={plugin3png} style={{marginTop: '20px', marginBottom: '20px', width: '74px'}}/>
                        </Col>
                        <Col>
                            <div style={{position: 'relative', textAlign: 'center', marginTop: 20, marginBottom: 20}}>
                                <span>危害等级:低</span>
                                <p style={{
                                    color: 'rgba(0,0,0,.85)',
                                    fontSize: 24,
                                    lineHeight: 2,
                                    margin: 0
                                }}>{lowLevelCheckerNum}个插件</p>
                            </div>
                        </Col>
                    </Row>
                </Col>
            </Row>
        )
    }
}

/**
 * 新建上传插件模块
 */
class AddPluginModal extends Component {
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
    }

    render() {
        const state = this.state;
        const props = {
            name: 'file',
            multiple: false,
            action: `${host}${api_prefix}${api_version}/admin/plugins/`,
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
                <Button type="dashed" icon="plus" style={{width: '100%'}} onClick={this.showModal}>新增插件</Button>
                <Modal
                    title="上传新插件"
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
                            上传插件前请确保本地运行测试正常
                        </p>
                    </Upload.Dragger>
                </Modal>
            </div>
        );
    }

}

