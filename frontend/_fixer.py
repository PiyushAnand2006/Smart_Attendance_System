import os
OPEN = chr(123)
CLOSE = chr(125)
LT = chr(60)
GT = chr(62)
SLASH = chr(47)
NL = chr(10)
DQ = chr(34)
SP = chr(39)
CP = chr(41)
OP = chr(40)
def fix_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    orig = text
    H1_CLOSE = LT + SLASH + "h1" + GT
    P_CLOSE = LT + SLASH + "p" + GT
    USER = OPEN + "user?.email || " + SP + "User" + SP
    TITLE = OPEN + "title"
    replacements = [
        (TITLE + H1_CLOSE, TITLE + CLOSE + H1_CLOSE),
        (USER + P_CLOSE, USER + CLOSE + P_CLOSE),
        ("            " + CP + CP + CLOSE + NL, "            " + CP + CP + CP + CLOSE + NL),
        ("          " + CP + CP + CLOSE + NL, "          " + CP + CP + CP + CLOSE + NL),
    ]
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
            print("  Fixed")
    if text != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    return False
files = [
    r"C:\Users\thaku\hackathon&projects\Smart_Attendance_System\frontend\src\app\admin\dashboard\page.tsx",
    r"C:\Users\thaku\hackathon&projects\Smart_Attendance_System\frontend\src\app\faculty\dashboard\page.tsx",
    r"C:\Users\thaku\hackathon&projects\Smart_Attendance_System\frontend\src\app\student\dashboard\page.tsx",
    r"C:\Users\thaku\hackathon&projects\Smart_Attendance_System\frontend\src\app\admin\students\page.tsx",
    r"C:\Users\thaku\hackathon&projects\Smart_Attendance_System\frontend\src\app\student\calculator\page.tsx",
    r"C:\Users\thaku\hackathon&projects\Smart_Attendance_System\frontend\src\components\Header.tsx",
]
for f in files:
    if os.path.exists(f):
        print("Checking:", os.path.basename(f))
        if fix_file(f):
            print("  Saved")
