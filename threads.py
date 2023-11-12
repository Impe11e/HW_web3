import logging
import concurrent.futures
from pathlib import Path
import shutil
import time
import sys

def get_extension(file_name):
    if '.' in file_name:
        extension = (file_name.split('.'))[-1]
    else:
        extension = None
    return extension

def process_file(file, dest_folder):
    file_name = file.name
    new_file_path = dest_folder / file_name
    shutil.move(str(file), str(new_file_path))
    logging.info(f'Moved file {file} to {new_file_path}')

def process_folder(src_folder, dest_folder):
    src_path = Path(src_folder)
    dest_path = Path(dest_folder)
    dest_path.mkdir(parents=True, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for item in src_path.iterdir():
            if item.is_file():
                extension = get_extension(item.name)
                if extension is None:
                    new_folder = dest_path / 'unknown'
                else:
                    new_folder = dest_path / extension

                new_folder.mkdir(parents=True, exist_ok=True)
                executor.submit(process_file, item, new_folder)
            elif item.is_dir():
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as sub_executor:
                    sub_executor.submit(process_folder, item, dest_folder)
    for item in src_path.iterdir():
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()

def main():
    src_folder = str(input("Введіть назву папки для сортування: "))
    src_path = Path(src_folder)
    if src_path.exists():
        pass
    else:
        logging.error(f"{src_path} doesn`t exist")
        sys.exit(1)
    dest_folder = str(input("Введіть назву папки куди сортувати: "))

    logging.basicConfig(format='%(threadName)s - %(asctime)s - %(message)s', level=logging.DEBUG, handlers=[logging.StreamHandler()])

    current_time = time.time()
    process_folder(src_folder, dest_folder)
    new_time = time.time()
    execution_time = new_time - current_time

    logging.info(f"Сортування завершено за {execution_time} часу")

if __name__ == "__main__":
    main()