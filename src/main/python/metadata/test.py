import json

cur = None

with open("E:\\zhouxiao\\code\\ChinaOpenDataPortal\\src\\main\\python\\metadata\\json\\metadata\\sichuan_mianyang.json", 'r', encoding='utf-8') as f:
    cur = json.load(f)



print(len(cur))

