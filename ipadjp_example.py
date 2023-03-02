from main import API

a = API()
a.config(
    sess='',
    uin='',
    wait=0,
    region=1,
    device=3
)
try:
    with open('transfercode.txt') as f:
        lines = f.readlines()
    if lines is not None:
        code = lines[0] 
except FileNotFoundError:
    print("transfercode.txt does not exist")
    code = ''

#a.setProxy('127.0.0.1:8888')
a.dologin(32939263112, code)
a.Complete_Overlord_Tower()
# a.o.use_potions = True
# a.completeStory()