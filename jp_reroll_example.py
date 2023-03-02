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

a.dologin(62660079170, code)

# This script will complete overlord tower and Story as far as you AP can get you
# It will clear the tutorials so you can quickly farm 10k nq for your rerolling

a.Complete_Overlord_Tower()
a.upgrade_items(item_limit=1)
a.present_receive_all_except_equip_and_AP()
a.o.use_potions = True
a.completeStory()
a.present_receive_all_except_equip_and_AP()
tutorials = a.client.player_sub_tutorials()
tutorials_to_complete = [1, 7, 8]
for i in tutorials_to_complete:
    tutorial = next((x for x in tutorials['result']['_items'] if x['m_sub_tutorial_id'] == i),None)
    if tutorial is not None and tutorial['status'] == 0:
        a.client.sub_tutorial_read(i)