import os
import json

REDIRECTS_FILE = 'redirects.json'
OUTPUT_DIR = 'output'  # or your actual output dir

redirects = [
    {
        "source": "/episodes/",
        "status": "301",
        "target": "/podcast"
    },
    {
        "source": "/antilibrary/",
        "status": "301",
        "target": "/books"
    },
    {
        "source": "/<*>",
        "status": "404-200",
        "target": "/404.html"
    }
]

valid_dirs = ['output', 'output/episodes']
invalid_files =  ['index.html', '404.html']

for directory in valid_dirs:
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f not in invalid_files]
    for file in files:
        rel_dir = directory.replace('output', '')
        file = file.replace('.html', '')
        redirects.append({
            "source": f'{rel_dir}/{file}/',
            "target": f'{rel_dir}/{file}',
            "status": "301",
        })                    

with open(REDIRECTS_FILE, 'w') as f:
    json.dump(redirects, f, indent=2)

print(f"Generated {len(redirects)} redirect rules.")
