def markCaptain(x):
    if '(c)' in x:
        return x
    else:
        return '-'
    
def changeAbbrev(x):
    if 'Titans' in x or 'GT' in x:
        return 'Gujarat Titans'
    elif 'PBKS' in x or 'Punjab'in x:
        return 'Punjab Kings'
    elif 'CSK' in x or 'Chennai' in x:
        return 'Chennai Super Kings'
    elif 'RR' in x or 'Royals' in x:
        return 'Rajasthan Royals'
    elif 'RCB' in x or 'Bangalore' in x:
        return 'Royal Challengers Bangalore'
    elif 'KKR' in x or 'Kolkata' in x:
        return 'Kolkata Knight Riders'
    elif 'SRH' in x or 'Hyderabad' in x:
        return 'Sunrisers Hyderabad'
    elif 'MI' in x:
        return 'Mumbai Indians'
    elif 'DC' in x:
        return 'Delhi Capitals'
    elif 'LSG' in x:
        return 'Lucknow Super Giants'
    else:
        return '-'

def winBy(x):
    if 'wickets' in x:
        return 'wickets'
    elif 'runs' in x:
        return 'runs'
    else:
        return '-'
    
def checkRunout(x):
    if 'run out' in x or '/' in x:
        return 1
    else:
        return 0