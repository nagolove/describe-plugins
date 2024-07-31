#!/usr/bin/env python3
import re
import os
import requests, sys
import progressbar

def download_readme(url):
    possible_paths = [
        f"https://raw.githubusercontent.com/{url.replace('\'', '')}/master/README.md",
        f"https://raw.githubusercontent.com/{url.replace('\'', '')}/master/readme.md",
        f"https://raw.githubusercontent.com/{url.replace('\'', '')}/master/README.markdown",
    ]
    
    print(f'download_readme: request for {url}');
    
    for readme_url in possible_paths:
        response = requests.get(readme_url)
        if response.status_code == 200:
            print(f'download_readme: got for {url}');
            return response.text

    print
    return None

def process_vim_init(file_path_in, file_path_out):
    with open(file_path_in, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    plugin_regex = re.compile(r"Plug\s+'([^']+)'")
    new_lines = []

    match_counter = 0

    for line in lines:
        match = plugin_regex.search(line)
        if match:
            match_counter += 1

    print(f'match_counter {match_counter}')
    bar = progressbar.ProgressBar(max_value=match_counter)
   
    i = 0
    for line in lines:
        match = plugin_regex.search(line)
        if match:
            new_lines.append("\n")
            new_lines.append(line)
            plugin_path = match.group(1)
            readme_content = download_readme(plugin_path)
            i += 1

            os.system('cls' if os.name == 'nt' else 'clear')
            # sys.stdout.write('\r')  # Возвращаем курсор в начало строки
            # sys.stdout.flush()

            bar.update(i)
            print("\n")

            if readme_content:
                commented_readme = '\n'.join(['" ' + line for line in readme_content.split('\n')])
                # print(commented_readme)
                new_lines.append("\n")
                new_lines.append(f'" {plugin_path} README {{{{{{')
                new_lines.append(commented_readme)
                new_lines.append(f'"}}}}}}')
                new_lines.append("\n")
            else:
                new_lines.append(f'" {plugin_path} README not found\n')
        else:
            new_lines.append(line)

    with open(file_path_out, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

# Укажите путь к вашему init.vim файлу
vim_init_file_path_in = '/home/nagolove/.config/nvim/init.vim'
vim_init_file_path_out = 'init.out.vim'
process_vim_init(vim_init_file_path_in, vim_init_file_path_out)

