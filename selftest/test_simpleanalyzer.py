from lib.simple_analyzer import SimpleAnalyzer

def test_parse_line():
    passing_test_data = ["This is an error message.",             "11:01 ERROR[Critical]: abcdefghijklmn",
                         "11:02 ERROR[Critical]: abcdefghijklmn", "11:03 ERROR[Critical]: abcdefghijklmn",
                         "E/GECKO (12345): Hello World!",         "Failed to do this!"]
    failing_test_data = ["sigkill: homescreen", "MediaErrorHandler", "be9uy7gbfp9webtgi3q2tg"]

    sa = SimpleAnalyzer()
    for sentence in passing_test_data:
        assert sa.parse_line(sentence).startswith("Error:")

    assert len(sa.return_sorted_error()) == 4
    assert len(sa.return_error()) == 6

    for sentence in failing_test_data:
        assert sa.parse_line(sentence) == ""

    assert len(sa.return_sorted_error()) == 4
    assert len(sa.return_error()) == 6

def test_clean_data():
    passing_test_data = ["This is an error message.",             "11:01 ERROR[Critical]: abcdefghijklmn",
                         "11:02 ERROR[Critical]: abcdefghijklmn", "11:03 ERROR[Critical]: abcdefghijklmn",
                         "E/GECKO (12345): Hello World!",         "Failed to do this!"]
    failing_test_data = ["sigkill: homescreen", "MediaErrorHandler", "be9uy7gbfp9webtgi3q2tg"]

    sa = SimpleAnalyzer()
    for sentence in passing_test_data:
        sa.parse_line(sentence)

    assert len(sa.return_sorted_error()) == 4
    assert len(sa.return_error()) == 6

    sa.clean_lists()
    assert len(sa.return_sorted_error()) == 0
    assert len(sa.return_error()) == 0


