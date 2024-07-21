# Команда для запуску: python task_1.py /path/to/source_folder /path/to/output_folder

import os
import shutil
import argparse
import asyncio
import logging
from aiofiles import open as aio_open
from aiofiles.os import listdir as aio_listdir, mkdir as aio_mkdir
from aiofiles.ospath import isfile as aio_isfile, isdir as aio_isdir

# Налаштування логування
logging.basicConfig(filename='file_sorter.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')


# Асинхронна функція для копіювання файлів
async def copy_file(src_path, dest_folder):
    try:
        # Перевірка чи існує папка призначення, якщо ні - створення
        if not await aio_isdir(dest_folder):
            await aio_mkdir(dest_folder)

        dest_path = os.path.join(dest_folder, os.path.basename(src_path))

        async with aio_open(src_path, 'rb') as src_file, aio_open(dest_path, 'wb') as dest_file:
            while True:
                chunk = await src_file.read(1024)
                if not chunk:
                    break
                await dest_file.write(chunk)
    except Exception as e:
        logging.error(f"Failed to copy {src_path} to {dest_folder}: {e}")


# Асинхронна функція для рекурсивного читання папок та сортування файлів
async def read_folder(src_folder, dest_folder):
    try:
        for entry in await aio_listdir(src_folder):
            src_path = os.path.join(src_folder, entry)
            if await aio_isfile(src_path):
                file_ext = os.path.splitext(entry)[1].lstrip('.').lower()
                if file_ext:
                    target_folder = os.path.join(dest_folder, file_ext)
                    await copy_file(src_path, target_folder)
            elif await aio_isdir(src_path):
                await read_folder(src_path, dest_folder)
    except Exception as e:
        logging.error(f"Failed to read folder {src_folder}: {e}")


async def main(source_folder, output_folder):
    await read_folder(source_folder, output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sort files by extension.')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')
    parser.add_argument('output_folder', type=str, help='Path to the destination folder')
    args = parser.parse_args()

    # Запуск асинхронного головного блоку
    asyncio.run(main(args.source_folder, args.output_folder))
