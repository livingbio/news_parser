

def test_parser_page():
    result = parser_page(url1)
    assert result == target, "..."

def test_get_category_urls():
    result = get_catetgory_urls(url)
    assert result == target, "..."




if __name__ == '__main__':
    test_parser_page()
    test_get_category_urls()