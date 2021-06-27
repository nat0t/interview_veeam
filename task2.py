"""
Дан файл, содержащий имена файлов, алгоритм хэширования (один из
MD5/SHA1/SHA256) и соответствующие им хэш-суммы, вычисленные по
соответствующему алгоритму и указанные в файле через пробел. Напишите
программу, читающую данный файл и проверяющую целостность файлов.
Пример
Файл сумм:
file_01.bin md5 aaeab83fcc93cd3ab003fa8bfd8d8906
file_02.bin md5 6dc2d05c8374293fe20bc4c22c236e2e
file_03.bin md5 6dc2d05c8374293fe20bc4c22c236e2e
file_04.txt sha1 da39a3ee5e6b4b0d3255bfef95601890afd80709
Пример вызова:
<your program> <path to the input file> <path to the directory
containing the files to check>
Формат вывода:
file_01.bin OK
file_02.bin FAIL
file_03.bin NOT FOUND
file_04.txt OK
"""
import argparse
import hashlib
import os


def get_args() -> tuple:
    parser = argparse.ArgumentParser(description='Check hash-sums of files '
                                                 'listed in checksum-file.')
    parser.add_argument('checksum', help='File of form: file_name algorithm'
                                         '(MD5/SHA1/SHA256) hash-sum.')
    parser.add_argument('-d', dest='check_dir', default=os.getcwd(),
                        help='Path to directory with checking files. '
                             'The current directory by default.')
    args = parser.parse_args()
    return args.checksum, args.check_dir


def parse_checksum(checksum_file) -> dict:
    """
    Parse checksum file and return dictionary.
    :param checksum_file: File with checksums.
    :return: Dictionary {file_name: (algorithm, hash-sum)}.
    """

    with open(checksum_file) as file:
        return {line.split()[0]: (line.split()[1], line.split()[2])
                for line in file.readlines()}


def calc_hash(file_name: str, algorithm: str) -> str:
    """
    Calculate checksum of file.
    :param file_name: Name of file for calculate checksum.
    :param algorithm: Hashing algorithm.
    :return: Hash sum of file.
    """

    algorithms = {
        'md5': hashlib.md5(),
        'sha1': hashlib.sha1(),
        'sha256': hashlib.sha256()
    }
    hash_ = algorithms.get(algorithm)

    with open(file_name, 'rb') as file:
        for chunk in iter(lambda: file.read(1024), b''):
            hash_.update(chunk)
    return hash_.hexdigest()


def check_hash(source: dict, check_dir: str) -> None:
    """
    Check hash-sums of files in source.
    :param source: Dictionary {file_name: (algorithm, hash-sum)}.
    :param check_dir: Directory with checking files.
    :return: None.
    """

    for file in source:
        file_path = os.path.join(check_dir, file)
        if os.path.exists(file_path):
            if source[file][1] == calc_hash(file_path, source[file][0]):
                print(f'{file} OK')
            else:
                print(f'{file} FAIL')
        else:
            print(f'{file} NOT FOUND')


def main() -> None:
    """Main process."""

    checksum_file, check_dir = get_args()
    check_hash(parse_checksum(checksum_file), check_dir)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
