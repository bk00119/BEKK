import pytest 

import db.profiles as pf

def test_test_profile():
    test_profile = pf.get_test_profile()
    assert isinstance(test_profile, dict)
