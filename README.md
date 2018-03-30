# 변경사항에 대한 기록

### 63page

```python
def test_home_page_returns_correct_html(self):
    [...]

def test_home_page_can_save_a_POST_reqeust(self):
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = '신규 작업 아이템'
    
    response = home_page(request)
    
    self.assertIn('신규 작업아이템', response.content.decode())
```

책에 나와있는 데로 적용하면 csrf 토큰 값 때문에 `test_home_page_returns_correct_html`메서드에서 
assert error를 뱉어낸다. 찾아보니 이전 버전 에서는 `render_to_string`메서드에 request 인자를 추가해서
해결 할 수 있었지만 지금 내가 사용하고 있는 버전에서는 (1.11.6) 위와 같은 방법으로 해결 할 수 없었다.
(추측으로는 request 별로 다른 csrf 토큰을 만드는 것 같다)
[패스트캠퍼스 강사님이 알려주신 방법으로는](https://lhy.kr/tdd-with-python) 아래와 같이 csrf토큰 
문자열을 정규표현식을 사용해 삭제하는 것 이다. 
```python
class HomePageTest(TestCase):
    pattern_input_csrf = re.compile(r'<input[^>]*csrfmiddlewaretoken[^>]*>')
    
    ...
    
    def test_home_page_returns_correct_html(self):
      request = HttpRequest()
      response = home_page(request)
      expected_html = render_to_string('home.html')
      self.assertEqual(
          re.sub(self.pattern_input_csrf, '', response.content.decode()),
          re.sub(self.pattern_input_csrf, '', expected_html)
      )

```

다만 온라인 상으로는 해당 부분 오류에 대한 여러 해결책과 이야기가 있었고 다른 해결 책을 적용 해 봤을 때 
현재 버전에서는 거의 적용되지 않았다.
[https://www.reddit.com/r/learnpython/comments/3vjxzn/django_unit_testing_csrf_token_in_html_assertion/](https://www.reddit.com/r/learnpython/comments/3vjxzn/django_unit_testing_csrf_token_in_html_assertion/)
[https://groups.google.com/forum/#!topic/obey-the-testing-goat-book/fwY7ifEWKMU](https://groups.google.com/forum/#!topic/obey-the-testing-goat-book/fwY7ifEWKMU)
저자는 django 버전에 따른 문제이기 때문에 현재 e-book에 올려놓은
방법대로 한다면 문제를 해결 할 수 있으니 여기에 시간을 오래 쏟을 필요는 없다고 말해줬다.
아래는 e-book에 나와있는 코드다.

```python
def test_uses_home_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')


def test_can_save_a_POST_request(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})
    self.assertIn('A new list item', response.content.decode())
```

1회독 때에는 강사님이 알려주신 방법으로 해결했으니 e-book에 나와있는 방법을 적용해서 진해해 보도록 한다.
