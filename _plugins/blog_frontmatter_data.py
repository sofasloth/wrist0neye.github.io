import frontmatter
import os
import json

input_dir = '_posts'
output_dir = 'assets'

files = []
for filename in os.listdir(input_dir) :
    if filename.endswith(".md") :
        filepath = os.path.join(input_dir, filename);

        print(filename)
        with open(filepath, "r", encoding="UTF-8") as file :
            post = frontmatter.loads(file.read())

            filedata = {}
            for k in ['title', 'tags', 'categories', 'incomplete', 'pin'] :
                filedata[k] = post[k] if k in post.keys() else False
            # title = post['title']
            # tags = post['tags'] if 'tags' in post.keys() else None
            # categories = post['categories'] if 'categories' in post.keys() else None
            # incomplete = post['incomplete'] if 'incomplete' in post.keys() else False
            # pin = post['pin'] if 'pin' in post.keys() else False

            # print(title, tags, categories, incomplete, pin)
            files.append(filedata)
export_data = {}
export_data["files"] = files

with open(output_dir + '/data.json','w',encoding="UTF-8") as f:
    json.dump(export_data, f, ensure_ascii=False, indent = 2)