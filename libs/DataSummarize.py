from collections import defaultdict

def get_daily_filtered(data, filter=[str]):
    result_count = defaultdict(int)

    # 日付が空の行は削除
    data = [row for row in data if len(row) > 2 and row[2] not in ("", None)]

    # 結果がPassまたはFixedの行を日付ごとにカウント
    for row in data:
        result, _, date = row
        if result in filter:
            result_count[date] += 1

    # 結果を返却
    result = []
    for date, count in sorted(result_count.items()):
        result.append([date, count])
    return result

def get_daily_filled_by_name(data):
    date_name_count = defaultdict(lambda: defaultdict(int))

    # 日付が空の行は削除
    data = [row for row in data if len(row) > 2 and row[2] not in ("", None)]

    # 結果が空ではない行を日付および名前ごとにカウント
    for row in data:
        result, name, date = row
        if result:  # 結果が空ではない場合
            date_name_count[date][name] += 1

    # 集計結果を返却
    result = []
    for date, name_counts in sorted(date_name_count.items()):
        dict = {}
        daily_count = []
        dict["date"] = date
        for name, count in sorted(name_counts.items()):
            daily_count.append({"name": name, "count":count})
        dict["results"] = daily_count
        result.append(dict)
    return result
