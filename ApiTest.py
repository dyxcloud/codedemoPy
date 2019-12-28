lblack = {'scu','kizunanosora','S-Cute','ps7','Siberian Mouse','shemaleJP','foreign','短片'}
def _not_skip_flie(filename):
    for b in lblack:
        if filename.find(b)>=0:
            return False
    return True

print(_not_skip_flie('asdas短片123as'))