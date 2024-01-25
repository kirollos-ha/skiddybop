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
        if ours > others:
            bigger_than += 1

    int before_us = len(others) - bigger_than
    return before_us + 1

def fs_dv_skidpad_score_rank(nteams:int, rank:int) -> float:
    pmax = fs_max_scores['skidpad']
    return pmax * ((nteams + 1 - rank) / nteams)

def fs_dv_skidpad_score_times(ours:float, others:list[float]) -> float:
    if ours > 25.0:
        print("squalificato perchè più di 25 secondi")
        return 0

    return fs_div_skidpad_score_rank(1 + len(others), our_rank(ours, others))

def fs_dc_skidpada_score(fastest:float, team:float, dq:bool=False) -> float:
    pmax = 75 # dalla tabella 3
    tmax = 1.5 * fastest
    score = 0.95 * pmax * (((tmax / team)**2)-1)/1.25
    if not dq:
        score += (5/100) * pmax

    return score

def fs_dv_accelleration_score_rank(nteams:int, rank:int) -> float:
    return fs_dv_skidpad_score_rank(nteams, rank)

def fs_dv_accelleration_score_times(ours:float, others:list[float]) -> float:
    return fs_dv_skidpad_score_times(ours:, others)

def team_total(one:float, two:float) -> float:
    return min(one, (one+two)/2)

def fs_autocross_score(fastest:flaot, team_one:float, team_two:float, fast:float, dq:bool = False) -> float:
    pmax = max_scores['autocross']
    score = 0.9 * pmax ((fast - team_total(one, two)) / (fast - fastest))
    if not dq:
        score += 0.1 * pmax
    return score

def fs_autocross_score_times(team_one:float, team_two:float, super6:float, others:list[tuple[float, float]]) -> float:
    fastest:float = min(team_total(x[0], x[1]) for x in others)
    return fs_autocross_score(fastest, team_one, team_two, super6)

def fs_trackdrive_scoring(fastest:float, team:float, dq:bool=False) -> float:
    pmax:float = max_scores['trackdrive']
    tmax:float = 2*fastest
    score = 0.75 * pmax * ((tmax/team) - 1)
    if not dq:
        score += (2.5/100) * pmax
    return score

# se proprio vogliamo esagerare
# hanno ci sono mai max_score diversi a seconda della cup dc o meno
fs_max_scores = {
    'skidpad'       : 75,
    'accelleration' : 75,
    'autocross'     : 100,
    'trackdrive'    : 200,
}
