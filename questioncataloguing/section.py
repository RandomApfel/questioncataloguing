from typing import Dict
from .question import _Question, question_from_dict


class Section:
    def __init__(self, s_id: str, name: str):
        self.id: str = s_id
        self.name: str = name
        self._questions: Dict[_Question] = {}

    def append_question(self, question: _Question):
        self._questions[question.id] = question

    def get_question(self, question_id: str=None, question_name: str=None) -> _Question:
        if question_id:
            return self._questions.get(question_id, None)

        if question_name:
            for q in self._questions.values():
                if question_name.lower() in q.name.lower():
                    return q
            return None

        return None

    def get_all_questions(self):
        sections = []
        for key in sorted(self._questions.keys()):
            sections.append(self._questions[key])
        return sections

    @property
    def question_count(self):
        return len(self._questions)

    def dict_dump(self) -> dict:
        assert isinstance(self.id, str)
        assert isinstance(self.name, str)

        res = {
            'id': self.id,
            'name': self.name,
            'questions': {
                q.id: q.dict_dump() for q in self._questions.values()
            }
        }
        return res


def section_from_dict(d: dict) -> Section:
    new_section = Section(d['id'], d['name'])
    for q in d['questions'].values():
        new_section.append_question(question_from_dict(q))
    return new_section
