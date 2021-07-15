from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import IRightBody, TwoLineAvatarIconListItem
import models
from actions import group_saver, show_res_by_search_text, show_res_all, del_by_id


class MainWindow(MDBoxLayout):
    pass


class SearchResultItem(TwoLineAvatarIconListItem):
    def __init__(self, group_id, **kwargs):
        super(SearchResultItem, self).__init__(**kwargs)
        self.group_id = group_id

    def del_series(self):
        if del_by_id(self.group_id):
            self.parent.remove_widget(self)



class RightButton(IRightBody, MDIconButton):
    pass


class MainApp(MDApp):
    def build(self):
        return MainWindow()

    def search(self, text_field_id, query):
        res = show_res_by_search_text(text_field_id, query)
        results = self.root.ids.search_results
        results.clear_widgets()
        for series in res:
            results.add_widget(
                SearchResultItem(text=f"{series[0]}", secondary_text=f"{series[1]}", group_id=series[2])
            )

    def show_all(self):
        res = show_res_all()
        results = self.root.ids.search_results
        results.clear_widgets()
        for series in res:
            results.add_widget(
                SearchResultItem(text=f"{series[0]}", secondary_text=f"{series[1]}", group_id=series[2])
            )

    def add_series(self, group_name, series_name):
        if group_saver(group_name, series_name):
            sm = self.root.ids.bottom_nav
            sm.switch_tab("screen search")


if __name__ == "__main__":
    MainApp().run()