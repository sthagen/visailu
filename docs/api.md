# API

The functions are documented but not yet collected in a flat api module.

Example of publishing the example from the usage docs with ten questions inside the test fixtures:

```python
❯ python
Python 3.11.4 (main, Jun 27 2023, 00:03:24) [Clang 16.0.6 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from visailu.publish import publish_path
>>> code, message, data = publish_path('test/fixtures/basic/use/ten.yml')
>>> code
0
>>> message
'published quiz data at build/ten.json (from model at test/fixtures/basic/use/ten.yml)'
>>> q_pairs = [(q['id'], q['question']) for q in data]
>>> for pair in q_pairs:
...     print(f'{pair[0] :2d} -> {pair[1]}')
...
 1 -> ABC1 stands for ...?
 2 -> ABC2 stands for ...?
 3 -> ABC3 stands for ...?
 4 -> ABC4 stands for ...?
 5 -> ABC5 stands for ...?
 6 -> ABC6 stands for ...?
 7 -> ABC7 stands for ...?
 8 -> ABC8 stands for ...?
 9 -> ABC9 stands for ...?
10 -> ABC10 stands for ...?
>>> import json
>>> with open('build/ten.json', 'rt', encoding='utf-8') as handle:
...     quiz = json.load(handle)
...
>>> pairs = [(q['id'], q['question']) for q in quiz]
>>> for pair in pairs:
...     print(f'{pair[0] :2d} -> {pair[1]}')
...
 1 -> ABC1 stands for ...?
 2 -> ABC2 stands for ...?
 3 -> ABC3 stands for ...?
 4 -> ABC4 stands for ...?
 5 -> ABC5 stands for ...?
 6 -> ABC6 stands for ...?
 7 -> ABC7 stands for ...?
 8 -> ABC8 stands for ...?
 9 -> ABC9 stands for ...?
10 -> ABC10 stands for ...?
>>> data == quiz
True
>>>
```
