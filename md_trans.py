import urllib

# 用來將我Obsidian筆記轉成README.md格式的輔助程式

with open("README.md", "r") as f:
    md = f.readlines()

new_md = []
for i in md:
    if i.startswith("![["):
        tmp = i.replace("[", "", 1)
        png_name = i.split("![[")[1].split("]]")[0]
        tmp = tmp.replace("]", "", 1).replace("\n", "")
        png_name = urllib.parse.quote(png_name)
        tmp += f"(./pic/{png_name})"
        new_md.append(tmp)
    else:
        new_md.append(i)

result = "".join(new_md)
with open("README_try.md", "w") as f:
    f.write(result)
