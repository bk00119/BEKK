import pytest 

import db.profiles as pf

def test_test_profile():
    test_profile = pf.get_test_profile()
    assert isinstance(test_profile, dict)

@pytest.mark.skip("working on")
def test_get_profile():
    profile = pf.get_profile("656e29138f600af5c067f4de")
    assert isinstance(profile, dict)

def test_add_profile():
    profile_id = pf.add_profile("john smith", ["cs hw1", "fin hw2"], True, ["cs", "fin"])
    assert profile_id is not None

     