from libs import DataSummarize as DataSum
import pprint

# サンプルデータ（結果、名前、日付）
data = [
    ["Pass", "Alice", "2023-01-01"],
    ["", "Bob", "2023-01-01"],
    ["Fixed", "Charlie", "2023-01-01"],
    ["Pass", "Dave", "2023-01-02"],
    ["Fixed", "Eve", "2023-01-02"],
    ["", "Frank", "2023-01-02"],
    ["Pass", "Grace", None],
    ["Fail", "Hank", "2023-01-03"],
    ["Pass", "Ivy", "2023-01-03"],
    ["Pass", "John", "2023-01-04"],
    ["Fixed", "John", "2023-01-04"],
    ["", "Leo", "2023-01-04"],
    ["Pass", "Mia", "2023-01-05"],
    ["Fixed", "Nina", "2023-01-05"],
    ["Fail", "Oscar", "2023-01-05"],
    ["Pass", "Paul", "2023-01-06"],
    ["", "Quinn", "2023-01-06"],
    ["Fixed", "Rose", ""],
]

pprint.pprint(DataSum.get_daily_filtered(data, filter=["Pass", "Fixed"]))

print("")

pprint.pprint(DataSum.get_daily_filled_by_name(data))
