# -*- coding: utf-8 -*-

import os
import subprocess
import sys

cp_map = {
    0x80: 0x20AC,
    0x82: 0x201A,
    0x83: 0x0192,
    0x84: 0x201E,
    0x85: 0x2026,
    0x86: 0x2020,
    0x87: 0x2021,
    0x88: 0x02C6,
    0x89: 0x2030,
    0x8A: 0x0160,
    0x8B: 0x2039,
    0x8C: 0x0152,
    0x8E: 0x017D,
    0x91: 0x2018,
    0x92: 0x2019,
    0x93: 0x201C,
    0x94: 0x201D,
    0x95: 0x2022,
    0x96: 0x2013,
    0x97: 0x2014,
    0x98: 0x02DC,
    0x99: 0x2122,
    0x9A: 0x0161,
    0x9B: 0x203A,
    0x9C: 0x0153,
    0x9E: 0x017E,
    0x9F: 0x0178
}


def cp1252_to_ucs2(cp):
    if cp < 0:
        cp += 256
    if cp in cp_map:
        result = cp_map[cp].to_bytes(2, byteorder='little')
    else:
        result = cp.to_bytes(2, byteorder='little')
    return result


def convert_wide_text_to_escaped_wide_text(wide_text):
    result = bytearray()
    special_chars = [0xA4, 0xA3, 0xA7, 0x24, 0x5B, 0x00, 0x5C, 0x20, 0x0D, 0x0A,
                     0x22, 0x7B, 0x7D, 0x40, 0x80, 0x7E, 0xBD]
    for i in range(0, len(wide_text), 2):
        escape_char = 0x10
        high = wide_text[i + 1]
        low = wide_text[i]
        if high == 0:
            result += bytes([low, 0x00])
            continue

        if high in special_chars:
            escape_char += 2
            high -= 9
        if low in special_chars:
            escape_char += 1
            low += 15

        result.extend(escape_char.to_bytes(2, byteorder='little') + cp1252_to_ucs2(low) + cp1252_to_ucs2(high))

    return result

characters = set()
worldmap_characters = set()


def extract_characters(name, text):
    for c in text:
        if c == '\n':
            continue
        characters.add(c)
        if name in ['countries_l_english', 'prov_names_l_english', 'area_regions_l_english',
                    'cultures_phase4_l_english', 'prov_names_adj_l_english', 'regions_phase4_l_english',
                    'tags_phase4_l_english']:
            worldmap_characters.add(c)


def process_file(name):
    print('Processing ' + name + '...')
    f = open('./original_yml/' + name + '.yml',"r", encoding='utf_8_sig')
    text = f.read()
    f.close()
    extract_characters(name, text)

    wide_text = text.encode('utf-16-le')
    escaped_wide_text = convert_wide_text_to_escaped_wide_text(wide_text)
    text = escaped_wide_text.decode('utf-16-le')
    f = open('./result_yml/' + name + '.yml', 'w', encoding='utf_8_sig')
    f.write(text)
    f.close()


def escape_yml():
    files = os.listdir("./original_yml")
    for file in files:
        file_name, file_ext = os.path.splitext(file)

        if file_ext == ".yml":
            process_file(file_name)

    # Add default texts
    f = open('./default_source.txt', 'r', encoding='utf_8_sig')
    text = f.read()
    extract_characters(None, text)
    f.close()

    f = open('./ingame_source.txt', 'w', encoding='utf_8_sig')
    f.write(''.join(characters))
    f.close()
    f = open('./worldmap_source.txt', 'w', encoding='utf_8_sig')
    f.write(''.join(worldmap_characters))
    f.close()


def generate_bmfont(name, ext, source_file):
    cmdList = [
        'bmfont64.exe',
        '-c',"./bmfc/" + name + ext,
        '-o',"./fonts/" + name + ".fnt",
        '-t',source_file
    ]

    subprocess.call(' '.join(cmdList))


def generate_fonts():
    files = os.listdir("./bmfc");
    for file in files:
        file_name, file_ext = os.path.splitext(file);
        if file_ext == ".bmfc":
            generate_bmfont(file_name, file_ext, "ingame_source.txt");
        if file_ext == "._bmfc":
            generate_bmfont(file_name, file_ext, "worldmap_source.txt");


if __name__ == "__main__":
    # execute only if run as a script
    if len(sys.argv) == 1:
        escape_yml()
        generate_fonts()
    elif sys.argv[1] == '-y':
        escape_yml()
    elif sys.argv[1] == '-f':
        generate_fonts()
    else:
        print('Usage: (EU4Tools.py | EU4Tools.py -y | EU4Tools.py -f)')