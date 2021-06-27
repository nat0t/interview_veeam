"""
Реализовать программу, осуществляющую копирование файлов в соответствии
с конфигурационным файлом. Конфигурационный файл должен иметь формат
xml. Для каждого файла в конфигурационном файле должно быть указано его
имя, исходный путь и путь, по которому файл требуется скопировать.

Пример
Конфигурационный файл:
<config>
    <file
            source_path="C:\Windows\system32"
            destination_path="C:\Program files"
            file_name="kernel32.dll"
    />
    <file
            source_path="/var/log"
            destination_path="/etc"
            file_name="server.log"
    />
</config>
"""
import argparse
import xml.etree.ElementTree as ET
import os.path as path
import os
import shutil


def get_args() -> str:
    parser = argparse.ArgumentParser(
        description='Copy files according to configuration file.')
    parser.add_argument('conf', help='Configuration xml-file of form: <config>'
                             '<filesource_path=path destination_path=path '
                             'file_name=name/></config>')
    args = parser.parse_args()
    return args.conf


def parse_config(config_name: str) -> dict:
    """
    Parse configuration file and return dictionary.
    :param config_name: Configuration file.
    :return: Dictionary {file_name: (source_path, destination_path)}.
    """

    config = ET.parse(config_name).getroot()
    return {file.get('file_name'): (file.get('source_path'),
            file.get('destination_path')) for file in config}


def copy_files(settings: dict) -> None:
    """
    Copy files according to settings.
    :param settings: Dictionary {file_name: (source_path, destination_path)}.
    :return: None.
    """

    for file in settings:
        src = path.join(path.normpath(settings[file][0]), file)
        dst = path.normpath(settings[file][1])
        try:
            if path.exists(src):
                if not path.exists(dst):
                    os.makedirs(dst)
                shutil.copy(src, dst)
                print(f'File {src} was copied to {dst}.')
            else:
                print(f'There is no file {src}.')
        except Exception as error:
            print(error)


def main() -> None:
    """Main process."""

    copy_files(parse_config(get_args()))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
