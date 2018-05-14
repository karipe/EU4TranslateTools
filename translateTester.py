# -*- coding: utf-8 -*-

import os

def translate_po_file(name, ext):
    f = open("./pofile/" + name + ext, "r", encoding='utf_8')
    lines = f.readlines()
    f.close()
    f = open("./original_yml/" + name + ".yml", "w", encoding='utf_8_sig')
    f.write('l_english:\n')

    msgctxt_readed = False
    for line in lines:
        line = line.strip()
        if 'msgctxt' in line:
            msgctxt_readed = True
            data = line.replace('msgctxt ', '').replace('"', '').replace('코', ':')
            f.write(' ' + data)
        if msgctxt_readed:
            if 'msgstr' in line:
                data = line.replace('msgstr', '')
                f.write(data + '\n')
    f.close()

def main():
    files = os.listdir("./pofile")
    for file in files:
        file_name, file_ext = os.path.splitext(file)
        if file_ext == ".po":
            translate_po_file(file_name, file_ext)

if __name__ == "__main__":
    main()