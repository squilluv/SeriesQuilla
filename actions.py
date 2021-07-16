from models import Groups, Series


def group_saver(group_name: str) -> bool:
    if group_name:
        group = Groups.add(group_name)
        return True
    return False


def series_saver(series_name: str,group_name: str) -> bool:
    if group_name and series_name:
        series = Series.add_series(series_name, group_name)
        return True
    return False


def show_res_by_search_text(name_table, search_text: str):
    if name_table == "series":
        return [tuple([group.name, ', '.join([series.name for series in group.series]), group.id]) for group in
                Groups.find_by_series_name(search_text)]
    elif name_table == "groups":
        return [tuple([group.name, ', '.join([series.name for series in group.series]), group.id]) for group in
                Groups.find_by_group_name(search_text)]


def show_res_all():
    return [tuple([group.name, ', '.join([series.name for series in group.series]), group.id]) for group in
            Groups.show_all()]


def del_group_by_id(group_id):
    return Groups.del_group_by_id(group_id)


def del_series_by_id(series_id):
    return Series.del_series_by_id(series_id)


def show_groups():
    return [tuple([group.name, group.id]) for group in
            Groups.show_groups()]


def show_series_by_id(group_id):
    return [tuple([series.name, series.id]) for series in
            Series.show_series_by_id(group_id)]