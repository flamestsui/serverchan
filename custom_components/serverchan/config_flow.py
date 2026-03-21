# custom_components/wxpusher/config_flow.py
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN  # 仅保留必要的导入

# 模块级别不执行任何耗时操作，日志初始化也延迟到类中

CONF_SENDKEY = "sendkey"


@config_entries.HANDLERS.register(DOMAIN)
class WxPusherConfigFlow(config_entries.ConfigFlow):
    VERSION = 1

    def __init__(self):
        # 日志初始化延迟到类实例化时（非模块级别）
        self._logger = logging.getLogger(__name__)

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input:
            if not user_input[CONF_SENDKEY]:
                errors[CONF_SENDKEY] = "missing_sendkey"
            
            if not errors:
                await self.async_set_unique_id(user_input[CONF_SENDKEY])
                self._abort_if_unique_id_configured()
                self._logger.debug("创建ServerChan配置项")
                return self.async_create_entry(title="ServerChan 通知", data=user_input)
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_SENDKEY): str,
            }),
            errors=errors
        )


class WxPusherOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry
        self._logger = logging.getLogger(__name__)

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input:
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=user_input
            )
            self._logger.debug("更新ServerChan配置项")
            return self.async_create_entry(title="", data={})

        current_data = self.config_entry.data
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_SENDKEY, default=current_data[CONF_SENDKEY]): str,
            })
        )