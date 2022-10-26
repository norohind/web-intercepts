from pathlib import Path
from collections import defaultdict

BASE_PATH = 'intercepts'


# As cron record:
# zstd --rm -z intercepts/*/*.json 2>&1 | grep -v "No such file or directory -- ignored" && python3 deduplication.py

def take_hash_from_name(name: str) -> str:
    return name.split('.')[2]


def remove_unique(files: dict[str, list[Path]]):
    for file_hash in tuple(files.keys()):
        files_list = files[file_hash]
        if len(files_list) == 1:
            del files[file_hash]


def main():
    for host_name in Path(BASE_PATH).iterdir():
        if host_name.is_dir():
            files: dict[str, list[Path]] = defaultdict(list)
            for intercept_file in host_name.iterdir():
                if intercept_file.is_file():
                    file_hash = take_hash_from_name(intercept_file.name)
                    files[file_hash].append(intercept_file)

            remove_unique(files)

            for duplicated_files in files.values():
                for file in duplicated_files[1:]:
                    print(f'Removing {file.name}')
                    file.unlink()


if __name__ == '__main__':
    main()
