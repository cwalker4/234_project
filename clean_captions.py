import json
import re
import os

def vtt_to_txt(filepath):
    """
    Converts a .vtt file to .txt and saves

    INPUT:
        filename

    """
    filename = filepath.split('/')[-1]
    if filename.startswith('.'):
        return
    try:
        captions = open(filepath, 'r').readlines()
    except UnicodeError:
        print("Couldn't convert: {}".format(filepath))
        return
    
    video_id = filename.split('.')[0]
    # only hold onto english subtitles (easier on text processing)
    language = captions[2].split('Language: ')[1].strip()

    if language != 'en':
        return
    
    result = []
    drop_regex = re.compile(r'-->')
    corrupted_regex = re.compile(r'<c>')
    for line in captions[5:]:
        # if it's a timestamp line or empty skip it
        if drop_regex.search(line) or not line.strip():
            continue
        if corrupted_regex.search(line):
            return
        else:
            result.append(line.encode('utf-8', 'ignore').decode('utf-8').lower())
            
    with open(os.path.join('derived_data/captions_clean', video_id + '.txt'), 'w') as f:
        f.write(" ".join(result))
        

if __name__ == "__main__":
    for file in os.listdir("scrape_results/captions"):
        vtt_to_txt("scrape_results/captions/" + file)
