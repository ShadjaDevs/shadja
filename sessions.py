from collections import Counter
from copy import deepcopy

def hash_session(session_response, center_id):
    # Here we'll use all 'significant' fields of sessions
    # and form a tuple out of them. A tuple can then be hashed
    # to give a unique hash to this session.
    # Goal is for hash to change if any field that we care about
    # in a session changes.
    # calendar is {center_info, sessions: [session_info]}
    # merging center_id with each session_info gives us 
    # a list of sessions. Probably useful for future, only minor cost, doing it.
    data = tuple((session_response.get(s, None) for s in (
        'fee_type', 'session_id', 'date', 'min_age_limit', 'vaccine')))

    data = (*data, session_response.get('available_capacity', 0) > 0, center_id)
    return hash(data)

def hash_sessions(sessions, center_id):
    return (hash_session(s, center_id) for s in sessions)

def hash_calendar(calendar):
    session_hashes = []

    if not calendar.get('centers', None):
        return

    for center in calendar['centers']:
        sessions = center.get('sessions', None)
        if not sessions:
            continue

        session_hashes.extend(
            hash_sessions(sessions, center.get('center_id')))

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
    return hash(frozenset(Counter(session_hashes).items()))
