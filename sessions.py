from collections import Counter
from copy import deepcopy

def hash_session(session_response):
    # Here we'll use all "significant" fields of sessions
    # and form a tuple out of them. A tuple can then be hashed
    # to give a unique hash to this session.
    # Goal is for hash to change if any field that we care about
    # in a session changes. 
    data = \
        tuple((session_response.get(s, None) for s in (
            "center_id", "from", "to", "fee_type", "session_id",
            "date", "min_age_limit", "vaccine"
        )))
    data = (*data, session_response.get("available_capacity", 0) > 0)
    return hash(
        data
    )

def hash_sessions(sessions):
    # https://stackoverflow.com/questions/29435556/how-to-combine-hash-codes-in-in-python3
    # hash(frozenset(Counter(<tuple>).items())) lets us hash together a 
    # bunch of hashes that are not necessarily unique, and could be in any order
    # examples:
    # >>> hash(frozenset(Counter((1, 2)).items()))
    # -8393522522739843608
    # >>> hash(frozenset(Counter((2, 1)).items()))
    # -8393522522739843608
    # >>> hash(frozenset(Counter((2, 1, "this")).items()))
    # -1990742254494264636
    return hash(frozenset(Counter((hash_session(s) for s in sessions)).items()))

def hash_calendar(calendar):
    all_hashes = []
    calendar = deepcopy(calendar)

    # If pincode is part of the dict, add that
    all_hashes.append(hash(calendar.get('pincode',0)))

    for i in range(len(calendar["centers"])):
        center = calendar["centers"][i]
        sessions = center.get("sessions", None)
        if sessions is None or len(sessions) == 0:
            all_hashes.append(hash_session(center))
            continue
        
        if "sessions" in center:
            del center["sessions"]
        
        all_hashes.append(hash_sessions(
            # calendar is {center_info, sessions: [session_info]}
            # merging center_info with each session_info gives us 
            # a list of sessions. Probably useful for future, only minor cost, doing it.
            [{**center, **s} for s in sessions] 
        ))
    return hash(frozenset(Counter((h for h in all_hashes))))

def hash_centers(code, centers):
    '''Small adapter to reuse hash_calendar function even for subscription
    availability dictionary'''
    availability2cal = {
        'pincode': code,
        'centers': centers
    }
    return hash_calendar(availability2cal)

def hash_calendars(calendars):
    return hash(frozenset(Counter(hash_centers(pincode, centers)
        for pincode, centers in calendars.items()).items()))
