- # serverchan 通知集成
[![Lastest Release](https://img.shields.io/github/release/flamestsui/serverchan.svg?style=flat)](https://github.com/flamestsui/serverchan/releases)[![GitHub All Releases](https://img.shields.io/github/downloads/flamestsui/serverchan/total)](https://github.com/flamestsui/serverchan/releases)

这是一个适用于 Home Assistant 的 Server酱 通知集成，允许你通过 Server酱 服务发送通知消息到你的设备。

## 功能介绍

通过该集成，你可以在 Home Assistant 中配置 serverchan 通知服务，实现将自动化、脚本或手动触发的消息通过 serverchan 平台发送到手机、微信等终端。

## 安装方法

1. 下载本项目的所有文件
2. 将 `serverchan` 文件夹复制到 Home Assistant 的 `custom_components` 目录下
3. 重启 Home Assistant

## 配置步骤

1. 在 [serverchan 官网](https://sc3.ft07.com/) 注册账号并获取你的 Token（在个人中心可查看）
2. 在 Home Assistant 中，进入 `设置 > 设备与服务 > 集成`
3. 点击右下角 `添加集成`，搜索 `Server酱 通知`
4. 在配置表单中输入你的 serverchan Token
5. 完成配置，集成将自动创建 `notify.serverchan` 服务

## 使用方法

可以通过调用 `notify.serverchan` 服务发送通知，支持以下参数：

- `message` (必填): 通知内容
- `title` (可选): 通知标题，默认值为 "Home Assistant 通知"

### 服务调用示例

#### 手动调用（开发者工具）

```yaml
service: notify.serverchan
data:
  message: "这是一条来自Home Assistant的测试消息"
  title: "测试通知"
```

#### 在自动化中使用

```yaml
automation:
  - alias: "温度过高时发送通知"
    trigger:
      platform: numeric_state
      entity_id: sensor.temperature
      above: 30
    action:
      service: notify.serverchan
      data:
        title: "温度警告"
        message: "当前温度过高，已超过30°C"
```
#### 多渠道发送

```yaml
action: notify.serverchan
data:
  title: 测试消息
  message: 测试内容
  isBatch: true
```
## 常见问题

- **发送失败？**

  1. 检查 serverchan Token 是否正确
  2. 确认网络连接正常，Home Assistant 能够访问 `https://www.serverchan.plus`
  3. 查看 Home Assistant 日志，搜索 "serverchan" 获取详细错误信息

- **标题不生效？**

  若未指定标题或标题为空，将自动使用默认标题 "Home Assistant 通知"

## 版本信息

当前版本：1.0.1
## 更新日志

| 版本号 | 创建日期       | 更新日志            |
| ------ | -------------- | ------------------- |
| 1.0.1  | 2026年03月07日 | 新增多渠道发送 |
| 1.0.0  | 2025年11月18日 | 初始版本发布，包含核心功能 |
## 依赖

- requests>=2.25.1（Home Assistant 会自动安装）

## 文档与支持

- [项目文档](https://github.com/flamestsui/serverchan)
- 如有问题，请提交 Issue 到项目仓库