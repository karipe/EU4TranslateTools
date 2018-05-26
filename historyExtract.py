# -*- coding: utf-8 -*-

import os
import os.path
import re


def parse_data(category, file):
    f = open("./history/%s/%s.txt" % (category, file), "r", encoding="ISO-8859-1")
    lines = f.readlines()
    f.close()

    data_re = re.compile('"(.*?)"')

    result_set = set()
    result = []

    for line in lines:
        line = line.split("#")[0].strip()  # 주석 제거
        m = data_re.findall(line)
        if m:
            for elem in m:
                original_text = elem
                result_set.add(original_text)
    for original_text in result_set:
        result.append([category, file, original_text])
    return list(result)


def main():
    folders = os.listdir("./history")

    result = []
    for category in folders:
        path = "./history/" + category
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                file_name, file_ext = os.path.splitext(file)
                result += parse_data(category, file_name)

    f = open('parsedHistory.txt', 'w', encoding="utf-8")
    for elem in result:
        f.write("%s\t%s\t%s\n" % (elem[0], elem[1], elem[2]))
    f.close()


main()