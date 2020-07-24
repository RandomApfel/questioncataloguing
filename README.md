# Question Cataloguing
A python module to create, store and restore
question catalogues.

A catalogue contains sections.  
A section contains questions.  
A question can be either
- a multiple choice question
- a text answer question (regex)
- an estimation question
- an audio dictate

## Usage
How to create a catalogue?

```python
from questioncataloguing import (
    Catalogue,
    Section,
    MultipleChoiceQuestion,
    RegexQuestion,
    EstimationQuestion,
    AudioDictate,
)

q0 = MultipleChoiceQuestion(
    q_id='q0',  # globally unique
    name='Question 1',
    question='What is the biggest animal currently on earth?',
    right_answer='The Blue Whale',
    wrong_questions=['The Rabbit', 'The Elephant', 'The Mouse']
)
q1 = RegexQuestion(
    q_id='q1',
    name='Question 2',
    question='What is the biggest animal currently on earth?',
    answer='Blue Whale',
    answer_regex=r'(a )?blue whale(s)?'
)
q2 = EstimationQuestion(
    q_id='q2',
    name='Question 3',
    question='How long is a blue whale in meters?',
    right_answer=25,
    expected_deviation=4,  # optional
    points=2  # optionale
)
q3 = AudioDictate(
    q_id='q3',
    name='Question 3',
    question='Say Eyjafjallajökull.'
    right_answer='Eyjafjallajökull',
    answer_regex=r'e(j|y)af(j|y)alla(j|y)(oe|o|ö)kull'
)


section0 = Section('section0', 'Section 1')
section0.append_question(q0)
section0.append_question(q1)
section0.append_question(q2)
section0.append_question(q3)

catalogue = Catalogue(
    catalogue_id='all_around_the_globe_0',
    name='All around the world',
    description='Test your knowledge about the world'
)
catalogue.append_section(section0)

```

How to dump a catalogue?
```python
from json import dumps
from questioncataloguing import Catalogue

c = Catalogue()
# add sections and questions

with open('catalogue_dump.json', 'w') as f:
    json_dump = dumps(c.dict_dump())
    f.write(json_dump)
```

How to restore a catalogue dump?
```python
from json import loads
from questioncataloguing import catalogue_from_dict

with open('catalogue_dump.json', 'r') as f:
    json_dumps = f.read()
    catalogue_from_dict(loads(json_dumps))

```

## Structure
The struture of a code is the folloing:  
* Catalogue
    * Metadata
    * Section List
    * Section_<id>
        * Question_<id>

## Question Types
Generic Data Members every Question has
```json
{
    "id": "unique id",
    "name": "human readable name",
    "question": "the question itself",
    "question_attachments": ["filename.ending"],
    "points": 1.0
}
```

Regex Answer
```json
{
    ...
    "answer": "answer human readable",
    "answer_regex": "regex expression to match answer",
    "explanation": "(opt) explanation for answer",
    "explanation_attachments": ["filename.ending"]
}
```

Multiple Choice
```json
{
    ...
    "right_answer": "right answer",
    "wrong_answers": ["wrong answer"],
    "explanation": "(opt) explanation for answer",
    "explanation_attachments": ["filename.ending"]
}
```

Estimation
```json
{
    ...
    "right_answer": 1000.5,
    "expected_deviation": 200,
}
```

## Building
To create a Python Wheel run
```bash
python3 setup.py bdist_wheel
```

To install it run
```bash
python3 -m pip install dist/questioncataloguing-*.*.*-py-none-any-whl
# or
python3 -m pip install .
```
