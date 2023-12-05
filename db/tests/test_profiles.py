import pytest 

import db.profiles as pf

def test_test_profile():
    test_profile = pf.get_test_profile()
    assert isinstance(test_profile, dict)

def test_get_profile():
    profile = pf.get_profile("123")
    assert isinstance(profile, dict)

def test_add_profile():
    profile_id = pf.add_profile("john smith", ["cs hw1", "fin hw2"], True, ["cs", "fin"])
    assert profile_id is not None

     