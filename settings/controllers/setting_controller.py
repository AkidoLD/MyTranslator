from dataclasses import dataclass
import tkinter
import uuid
from dataclasses import dataclass
from tkinter import Button, Widget, Misc, Frame, Label
from typing import Type, Dict, Tuple

from settings.domain.models.base_config import BaseConfig
from settings.domain.models.config_group import ConfigGroup
from settings.ui.components.config_button import ConfigButton
from settings.ui.components.config_group_widget import ConfigGroupWidget
from settings.ui.setting_frame import SettingFrame
from shared.ui.components.circle_widget import CircleWidget
from shared.ui.components.menu_stack import MenuStack


class SettingController:
    _CONFIG_BTN_KEY = "config_btn"
    _CONFIG_VIEW_KEY = "config_view"

    def __init__(self, setting_frame: MenuStack):
        if not isinstance(setting_frame, MenuStack):
            raise TypeError(f"setting frame must be MenuStack, got type {type(setting_frame).__name__}")
        #
        self._configs : Dict[str: Tuple[Button, Widget]] = {}
        #
        self._setting_frame = setting_frame
        #
        item = self._setting_frame.add_menu("default", "",Frame)
        Label(
            item,
            text="Aucune option selectionnee.",
            anchor="center",
            background="white",
            font=("", 16, "bold")
        ).pack(fill="both", expand=True, anchor="center")

    def _get_btn_master(self, group_id : str) -> Widget :
        item : dict = self._configs.get(group_id)
        if not item : return self.config_list_pane
        #
        c_btn = item.get(self._CONFIG_BTN_KEY)
        if not c_btn :
            raise RuntimeError(f"unable to retrieve the config btn on configs map.")

        #Check if is a ConfigGroupWidget
        if not isinstance(c_btn, ConfigGroupWidget):
            raise RuntimeError(f"widget with id {group_id} is not a ConfigGroupWidget")
        #
        return c_btn.pane

    def add_configuration(self, config: Type[BaseConfig], view_class : Type[Widget] = None, **kwargs) -> Widget :
        if not isinstance(config, BaseConfig):
            raise TypeError(f"config must be BaseConfig, got class {type(config).__name__}")
        #
        if view_class and not issubclass(view_class, Widget):
            raise TypeError(f"view_class must be subclass of Widget, got class {type(view_class).__name__}")
        #
        c_btn = self._add_config_btn(config)
        #
        view = None
        if view_class :
            view = self._configs_stack.add_item(config.id, view_class)
            print(f"La vue de {config.title} a ete cree.")
            #
            btn = c_btn if isinstance(c_btn, ConfigButton) else c_btn.btn
            btn.bind("<Button-1>", lambda e : self._configs_stack.raise_item(config.id), "+")
        #
        self._configs[config.id] = {
            self._CONFIG_VIEW_KEY : view,
            self._CONFIG_BTN_KEY : c_btn
        }
        #
        return view

    def _add_config_btn(self, config : BaseConfig | Type[BaseConfig]) -> ConfigButton | ConfigGroupWidget:
        if not isinstance(config, BaseConfig):
            raise TypeError(f"config must be BaseConfig, got type {type(config).__name__}")

        master = self._get_btn_master(config.group_id)
        #
        #Get the correct widget class
        config_btn_cls = ConfigButton if not isinstance(config, ConfigGroup) else ConfigGroupWidget
        config_btn = config_btn_cls(master, text=config.title)
        #
        config_btn.pack(side="top", fill='x', pady=1)
        #
        return config_btn

    def remove_configuration(self, config_id : str):
        if not isinstance(config_id, str) or not config_id.strip(): return
        #
        config : Dict[str : Widget] = self._configs.get(config_id, None)
        #
        if config is None :
            print(f"No configuration with id {config_id} found")
            return
        #
        if not isinstance(config, dict) :
            print(f"config must be dict, got type {type(config).__name__}")
            return
        #
        view : Widget = config.get(self._CONFIG_VIEW_KEY)
        c_btn : Widget = config.get(self._CONFIG_BTN_KEY)

        if view :
            self._configs_stack.remove_child(config_id)
            view.destroy()
        if c_btn :
            c_btn.destroy()

        #
        self._configs.pop(config_id)

    ##################################### GETTERS AND SETTERS #############################################
    @property
    def config_list_pane(self):
        return self._configs_list_pane


if __name__ == "__main__" :
    root = tkinter.Tk()
    root.geometry("500x500")
    setting = SettingFrame(root)
    controller = SettingController(setting)
    #
    app_conf_group = ConfigGroup("Application")
    trans_conf_group = ConfigGroup("Translation")
    #
    #
    app_theme_conf = BaseConfig("Theme", app_conf_group.id)
    app_lang_conf = BaseConfig("Language", app_conf_group.id)
    #
    app_view = controller.add_configuration(app_conf_group, Frame)
    theme_view = controller.add_configuration(app_theme_conf, Frame)
    lang_view = controller.add_configuration(app_lang_conf, Frame, background="cyan")
    #
    trans_view = controller.add_configuration(trans_conf_group, Frame)
    #
    Button(app_view, command=lambda : controller.remove_configuration(app_theme_conf.id), text="Remove theme option").pack(side="top", fill="x")
    #
    Label(trans_view, text="Ceci est la vue de traduction").pack(fill="both", expand=True)
    #
    for color in ["blue", "red", "yellow", "orange", "pink"] :
        CircleWidget(theme_view, 50, color).pack(side="top", fill="x", anchor="center", pady=10)
    #
    setting.pack(fill="both", expand=True)
    root.mainloop()
