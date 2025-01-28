import subprocess
import re
from collections import defaultdict

# コメント形式の定義（プログラミング言語別に設定）
COMMENT_PATTERNS = [
    r'^\s*#',           # Python, Shell, etc.
    r'^\s*//',          # C, C++, Java, JavaScript, etc.
    r'^\s*/\*.*\*/',    # Single-line block comment
    r'^\s*\*',          # Block comment continuation
]


def gen_diff_command(commit_from:str, commit_to:str, extensions:list[str]=None, exclude_paths:list[str]=None):
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


def is_comment_line(line):
    """
    行がコメントかどうかを判定します。
    """
    for pattern in COMMENT_PATTERNS:
        if re.match(pattern, line):
            return True
    return False


def get_diff(command):
    """
    Git diff の結果を取得します。
    """
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True, encoding='utf-8')
        return result.stdout
    except Exception as e:
        print(f"Error running git diff: {e}")
        return None


def get_sql_diff(commit_from:str, commit_to:str, exclude_paths:list[str]=None):
    """
    Execute git diff command and parse its output.
    """
    # ベースコマンド
    command = ["git", "diff", commit_from, commit_to, "--", "*.sql"]

    # 除外するパス
    if exclude_paths:
        for path in exclude_paths:
            command.append(f":(exclude){path}")

    diff_output = subprocess.check_output(command, text=True, encoding='utf-8')
    return diff_output


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
            content = line.lstrip('-').strip()
            if not content or is_comment_line(content):
                # 空行またはコメント行は無視
                continue
            if current_file:
                file_stats[current_file]['deleted'] += 1

        # 追加行 (+ で始まる行)
        if line.startswith('+') and not line.startswith('+++'):
            content = line.lstrip('+').strip()
            if not content or is_comment_line(content):
                # 空行またはコメント行は無視
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

def count_sql_statements(diff_output):
    """
    Count added, deleted, and modified SQL statements in the diff output.
    
    Args:
        diff_output (str): The output of the git diff command.

    Returns:
        dict: A dictionary with file names as keys and counts of added, deleted, 
              and modified statements as values.
    """
    statement_counts = defaultdict(lambda: {"added": 0, "deleted": 0, "modified": 0})
    
    current_file = None
    added_statements = []
    deleted_statements = []

    for line in diff_output.splitlines():
        # Detect file changes
        if line.startswith("diff --git"):
            if current_file:
                statement_counts[current_file]["added"] = len(added_statements)
                statement_counts[current_file]["deleted"] = len(deleted_statements)
                # Calculate modifications
                modified_count = len(set(added_statements) & set(deleted_statements))
                statement_counts[current_file]["modified"] = modified_count
                # Reset for next file
                added_statements.clear()
                deleted_statements.clear()
            
            current_file = re.search(r"b/(.+\.sql)", line)
            current_file = current_file.group(1) if current_file else None
        
        # Count added and deleted lines
        elif line.startswith("+") and not line.startswith("+++") and current_file:
            statements = re.findall(r"[^;]+;", line[1:])  # Extract statements ending with a semicolon
            added_statements.extend(statements)
        elif line.startswith("-") and not line.startswith("---") and current_file:
            statements = re.findall(r"[^;]+;", line[1:])
            deleted_statements.extend(statements)

    # Handle the last file in the diff output
    if current_file:
        statement_counts[current_file]["added"] = len(added_statements)
        statement_counts[current_file]["deleted"] = len(deleted_statements)
        modified_count = len(set(added_statements) & set(deleted_statements))
        statement_counts[current_file]["modified"] = modified_count

    return statement_counts


def print_stats(file_stats):
    """
    ファイル単位での差分結果を出力します。
    """
    print(f"{'File':<30} {'Added':<10} {'Deleted':<10} {'Modified':<10}")
    print("-" * 60)
    for file, stats in sorted(file_stats.items()):
        print(f"{file:<30} {stats['added']:<10} {stats['deleted']:<10} {stats['modified']:<10}")

def print_sql_statement_counts(statement_counts):
    # Print results
    for file, counts in statement_counts.items():
        print(f"File: {file}")
        print(f"  Added: {counts['added']}")
        print(f"  Deleted: {counts['deleted']}")
        print(f"  Modified: {counts['modified']}")

if __name__ == "__main__":
    command = gen_diff_command(commit_from="38acf71", commit_to="1f676a1", extensions=["py","bat","ini"])
    diff_output = get_diff(command)
    if diff_output:
        file_stats = parse_git_diff(diff_output)
        print_stats(file_stats)
    else:
        print("Failed to get git diff output.")


