import os
import shutil

output_dir = 'output'
docs_dir = 'docs'

for filename in os.listdir(output_dir):
    if filename.endswith('.html'):
        src = os.path.join(output_dir, filename)
        dst = os.path.join(docs_dir, filename)
        shutil.copy2(src, dst)
        print(f'Copied {filename} to docs/') 