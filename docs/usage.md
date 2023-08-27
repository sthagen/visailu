# Usage

Simple quiz data managing application - probably not useful to many.

## Synopsis

```console
❯ visailu

 Usage: visailu [OPTIONS] COMMAND [ARGS]...

 Quiz (Finnish: visailu) data operations.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version  -V        Display the application version and exit                                                        │
│ --help     -h        Show this message and exit.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ publish            Publish the model data in simplified JSON syntax.                                                 │
│ validate           Validate the YAML data against the model.                                                         │
│ verify             Verify the model data against YAML syntax.                                                        │
│ version            Display the application version and exit.                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

### Verification

Invalid YAML syntax example:

```console
❯ visailu verify test/fixtures/basic/abuse/invalid-yaml.yml
2023-08-27T13:20:13.577587+00:00 ERROR [VISAILU]: pathtest/fixtures/basic/abuse/invalid-yaml.yml is not a valid YAML file. Details: mapping values are not allowed here in "test/fixtures/basic/abuse/invalid-yaml.yml", line 1, column 14
```

Note: Invalid YAML files will produce a log output and return a non-zero code to the calling process.
Successful verification will return the code `0` and produce no output log.

Valid YAML syntax example:

```console
❯ visailu verify test/fixtures/basic/use/minimal.yml
```

### Validation

Invalid Model example (missing any questions):

```console
❯ visailu validate test/fixtures/basic/abuse/model-missing-questions.yml
2023-08-27T13:25:23.335820+00:00 ERROR [VISAILU]: path test/fixtures/basic/abuse/model-missing-questions.yml misses model values
```

Valid Model example:

```console
❯ visailu validate test/fixtures/basic/use/minimal.yml
```

### Publication

Failing publication due to invalid Model example (missing any questions):

```console
❯ visailu publish test/fixtures/basic/abuse/model-missing-questions.yml
2023-08-27T13:25:49.312231+00:00 ERROR [VISAILU]: path test/fixtures/basic/abuse/model-missing-questions.yml misses model values
```

Succeeding publication example (albeit with warnings):

```console
❯ visailu publish test/fixtures/basic/use/questions-answers-counts-differing.yml
2023-08-27T13:35:41.776461+00:00 WARNING [VISAILU]: model with too few questions 9 instead of 10
2023-08-27T13:35:41.776941+00:00 WARNING [VISAILU]: model with too few answers 1 instead of 4 at question 1
2023-08-27T13:35:41.776962+00:00 WARNING [VISAILU]: model with too few answers 3 instead of 4 at question 2
2023-08-27T13:35:41.776980+00:00 WARNING [VISAILU]: model with too few answers 3 instead of 4 at question 4
2023-08-27T13:35:41.776996+00:00 WARNING [VISAILU]: model with too many answers 12 instead of 4 at question 5
2023-08-27T13:35:41.777010+00:00 WARNING [VISAILU]: model with too few answers 1 instead of 4 at question 6
2023-08-27T13:35:41.777022+00:00 WARNING [VISAILU]: model with too few answers 2 instead of 4 at question 7
2023-08-27T13:35:41.777039+00:00 WARNING [VISAILU]: model with too many answers 5 instead of 4 at question 8
2023-08-27T13:35:41.777063+00:00 WARNING [VISAILU]: model with too few answers 3 instead of 4 at question 9
2023-08-27T13:35:41.777076+00:00 WARNING [VISAILU]: quiz with too few questions 9 instead of 10
2023-08-27T13:35:41.777314+00:00 INFO [VISAILU]: published quiz data at build/questions-answers-counts-differing.json (from model at test/fixtures/basic/use/questions-answers-counts-differing.yml)
```

Following the prior successful publish command on a clean folder tree the result is:

```console
❯ tree build
build
└── questions-answers-counts-differing.json

1 directory, 1 file

```

But be aware, that the authors SHOULD fix the mismatches (too few questions for example and varying answer counts)
in the model (YAML format) and publish again instead of wasting time editing the generated JSON file.

Where the input was:

```yaml
---
id: some-id-questions-answers-counts-differing
title: Questions Answers Counts Differing
meta:
  scale:
    domain: text
    range: binary
  defaults:
    rating: false
questions:
- question: ABC1 stands for ...?
  answers:
  - answer: Et cetera1
    rating: true
- question: ABC2 stands for ...?
  answers:
  - answer: A company2
  - answer: A Bogus Car2
    rating: true
  - answer: Et cetera2
- question: ABC3 stands for ...?
  answers:
  - answer: Alphabet3
  - answer: A company3
  - answer: A Bogus Car3
    rating: true
  - answer: Et cetera3
- question: ABC4 stands for ...?
  answers:
  - answer: Alphabet4
  - answer: A Bogus Car4
    rating: true
  - answer: Et cetera4
