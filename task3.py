"""
Напишите прототип тестовой системы, состоящей из двух тест-кейсов. В
данной задаче использование стороннего модуля для автоматизации
тестирования не приветствуется.
Тестовая система представляет собой иерархию классов, описывающую
тест-кейсы.
У каждого тест-кейса есть:
* Номер (tc_id) и название (name)
* Методы для подготовки (prep), выполнения (run) и завершения (clean_up)
тестов.
* Метод execute, который задаёт общий порядок выполнения тест-кейса и
обрабатывает исключительные ситуации.
Все этапы выполнения тест-кейса, а также исключительные ситуации должны
быть задокументированы в лог-файле или в стандартном выводе.
Тест-кейс 1: Список файлов
* [prep] Если текущее системное время, заданное как целое количество
секунд от начала эпохи Unix, не кратно двум, то необходимо прервать
выполнение тест-кейса.
* [run] Вывести список файлов из домашней директории текущего
пользователя.
*[clean_up] Действий не требуется.
Тест-кейс 2: Случайный файл
*[prep] Если объем оперативной памяти машины, на которой исполняется
тест, меньше одного гигабайта, то необходимо прервать выполнение
тест-кейса.
*[run] Создать файл test размером 1024 КБ со случайным содержимым.
*[clean_up] Удалить файл test.
"""
import logging.config
import os.path
import random
import string
import time
import psutil

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('tc')


class TestCase:
    def __init__(self, tc_id: int, name: str) -> None:
        self.tc_id = tc_id
        self.name = name
        logger.info(f'Created test case #{self.tc_id} with name {self.name}.')

    def prep(self):
        pass

    def run(self):
        pass

    def clean_up(self):
        pass

    def execute(self):
        try:
            if self.prep():
                logger.info(f'Test #{self.tc_id}: preparation passed.')
                self.run()
                logger.info(f'Test #{self.tc_id}: passed.')
                self.clean_up()
                logger.info(f'Test #{self.tc_id}: cleaning completed.')
            else:
                logger.warning(
                    f'Test #{self.tc_id} stopped: preparation failed.')
        except Exception as error:
            logger.error(f'Unexpected error:\n{error}')


class TC1(TestCase):
    def prep(self) -> bool:
        return not (round(time.time()) & 1)

    def run(self) -> None:
        home = os.path.expanduser('~')

        for entry in os.listdir(home):
            if os.path.isfile(os.path.join(home, entry)):
                print(entry)


class TC2(TestCase):
    def prep(self) -> bool:
        return psutil.virtual_memory()[0] >= 1024 ** 3

    def run(self) -> None:
        with open('test', 'w', encoding='utf8') as file:
            for _ in range(1024 ** 2):
                file.write(random.choice(string.ascii_letters + string.digits +
                                         string.punctuation))

    def clean_up(self) -> None:
        if os.path.exists('test'):
            os.remove('test')


def main() -> None:
    files_list = TC1(1, 'files_list')
    files_list.execute()

    random_file = TC2(2, 'random_file')
    random_file.execute()


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        logger.error(f'Unexpected error:\n{error}')
