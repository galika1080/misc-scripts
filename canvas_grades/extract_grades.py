import re

file = open('grade_from_canvas.txt',mode='r')
xml = file.read()
file.close()

pattern = re.compile(r'''<span class="grade" tabindex="0">[ \t\n]+
<span class="tooltip_wrap right" aria-hidden="true">[ \t\n]+
<span class="tooltip_text score_teaser">[ \t\n]+
Click to test a different score[ \t\n]+
</span>[ \t\n]+
</span>[ \t\n]+
<span class="screenreader-only" role="button">[ \t\n]+
Click to test a different score[ \t\n]+
</span>[ \t\n]+
(.*)[ \t\n]+
</span>''')

pattern = re.compile(r'Click to test a different score[ \t\n]*</span>[ \t\n]*(\d+.?\d*)')

total = 50

for grade in re.findall(pattern, xml):
    print(grade)
    total += float(grade)

print("Total:", total)