from collections import Counter

def hash_session(session_response):
    # Here we'll use all "significant" fields of sessions
    # and form a tuple out of them. A tuple can then be hashed
    # to give a unique hash to this session.
    # Goal is for hash to change if any field that we care about
    # in a session changes. 
    data = \
        tuple((session_response.get(s, None) for s in (
            "center_id", "from", "to", "fee_type", "session_id",
            "date", "available_capacity", "min_age_limit", "vaccine"
        )))
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
