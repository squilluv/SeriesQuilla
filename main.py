from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import IRightBody, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import models
from actions import *


class MainWindow(MDBoxLayout):
    pass


class GroupsItems(OneLineAvatarIconListItem):
    def __init__(self, group_id, **kwargs):
        super(GroupsItems, self).__init__(**kwargs)
        self.group_id = group_id

    def del_group(self):
        if del_group_by_id(self.group_id):
            self.parent.remove_widget(self)

    def show_series_by_group(self):
        res = show_series_by_id(self.group_id)
        results = self.parent
        results.clear_widgets()
        app = MDApp.get_running_app()
        app.root.ids.toolbar.left_action_items = [["arrow-left", lambda x: app.show_groups()]]
        for group in res:
            results.add_widget(
                SeriesItems(text=f"{group[0]}", series_id=group[1])
            )


class AddGroup(MDBoxLayout):
    def add_group(self, group_name):
        if group_saver(group_name):
            Snackbar(text="Группа добавлена").open()
            res = show_groups()
            results = self.parent
            results.clear_widgets()
            for group in res:
                results.add_widget(
                    GroupsItems(text=f"{group[0]}", group_id=group[1])
                )


class AddSeries(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        res = show_groups()
        self.group_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{group[0]}",
                "height": dp(56),
                "on_release": lambda x=f"{group[0]}": self.set_item(x),
            } for group in res
        ]

        self.groups_menu = MDDropdownMenu(
            caller=self.ids.group_name,
            items=self.group_items,
            width_mult=4,
        )

        self.groups_menu.bind()

        self.group_name = ""

    def set_item(self, group_name):
        self.ids.group_name.set_item(group_name)
        self.group_name = group_name
        self.groups_menu.dismiss()

    def callback_group(self):
        self.groups_menu.open()

    def add_series(self, series_name,):
        if series_saver(series_name, self.group_name):
            Snackbar(text="Сериал добавлен").open()
            res = show_groups()
            results = self.parent
            results.clear_widgets()
            for group in res:
                results.add_widget(
                    GroupsItems(text=f"{group[0]}", group_id=group[1])
                )


class SearchBySeries(MDBoxLayout):
    def search_series(self, series_name):
        res = show_res_by_search_text("series", series_name)
        results = self.parent
        results.clear_widgets()
        for series in res:
            results.add_widget(
                SeriesItemsForSearch(text=f"{series[0]}", secondary_text=f"{series[1]}", series_id=series[2])
            )



class SeriesItems(OneLineAvatarIconListItem):
    def __init__(self, series_id, **kwargs):
        super(SeriesItems, self).__init__(**kwargs)
        self.series_id = series_id

    def del_series(self):
        if del_series_by_id(self.series_id):
            self.parent.remove_widget(self)


class SeriesItemsForSearch(TwoLineAvatarIconListItem):
    def __init__(self, series_id, **kwargs):
        super(SeriesItemsForSearch, self).__init__(**kwargs)
        self.series_id = series_id


class RightButton(IRightBody, MDIconButton):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Pink'
        self.theme_cls.accent_palette = 'Pink'
        self.theme_cls.accent_hue = '400'
        self.title = 'SeriesQuilla'

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Добавить группу",
                "height": dp(56),
                "on_release": lambda x=f"Item": self.show_group_add_widget(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Добавить сериал",
                "height": dp(56),
                "on_release": lambda x=f"Item": self.show_series_add_widget(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Найти сериал",
                "height": dp(56),
                "on_release": lambda x=f"Item": self.show_search_series_add_widget(x),
            }
        ]

        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

        return MainWindow()

    def on_start(self):
        self.show_groups()

    def show_groups(self):
        res = show_groups()
        self.root.ids.toolbar.left_action_items = [["menu", lambda x: self.callback(x)]]
        results = self.root.ids.results
        results.clear_widgets()
        for group in res:
            results.add_widget(
                GroupsItems(text=f"{group[0]}", group_id=group[1])
            )

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def show_group_add_widget(self, x):
        self.menu.dismiss()
        app = MDApp.get_running_app()
        app.root.ids.toolbar.left_action_items = [["arrow-left", lambda x: app.show_groups()]]
        results = self.root.ids.results
        results.clear_widgets()
        results.add_widget(
            AddGroup()
        )

    def show_series_add_widget(self, x):
        self.menu.dismiss()
        app = MDApp.get_running_app()
        app.root.ids.toolbar.left_action_items = [["arrow-left", lambda x: app.show_groups()]]
        results = self.root.ids.results
        results.clear_widgets()
        results.add_widget(
            AddSeries()
        )

    def show_search_series_add_widget(self, x):
        self.menu.dismiss()
        app = MDApp.get_running_app()
        app.root.ids.toolbar.left_action_items = [["arrow-left", lambda x: app.show_groups()]]
        results = self.root.ids.results
        results.clear_widgets()
        results.add_widget(
            SearchBySeries()
        )

if __name__ == "__main__":
    MainApp().run()