def shift(lst) -> list:
    last    = lst[-1]
    lst[1:] = lst[:-1]
    lst[0]  = last
    return lst

def get_round(keys) -> list:
    pair_amount = len(keys) // 2
    round = [(keys[i], keys[-(i+1)]) for i in range(pair_amount)]
    return round

def get_schedule(registered) -> list:
    keys = list(registered)
    if len(keys) % 2 == 1:
        keys.append(None) #add dummy key if uneven

    schedule = []

    last_keys  = keys
    for round in range(len(keys) - 1):
        schedule.append(get_round(last_keys))
        last_keys[1:] = shift(last_keys[1:])
    
    return schedule