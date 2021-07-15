from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import IRightBody, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
import models
from actions import group_saver, show_res_by_search_text, show_res_all, del_by_id, show_groups, show_series_by_id


class MainWindow(MDBoxLayout):
    pass


class GroupsItems(OneLineAvatarIconListItem):
    def __init__(self, group_id, **kwargs):
        super(GroupsItems, self).__init__(**kwargs)
        self.group_id = group_id

    def del_series(self):
        if del_by_id(self.group_id):
            self.parent.remove_widget(self)

    def show_series_by_group(self):
        res = show_series_by_id(self.group_id)
        results = self.parent
        results.clear_widgets()
        app = MDApp.get_running_app()
        app.root.ids.toolbar.left_action_items = [["arrow-left", lambda x: app.show_groups()]]
        for group in res:
            results.add_widget(
                SeriesItems(text=f"{group[0]}", secondary_text="JUSt", series_id=group[1])
            )


class SeriesItems(TwoLineAvatarIconListItem):
    def __init__(self, series_id, **kwargs):
        super(SeriesItems, self).__init__(**kwargs)
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
        return MainWindow()

    def on_start(self):
        self.show_groups()

    def show_groups(self):
        res = show_groups()
        self.root.ids.toolbar.left_action_items = [["menu", lambda x: print('hah')]]
        results = self.root.ids.results
        results.clear_widgets()
        for group in res:
            results.add_widget(
                GroupsItems(text=f"{group[0]}", group_id=group[1])
            )

    def add_series(self, group_name, series_name):
        if group_saver(group_name, series_name):
            sm = self.root.ids.bottom_nav
            sm.switch_tab("screen search")


if __name__ == "__main__":
    MainApp().run()