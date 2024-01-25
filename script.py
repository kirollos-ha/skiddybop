# se proprio vogliamo esagerare
# hanno ci sono mai max score diversi a seconda della cup dc o meno
fs_max_scores = {
    'skidpad'       : 75,
    'accelleration' : 75,
    'autocross'     : 100,
    'trackdrive'    : 200,
}

# penalità
cone_accel:float = 2
cone_skidpad:float = 0.2
cone_trackdrive:float = 2
cone_autocross:float = 2

# utility
def our_rank(ours:float, others:list[float]) -> int:
    """
    DOVREBBE dare il rank dati il nostro tempo e i tempi degli altri team
    non ho idea di come dovrei controllare per penalità con st'api del cazzo
    dipende da come ci tira con le domande

    almeno credo che venga definito così il rank, non da altre spec nel 4.5
    e non so se voglio andare a cercare roba OLTRE il 4.5
    """
    if ours > 25.0:
        print("comunque squalificato che ci mai messo più di 25 secondi")

    bigger_than:int = 0
    for i in others:
        if ours > i:
            bigger_than += 1

    before_us = len(others) - bigger_than
    return before_us + 1

# skidpad
# driverless nella cup normale
# FS rules D 4.5
def dv_skidpad_ranks(n_teams:int, rank:int) -> float:
    pmax = fs_max_scores['skidpad']
    return pmax * ((n_teams + 1 - rank) / n_teams)

def dv_skidpad_times(ours:float, others:list[float]) -> float:
    if ours > 25.0:
        print("squalificato perchè più di 25 secondi")
        return 0

    return dv_skidpad_ranks(1 + len(others), our_rank(ours, others))

# driverless cup
# FS rules D 4.6
def dc_skidpad(fastest_any_team:float,
                        fastest_this_team:float,
                        disqualified:bool=False) -> float:
    pmax = fs_max_scores['skidpad']
    tmax = 1.5 * fastest_any_team
    score = 0.95 * pmax * (((tmax / fastest_this_team)**2)-1)/1.25
    if not disqualified:
        score += (5/100) * pmax

    return score

# accelleration
# driverless nella cup normale
# sono le stesse formule di skidpad (potevo usare *args, lo so)
# D 5.5
def dv_accel_ranks(n_teams:int, rank:int) -> float:
    return dv_skidpad_ranks(n_teams, rank)

def dv_accel_times(ours:float, others:list[float]) -> float:
    return dv_skidpad_times(ours, others)

## D 5.6
def dc_accel(fastest_any_team:float,
                              fastest_this_team:float,
                              disqualified:bool=False) -> float:
    return dc_skidpad(fastest_any_team,
                               fastest_this_team,
                               disqualified)

# autocross
# D 6.5 lo score, D 6.4 la procedura
def team_total(one:float, two:float) -> float:
    return min(one, (one+two)/2)

def dc_autocross(fastest:float, team_one:float, team_two:float, fast:float, dq:bool = False) -> float:
    pmax = fs_max_scores['autocross']
    score = 0.9 * pmax * ((fast - team_total(team_one, team_two)) / (fast - fastest))
    if not dq:
        score += 0.1 * pmax
    return score

def dc_autocross_times(team_one:float, team_two:float, super6:float, others:list[tuple[float, float]]) -> float:
    fastest:float = min(team_total(x[0], x[1]) for x in others)
    return dc_autocross(fastest, team_one, team_two, super6)

# track drive
# D 8.4
def dc_trackdrive(fastest:float, team:float, dq:bool=False) -> float:
    pmax:float = fs_max_scores['trackdrive']
    tmax:float = 2*fastest
    score = 0.75 * pmax * ((tmax/team) - 1)
    if not dq:
        score += (2.5/100) * pmax
    return score

# fs east
# skidpad (EA 6.6.2)
def east_skidpad(fastest_any_team:float, fastest_this_team:float) -> float:
    tmax:float = 1.5 * fastest_any_team
    return 75 * (((tmax/fastest_this_team)**2)-1)/0.5625

# acceleration (EA 6.10.4)
def east_accel(fastest_any_team:float, fastest_this_team:float) -> float:
    tmax:float = 2 * fastest_any_team
    return 75 * ((tmax/fastest_this_team) - 1)

# autocross (EA 6.8.2)
def east_autocross(fastest_any_team:float,
                         fastest_this_team:float,
                         time_spent_over_6:float) -> float:
    return 100 * ((time_spent_over_6 - fastest_this_team) /
                  (time_spent_over_6 - fastest_any_team))

# track drive (EA 6.13.4)
def east_trackdrive(fastest_any_team:float,
                          fastest_this_team:float) -> float:
    return 175 * ((fastest_any_team/fastest_this_team) - 1)
