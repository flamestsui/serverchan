import functools
import logging
import requests
import json
from typing import Any
import re

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.notify import (
    BaseNotificationService,
    DOMAIN as NOTIFY_DOMAIN,
)


DOMAIN = "serverchan"
CONF_SENDKEY = "sendkey"
SERVICE_SENDMESSAGE = "sendmessage"

_LOGGER = logging.getLogger(__name__)

# 通知服务实现
class WxPusherNotificationService(BaseNotificationService):
    def __init__(self, sendkey: str):
        self._sendkey = sendkey
        self._api_url = self.get_url(sendkey)
        _LOGGER.debug(f"服务初始化:sendkey={sendkey[:4]}****")
        
    def get_url(self, sendkey: str):
        # 判断 sendkey 是否以'sctp' 开头，并提取数字构成URL
        if sendkey.startswith('sctp'):
            match = re.match(r'sctp(\d+)t', sendkey)
            if match:
                num = match.group(1)
                url = f'https://{num}.push.ft07.com/send/{sendkey}.send'
            else:
                raise ValueError('Invalid sendkey format for sctp')
        else:
            url = f'https://sctapi.ftqq.com/{sendkey}.send'
        return url

    def send_message(self, title: str, desp: str = "", options=None):
        if options is None:
            options = {}
        params = {
            'title': title,
            'desp': desp,
            **options
        }
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }

        try:
            response = requests.post(self._api_url, json=params, headers=headers)
            # 强制打印原始响应文本（关键：无论是否JSON，先看内容）
            # _LOGGER.error(f"API原始响应:{response.text}")  # 临时添加，用于调试
            
            result = response.json()
            # 处理响应
            if isinstance(result, list):
                _LOGGER.error(f"API返回列表（错误）:{result} 请核对sendkey")
            elif isinstance(result, dict):
                if result.get("code") == 0:
                    _LOGGER.debug("发送成功")
                elif result.get("code") == 10001:
                    _LOGGER.error(f"发送失败:{result.get('error')} 请核对sendkey")
                else:
                    _LOGGER.error(f"发送失败:{result}")
            else:
                _LOGGER.error(f"未知格式:{type(result)}")

        except Exception as e:
            _LOGGER.error(f"发送异常:{str(e)}")



# 配置页加载（直接注册服务）
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    service = WxPusherNotificationService(
        entry.data[CONF_SENDKEY]
    )

    # 修正后的服务处理函数
    async def async_handle_service(call: ServiceCall) -> None:
        title = call.data.get("title", "")
        desp = call.data.get("message", "")
        options = call.data.get("options", {})
        # 用partial绑定所有参数（包括关键字参数）
        send_func = functools.partial(
            service.send_message,
            title=title,
            desp=desp,
            options=options
        )
        
        # 只传绑定后的函数给async_add_job
        await hass.async_add_executor_job(send_func)

    # 注册通知服务 (notify.serverchan)
    hass.services.async_register(NOTIFY_DOMAIN, DOMAIN, async_handle_service)
    
    # 注册开发者动作服务 (serverchan.sendmessage)
    hass.services.async_register(DOMAIN, SERVICE_SENDMESSAGE, async_handle_service)
    
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    return True


# 配置页卸载（注销服务）
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.services.async_remove(NOTIFY_DOMAIN, DOMAIN)
    hass.services.async_remove(DOMAIN, SERVICE_SENDMESSAGE)
    return True


# 配置更新时重新加载
async def async_update_options(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_reload(entry.entry_id)
