import parser


def test_parser_page():
    result = parser.parser_page(url)
    assert result == target, 'target error {} != {}'.format(result, target)
