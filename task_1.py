import os
import asyncio
import aiofiles
import logging

# Отримання абсолютного шляху до папки з програмою
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, 'file_sorter.log')

# Налаштування логування в файл
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def copy_file(src, dest):
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        async with aiofiles.open(src, 'rb') as fsrc:
            async with aiofiles.open(dest, 'wb') as fdst:
                while True:
                    buffer = await fsrc.read(1024)
                    if not buffer:
                        break
                    await fdst.write(buffer)
        logging.info(f'Copied {src} to {dest}')
    except Exception as e:
        logging.error(f'Error copying {src} to {dest}: {e}')


async def read_folder(source_folder, output_folder):
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            src_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lstrip('.').lower()
            dest_folder = os.path.join(output_folder, file_ext)
            dest_path = os.path.join(dest_folder, file)
            tasks.append(copy_file(src_path, dest_path))
    await asyncio.gather(*tasks)


def main():
    # Запит для вказування вихідної папки
    source_folder = input("Please enter the path to the source folder: ")

    if not os.path.exists(source_folder):
        logging.error(f"Source folder '{source_folder}' does not exist.")
        print(f"Source folder '{source_folder}' does not exist.")
        return

    # Запит для вказування цільової папки
    output_folder = input("Please enter the path to the output folder: ")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    asyncio.run(read_folder(source_folder, output_folder))


if __name__ == "__main__":
    main()
