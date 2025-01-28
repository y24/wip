import subprocess
import argparse

def generate_git_diff_command(commit_from, commit_to, extensions=None, exclude_paths=None):
    # ベース
    command = ["git", "diff", f"{commit_from}..{commit_to}", "--stats"]

    # 拡張子
    if extensions:
        ext_filters = [f"*.{ext}" for ext in extensions]
        command.extend(["--", *ext_filters])

    # 除外するパス
    if exclude_paths:
        for path in exclude_paths:
            command.append(f":(exclude){path}")

    return " ".join(command)

def main():
    parser = argparse.ArgumentParser(description="Generate a git diff command with specific options.")
    parser.add_argument("commit_from", help="The starting commit hash")
    parser.add_argument("commit_to", help="The ending commit hash")
    parser.add_argument("--extensions", nargs="*", help="List of file extensions to include (e.g., py, js)")
    parser.add_argument("--exclude", nargs="*", help="List of directories or file names to exclude")

    args = parser.parse_args()

    # Generate the git diff command
    command = generate_git_diff_command(
        commit_from=args.commit_from,
        commit_to=args.commit_to,
        extensions=args.extensions,
        exclude_paths=args.exclude
    )

    return command
    # print(f"Generated Command: {command}")

    # Optionally execute the command
    execute = input("Do you want to execute this command? (y/n): ").strip().lower()
    if execute == 'y':
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    main()