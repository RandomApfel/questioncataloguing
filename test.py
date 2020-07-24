#!/usr/bin/python3
from questioncataloguing import (
    Catalogue,
    Section,
    MultipleChoiceQuestion,
    RegexQuestion,
    EstimationQuestion,
    question_from_dict,
    catalogue_from_dict,
    copy_to_mediadir
)
from json import dumps, loads
from time import time


c = Catalogue(
    catalogue_id='test0',
    name='Katalog 1',
    description='Ein Fragenkatalog blah blah.'
)

for sec in ['sec{}'.format(i) for i in range(12)]:
    s = Section(sec, 'Sektion 1')
    c.append_section(s)

    for i in range(250):
        q0 = MultipleChoiceQuestion(q_id='qa'+str(i), name='Question 1',  question='What??', right_answer='Foobar', wrong_answers=['no', 'no'])
        q0 = question_from_dict(q0.dict_dump())

        q1 = RegexQuestion(q_id='qb'+str(i), name='Question 2', question='Word starting with a?', answer='z.B. Affe', answer_regex=r'[aA].*')
        q1 = question_from_dict(q1.dict_dump())

        q2 = EstimationQuestion(q_id='qc'+str(i), name='Question 3', question='1 km in feet', right_answer=3280.84, expected_deviation=700)
        q2 = question_from_dict(q2.dict_dump())

        s.append_question(q0)
        s.append_question(q1)
        s.append_question(q2)

start = time()
dump_string = dumps(c.dict_dump())
end = time()

print('Storing duration:', end - start)

start = time()
restored_catalogue = catalogue_from_dict(loads(dump_string))
end = time()
print('Restoring duration:', end - start)

start = time()
estimate_question = restored_catalogue.get_section('sec11').get_question('qc249')
end = time()
print('Get last question duration', end - start)

copy_to_mediadir('questioncataloguing/section.py', mediadir='mediadir')

