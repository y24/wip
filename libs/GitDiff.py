import subprocess
import re
from collections import defaultdict

def gen_diff_command(commit_from:str, commit_to:str, extensions:list[str], exclude_paths:list[str]):
    # ベースコマンド
    command = ['git', 'diff', f'{commit_from}..{commit_to}', '--unified=0']

    # 拡張子
    if extensions:
        ext_filters = [f"*.{ext}" for ext in extensions]
        command.extend(["--", *ext_filters])

    # 除外するパス
    if exclude_paths:
        for path in exclude_paths:
            command.append(f":(exclude){path}")

    return command


def get_git_diff(command):
    """
    Git diff の結果を取得します。
    """
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, encoding='utf-8')
        return result.stdout
    except Exception as e:
        print(f"Error running git diff: {e}")
        return None

def parse_git_diff(diff_output):
    """
    Git diff の出力を解析し、変更行数をファイル単位でカウントします。
    空行や空白のみの行の追加・削除はカウントしません。
    """
    file_stats = defaultdict(lambda: {'added': 0, 'deleted': 0, 'modified': 0})
    current_file = None

    lines = diff_output.splitlines()
    for line in lines:
        # ファイルの変更を示す行を検出
        if line.startswith('diff --git'):
            match = re.search(r'b/(.+)$', line)
            if match:
                current_file = match.group(1)
            continue

        # 行番号の変更（@@ -X,Y +A,B @@）を検出
        if line.startswith('@@'):
            continue

        # 削除行 (- で始まる行)
        if line.startswith('-') and not line.startswith('---'):
            if current_file and not line.strip('-').strip():
                # 空行の場合は無視
                continue
            if current_file:
                file_stats[current_file]['deleted'] += 1

        # 追加行 (+ で始まる行)
        if line.startswith('+') and not line.startswith('+++'):
            if current_file and not line.strip('+').strip():
                # 空行の場合は無視
                continue
            if current_file:
                file_stats[current_file]['added'] += 1

    # 変更を計算する
    for file, stats in file_stats.items():
        # 削除と追加が同数の場合、それを変更としてカウント
        matched_changes = min(stats['added'], stats['deleted'])
        stats['modified'] = matched_changes
        stats['added'] -= matched_changes
        stats['deleted'] -= matched_changes

    return file_stats

def print_stats(file_stats):
    """
    ファイル単位での差分結果を出力します。
    """
    print(f"{'File':<30} {'Added':<10} {'Deleted':<10} {'Modified':<10}")
    print("-" * 60)
    for file, stats in sorted(file_stats.items()):
        print(f"{file:<30} {stats['added']:<10} {stats['deleted']:<10} {stats['modified']:<10}")


if __name__ == "__main__":
    command = gen_diff_command(commit_from="38acf71", commit_to="1f676a1", extensions=["py","bat","ini"])
    diff_output = get_git_diff(command)
    if diff_output:
        file_stats = parse_git_diff(diff_output)
        print_stats(file_stats)
    else:
        print("Failed to get git diff output.")