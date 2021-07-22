from models import Groups, Series
import yadisk
import requests
import json


def group_saver(group_name: str) -> bool:
    if group_name:
        group = Groups.add(group_name)
        upload_data_base()
        return True
    return False


def series_saver(series_name: str,group_name: str) -> bool:
    if group_name and series_name:
        series = Series.add_series(series_name, group_name)
        upload_data_base()
        return True
    return False


def show_res_by_search_text(name_table, search_text: str):
    if name_table == "series":
        return [tuple([series.name, series.groups.name, series.id]) for series in
                Series.find_by_series_name(search_text)]
    elif name_table == "groups":
        return [tuple([group.name, ', '.join([series.name for series in group.series]), group.id]) for group in
                Groups.find_by_group_name(search_text)]


def show_res_all():
    return [tuple([group.name, ', '.join([series.name for series in group.series]), group.id]) for group in
            Groups.show_all()]


def del_group_by_id(group_id):
    if Groups.del_group_by_id(group_id):
        upload_data_base()
        return True
    return False


def del_series_by_id(series_id):
    if Series.del_series_by_id(series_id):
        upload_data_base()
        return True
    return False


def show_groups():
    return [tuple([group.name, group.id]) for group in
            Groups.show_groups()]


def show_series_by_id(group_id):
    return [tuple([series.name, series.id]) for series in
            Series.show_series_by_id(group_id)]

def upload_data_base():
    y = yadisk.YaDisk(token="AQAAAAAVrSMfAAdA3XzLeOPEe04OkBNeOzOz9Rs")
    y.get_disk_info()
    with open("SquillSeries.sqlite", "w") as f:
        y.upload(f, "/SQ_BD/SquillSeries.sqlite")


def update_db_series():
    response = requests.get("https://kinobd.ru/api/films?page=1")
    res = json.loads(response.text)

    while res['next_page_url'] != None:
        print(res['current_page'])
        for movie in res['data']:
            if movie['type'] == 'serial':
                genres = ''
                for genre in movie['genres']:
                    if len(genres) == 0:
                        genres += genre['name_ru']
                    else:
                        genres += ", " + genre['name_ru']
                try:
                    if movie['raiting_imdb'] == None:
                        movie['raiting_imdb'] = 0
                    if movie['raiting_kp'] == None:
                        movie['raiting_kp'] = 0
                    series = Series.add_series(movie['name_russian'],
                                               0,
                                               movie['kinopoisk_id'],
                                               movie['year'],
                                               movie['raiting_imdb'],
                                               movie['raiting_kp'],
                                               genres)
                except:
                    if movie['rating_imdb'] == None:
                        movie['rating_imdb'] = 0
                    if movie['rating_kp'] == None:
                        movie['rating_kp'] = 0
                    series = Series.add_series(movie['name_russian'],
                                               0,
                                               movie['kinopoisk_id'],
                                               movie['year'],
                                               movie['rating_imdb'],
                                               movie['rating_kp'],
                                               genres)

        response = requests.get(res['next_page_url'])
        res = json.loads(response.text)