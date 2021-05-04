import unittest

from sessions import * 

class TestSessions(unittest.TestCase):
    session_a = {
        "center_id": "3",
        "available_capacity": 5
    }
    session_b = {
        "center_id": "3",
        "available_capacity": 10
    }
    session_c = {
        "center_id": "4",
        "available_capacity": 4
    }

    calendar_a = { 
        "centers": [{
            "center_id": 45,
            "sessions": [
                {
                    "available_capacity": 10
                },
                {
                    "available_capacity": 15
                }
            ]
        }]
    }
    calendar_b = {
        "centers": [{
            "center_id": 45,
            "sessions": [
                {
                    "available_capacity": 15
                },
                {
                    "available_capacity": 10
                }
            ]
        }]
    }
    calendar_c = {
        "centers": [{
            "center_id": 45,
            "sessions": [
                {
                    "available_capacity": 10
                }
            ]
        }]
    }


    def test_hash_session(self):
        self.assertNotEqual(hash_session(self.session_a), hash_session(self.session_b))
        self.assertEqual(hash_session(self.session_a), hash_session(self.session_a))
        session_x = self.session_a
        session_x["dont_care"] = 444
        self.assertEqual(hash_session(self.session_a), hash_session(session_x))

    
    def test_hash_sessions(self):
        self.assertEqual(
            hash_sessions([self.session_a, self.session_b]),
            hash_sessions([self.session_b, self.session_a])
        )
        self.assertNotEqual(
            hash_sessions([self.session_a]),
            hash_sessions([self.session_a, self.session_b])
        )
        self.assertNotEqual(
            hash_sessions([]), hash_sessions([self.session_a])
        )
        self.assertEqual(
            hash_sessions([]), hash_sessions([])
        )
    
    def test_hash_calendar(self):
        self.assertEqual(
            hash_calendar(self.calendar_a),
            hash_calendar(self.calendar_b)
        )
        self.assertNotEqual(
            hash_calendar(self.calendar_a),
            hash_calendar(self.calendar_c)
        )

if __name__=="__main__":
    unittest.main()