import re

with open('lbp_animation.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'sub\(voice_data\["(.*?)"\]\)', r'sub("\1")', content)

with open('lbp_animation.py', 'w', encoding='utf-8') as f:
    f.write(content)