- question: ABC5 stands for ...?
  answers:
  - answer: Alphabet5
  - answer: Alphabet51
  - answer: Alphabet52
  - answer: Alphabet53
  - answer: Alphabet54
  - answer: Alphabet55
  - answer: Alphabet56
  - answer: Alphabet57
  - answer: Alphabet58
  - answer: A company5
  - answer: A Bogus Car5
    rating: true
  - answer: Et cetera5
- question: ABC6 stands for ...?
  answers:
  - answer: A Bogus Car6
    rating: true
- question: ABC7 stands for ...?
  answers:
  - answer: A Bogus Car7
    rating: true
  - answer: Et cetera7
- question: ABC8 stands for ...?
  answers:
  - answer: AlphabetX8
  - answer: Alphabet8
  - answer: A company8
  - answer: A Bogus Car8
    rating: true
  - answer: Et cetera8
- question: ABC9 stands for ...?
  answers:
  - answer: Alphabet9
  - answer: A Bogus Car9
    rating: true
  - answer: Et cetera9
```

and the output (quiz export) is (not useful):

```json
[
  {
    "id": 1,
    "question": "ABC1 stands for ...?",
    "options": [
      {
        "answer": "Et cetera1",
        "isCorrect": true
      }
    ]
  },
  {
    "id": 2,
    "question": "ABC2 stands for ...?",
    "options": [
      {
        "answer": "A company2",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car2",
        "isCorrect": true
      },
      {
        "answer": "Et cetera2",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 3,
    "question": "ABC3 stands for ...?",
    "options": [
      {
        "answer": "Alphabet3",
        "isCorrect": false
      },
      {
        "answer": "A company3",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car3",
        "isCorrect": true
      },
      {
        "answer": "Et cetera3",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 4,
    "question": "ABC4 stands for ...?",
    "options": [
      {
        "answer": "Alphabet4",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car4",
        "isCorrect": true
      },
      {
        "answer": "Et cetera4",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 5,
    "question": "ABC5 stands for ...?",
    "options": [
      {
        "answer": "Alphabet5",
        "isCorrect": false
      },
      {
        "answer": "Alphabet51",
        "isCorrect": false
      },
      {
        "answer": "Alphabet52",
        "isCorrect": false
      },
      {
        "answer": "Alphabet53",
        "isCorrect": false
      },
      {
        "answer": "Alphabet54",
        "isCorrect": false
      },
      {
        "answer": "Alphabet55",
        "isCorrect": false
      },
      {
        "answer": "Alphabet56",
        "isCorrect": false
      },
      {
        "answer": "Alphabet57",
        "isCorrect": false
      },
      {
        "answer": "Alphabet58",
        "isCorrect": false
      },
      {
        "answer": "A company5",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car5",
        "isCorrect": true
      },
      {
        "answer": "Et cetera5",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 6,
    "question": "ABC6 stands for ...?",
    "options": [
      {
        "answer": "A Bogus Car6",
        "isCorrect": true
      }
    ]
  },
  {
    "id": 7,
    "question": "ABC7 stands for ...?",
    "options": [
      {
        "answer": "A Bogus Car7",
        "isCorrect": true
      },
      {
        "answer": "Et cetera7",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 8,
    "question": "ABC8 stands for ...?",
    "options": [
      {
        "answer": "AlphabetX8",
        "isCorrect": false
      },
      {
        "answer": "Alphabet8",
        "isCorrect": false
      },
      {
        "answer": "A company8",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car8",
        "isCorrect": true
      },
      {
        "answer": "Et cetera8",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 9,
    "question": "ABC9 stands for ...?",
    "options": [
      {
        "answer": "Alphabet9",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car9",
        "isCorrect": true
      },
      {
        "answer": "Et cetera9",
        "isCorrect": false
      }
    ]
  }
]
```

A correct example with ten questions in the model (input data) namely `test/fixtures/basic/use/ten.yml`:

```yaml
---
id: some-id-ten
title: Some Title Ten
meta:
  scale:
    domain: text
    range: binary
  defaults:
    rating: false
questions:
- question: ABC1 stands for ...?
  answers:
  - answer: Alphabet1
  - answer: A company1
  - answer: A Bogus Car1
    rating: true
  - answer: Et cetera1
- question: ABC2 stands for ...?
  answers:
  - answer: Alphabet2
  - answer: A company2
  - answer: A Bogus Car2
    rating: true
  - answer: Et cetera2
- question: ABC3 stands for ...?
  answers:
  - answer: Alphabet3
  - answer: A company3
  - answer: A Bogus Car3
    rating: true
  - answer: Et cetera3
- question: ABC4 stands for ...?
  answers:
  - answer: Alphabet4
  - answer: A company4
  - answer: A Bogus Car4
    rating: true
  - answer: Et cetera4
- question: ABC5 stands for ...?
  answers:
  - answer: Alphabet5
  - answer: A company5
  - answer: A Bogus Car5
    rating: true
  - answer: Et cetera5
- question: ABC6 stands for ...?
  answers:
  - answer: Alphabet6
  - answer: A company6
  - answer: A Bogus Car6
    rating: true
  - answer: Et cetera6
- question: ABC7 stands for ...?
  answers:
  - answer: Alphabet7
  - answer: A company7
  - answer: A Bogus Car7
    rating: true
  - answer: Et cetera7
- question: ABC8 stands for ...?
  answers:
  - answer: Alphabet8
  - answer: A company8
  - answer: A Bogus Car8
    rating: true
  - answer: Et cetera8
- question: ABC9 stands for ...?
  answers:
  - answer: Alphabet9
  - answer: A company9
  - answer: A Bogus Car9
    rating: true
  - answer: Et cetera9
- question: ABC10 stands for ...?
  answers:
  - answer: Alphabet10
  - answer: A company10
  - answer: A Bogus Car10
    rating: true
  - answer: Et cetera10
```

The execution:

```console
❯ visailu publish test/fixtures/basic/use/ten.yml
2023-08-27T13:35:13.696157+00:00 INFO [VISAILU]: published quiz data at build/ten.json (from model at test/fixtures/basic/use/ten.yml)
```

Which produces the folloing naive quiz data export (in JSON format within the build folder):

```console
❯ tree build
build
└── ten.json

1 directory, 1 file
```

The quiz export file `build/ten.json` has the following content:

```json
[
  {
    "id": 1,
    "question": "ABC1 stands for ...?",
    "options": [
      {
        "answer": "Alphabet1",
        "isCorrect": false
      },
      {
        "answer": "A company1",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car1",
        "isCorrect": true
      },
      {
        "answer": "Et cetera1",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 2,
    "question": "ABC2 stands for ...?",
    "options": [
      {
        "answer": "Alphabet2",
        "isCorrect": false
      },
      {
        "answer": "A company2",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car2",
        "isCorrect": true
      },
      {
        "answer": "Et cetera2",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 3,
    "question": "ABC3 stands for ...?",
    "options": [
      {
        "answer": "Alphabet3",
        "isCorrect": false
      },
      {
        "answer": "A company3",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car3",
        "isCorrect": true
      },
      {
        "answer": "Et cetera3",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 4,
    "question": "ABC4 stands for ...?",
    "options": [
      {
        "answer": "Alphabet4",
        "isCorrect": false
      },
      {
        "answer": "A company4",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car4",
        "isCorrect": true
      },
      {
        "answer": "Et cetera4",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 5,
    "question": "ABC5 stands for ...?",
    "options": [
      {
        "answer": "Alphabet5",
        "isCorrect": false
      },
      {
        "answer": "A company5",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car5",
        "isCorrect": true
      },
      {
        "answer": "Et cetera5",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 6,
    "question": "ABC6 stands for ...?",
    "options": [
      {
        "answer": "Alphabet6",
        "isCorrect": false
      },
      {
        "answer": "A company6",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car6",
        "isCorrect": true
      },
      {
        "answer": "Et cetera6",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 7,
    "question": "ABC7 stands for ...?",
    "options": [
      {
        "answer": "Alphabet7",
        "isCorrect": false
      },
      {
        "answer": "A company7",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car7",
        "isCorrect": true
      },
      {
        "answer": "Et cetera7",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 8,
    "question": "ABC8 stands for ...?",
    "options": [
      {
        "answer": "Alphabet8",
        "isCorrect": false
      },
      {
        "answer": "A company8",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car8",
        "isCorrect": true
      },
      {
        "answer": "Et cetera8",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 9,
    "question": "ABC9 stands for ...?",
    "options": [
      {
        "answer": "Alphabet9",
        "isCorrect": false
      },
      {
        "answer": "A company9",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car9",
        "isCorrect": true
      },
      {
        "answer": "Et cetera9",
        "isCorrect": false
      }
    ]
  },
  {
    "id": 10,
    "question": "ABC10 stands for ...?",
    "options": [
      {
        "answer": "Alphabet10",
        "isCorrect": false
      },
      {
        "answer": "A company10",
        "isCorrect": false
      },
      {
        "answer": "A Bogus Car10",
        "isCorrect": true
      },
      {
        "answer": "Et cetera10",
        "isCorrect": false
      }
    ]
  }
]
```

### Version

```console
❯ visailu version
Quiz (Finnish: visailu) data operations. version 2023.8.25+parent.fb1e0e78
```
