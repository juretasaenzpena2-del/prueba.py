from ej1a3 import invert_text

def test_invert_text():
    assert invert_text("Good day") == "yad dooG", "invert_text does not return the correct value for 'Good day'. It should be 'yad dooG'"
    assert invert_text("python") == "nohtyp", "invert_text does not return the correct value for 'python'. It should be 'nohtyp'"
    assert invert_text("987654321") == "123456789", "invert_text does not return the correct value for '987654321'. It should be '123456789'"
    assert invert_text("") == "", "invert_text does not return the correct value for ''. It should be ''"