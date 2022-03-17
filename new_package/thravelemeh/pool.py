last_locatable_mothers = ['a', 'aa', 'e', 'i', 'o', 'u']
last_locatable_sons = ['b', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'p', 's', 't', 'v', 'z']
last_unlocatable_mothers = ['w', 'y']
last_unlocatable_sons = ['c', 'j', 'q', 'r', 'x']

special_character = ['h']

forbidden = ['aaa', 'ee', 'ii', 'oo', 'uu', 'yw', 'wy', 'sss']
lmnhs = ['l', 'm', 'n', 'h']

mothers_with_h = last_unlocatable_mothers + last_locatable_mothers + special_character
sons_with_h = last_unlocatable_sons + last_unlocatable_sons + special_character

mothers = last_unlocatable_mothers + last_locatable_mothers
sons = last_unlocatable_sons + last_locatable_sons

last_locatables = last_locatable_mothers + last_locatable_sons
last_unlocatable = last_unlocatable_mothers + last_unlocatable_sons

alls = last_locatable_mothers + last_unlocatable_mothers + last_locatable_sons + last_unlocatable_sons + \
       special_character
