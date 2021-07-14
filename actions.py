from models import Groups, Series

def group_saver(group_name: str, series_name: str) -> bool:
    if group_name and series_name:
        group = Groups.add(group_name)
        series = Series.add(series_name, group)
        return True
    return False

def show_for_name(group_name: str):
    return [tuple([group.name, ', '.join([series.name for series in group.series])]) for group in Groups.find_by_group_name(group_name)]