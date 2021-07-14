from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import IRightBody, TwoLineAvatarIconListItem
import models
from actions import group_saver, show_for_name


class MainWindow(MDBoxLayout):
    pass


class SearchResultItem(TwoLineAvatarIconListItem):
    pass


class RightButton(IRightBody, MDIconButton):
    pass


class MainApp(MDApp):
    def build(self):
        return MainWindow()

    def search_series(self, query):
        res = show_for_name(query)
        app = MDApp.get_running_app()
        results = app.root.ids.search_results
        for series in res:
            results.add_widget(
                SearchResultItem(text="text", secondary_text="text 2")
            )

    def add_series(self, group_name, series_name):
        if group_saver(group_name, series_name):
            app = MDApp.get_running_app()
            sm = app.root.ids.bottom_nav
            sm.switch_tab("screen search")


if __name__ == "__main__":
    MainApp().run()