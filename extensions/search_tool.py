import re

with open(r'D:\Zovix\apktool_out\AndroidManifest.xml', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('LAUNCHER')
if idx != -1:
    print("=== Context around LAUNCHER ===")
    print(content[max(0,idx-600):idx+50])


acts = re.findall(r'android:name="(com\.blackhub[^"]+)"', content)
for a in acts:
    print("Activity:", a)
