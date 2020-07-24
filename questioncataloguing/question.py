from typing import List
from re import compile
import math


class _Question:
    def __init__(self):
        self.id = None
        self.name = None
        self.question = None
        self.question_attachments = None
        self.points = None

        self.type = None  # To be set by inheriting class
        self.section_id = None  # To be set by catalogue indexing

        raise NotImplementedError()

    def dict_dump(self) -> dict:
        assert isinstance(self.id, str)
        assert isinstance(self.name, str)
        assert isinstance(self.question, str)
        assert isinstance(self.question_attachments, list)
        for question_attachments in self.question_attachments:
            assert isinstance(question_attachments, str)
        assert isinstance(self.points, float)

        res = {
            'type': self.type,
            'id': self.id,
            'name': self.name,
            'question': self.question,
            'question_attachments': self.question_attachments,
            'points': self.points,
        }
        res.update(self.dict_to_dump_type_specific())
        assert 'type' in res.keys()
        return res
    
    def dict_to_dump_type_specific(self) -> dict:
        raise NotImplementedError()


def question_from_dict(d: dict) -> _Question:
    question_dict = dict(d)
    question_type = question_dict['type']
    del question_dict['type']
    question_dict['q_id'] = question_dict['id']
    del question_dict['id']

    if question_type == 'regex':
        return RegexQuestion(**question_dict)
    elif question_type == 'multiplechoice':
        return MultipleChoiceQuestion(**question_dict)
    elif question_type == 'estimation':
        return EstimationQuestion(**question_dict)
    elif question_type == 'audiodictate':
        return AudioDictate(**question_dict)
    else:
        raise ValueError('Question type unkndown: ' + question_type)


class RegexQuestion(_Question):
    def __init__(
        self,
        q_id: str,
        name: str,
        question: str,
        answer: str,
        answer_regex: str,
        question_attachments:  List[str]=[],
        points: float=1.0,
        explanation: str=None,
        explanation_attachments: List[str]=[]
    ):
        self.id = q_id
        self.name = name
        self.question = question
        self.answer = answer
        self.answer_regex = answer_regex
        self.question_attachments = question_attachments
        self.points = points
        self.explanation = explanation
        self.explanation_attachments = explanation_attachments
        self.type = 'regex'

        self._pattern = compile(self.answer_regex + '$')

    def dict_to_dump_type_specific(self) -> dict:
        res = {
            'answer': self.answer,
            'answer_regex': self.answer_regex,
            'explanation': self.explanation,
            'explanation_attachments': self.explanation_attachments
        }
        return res

    def match(self, answer: str) -> bool:
        return bool(self._pattern.match(answer))


class MultipleChoiceQuestion(_Question):
    def __init__(
        self,
        q_id: str,
        name: str,
        question: str,
        right_answer: str,
        wrong_answers: List[str],
        question_attachments: List[str]=[],
        points: float=1.0,
        explanation: str=None,
        explanation_attachments: List[str]=[]
    ):
        self.id = q_id
        self.name = name
        self.question = question
        self.right_answer = right_answer
        self.wrong_answers = wrong_answers
        self.question_attachments = question_attachments
        self.points = points
        self.explanation = explanation
        self.explanation_attachments = explanation_attachments

        self.type = 'multiplechoice'

    @property
    def correct_answer(self):
        return self.right_answer
        
    def dict_to_dump_type_specific(self):
        assert isinstance(self.right_answer, str)
        assert isinstance(self.wrong_answers, list)
        for w in self.wrong_answers:
            assert isinstance(w, str)
        assert isinstance(self.explanation, str) or self.explanation == None
        assert isinstance(self.explanation_attachments, list)
        for e in self.explanation_attachments:
            assert isinstance(e, str)

        res = {
            'right_answer': self.right_answer,
            'wrong_answers': self.wrong_answers,
            'explanation': self.explanation,
            'explanation_attachments': self.explanation_attachments
        }
        return res


class EstimationQuestion(_Question):
    def __init__(
        self,
        q_id: str,
        name: str,
        question: str,
        right_answer: float,
        expected_deviation: float=None,
        question_attachments: List[str]=[],
        points: float=1.0
    ):
        self.id = q_id
        self.name = name
        self.question = question
        self.right_answer = right_answer
        self.expected_deviation = expected_deviation
        self.question_attachments = question_attachments
        self.points = points

        self.type = 'estimation'

        if not self.expected_deviation:
            self.expected_deviation = self.right_answer / 3

    def dict_to_dump_type_specific(self):
        res = {
            'right_answer': self.right_answer,
            'expected_deviation': self.expected_deviation
        }
        return res

    def evaluate_score(self, answer: float):
        # Gauss
        exp = - (answer - self.right_answer)**2 / (2 * self.expected_deviation ** 2)
        score = math.pow(math.e, exp)

        return score


class AudioDictate(_Question):
    def __init__(
        self,
        q_id,
        name,
        question,
        right_answer,
        answer_regex,
        countdown: int=3,
        points: float=1,
        question_attachments: List[str]=[],
    ):
        self.type = 'audiodictate'
        self.id = q_id
        self.name = name
        self.question = question
        self.right_answer = right_answer
        self.answer_regex = answer_regex
        self.countdown = countdown
        self.points = points
        self.question_attachments = question_attachments

        self._pattern = compile(self.answer_regex + '$')

    def dict_to_dump_type_specific(self) -> dict:
        res = {
            'right_answer': self.right_answer,
            'answer_regex': self.answer_regex,
            'countdown': self.countdown,
        }
        return res

    def match(self, answer: str) -> bool:
        return bool(self._pattern.match(answer))
