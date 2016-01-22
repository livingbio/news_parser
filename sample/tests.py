from sample import process
import requests

class FakeResponse():
    content = ''

    def __init__(self, content):
        self.content = content

def test_process():
    fake_response = FakeResponse('<html><title>george</title></html>')
    
    def fake_request_get(url):
        return fake_response

    origin_get = requests.get
    requests.get = fake_request_get

    result = process('http://www.google.com')
    assert result == 'george', 'process error {} is not george'.format(result)
    
    requests.get = origin_get




if __name__ == '__main__':
    test_process()
