from time import time
from .section import Section, section_from_dict
from .question import _Question

class Catalogue:
    def __init__(self, catalogue_id, name, description, supported_modes=[], buildtime=None, mediadir=None):
        self.id = catalogue_id
        self.name = name
        self.description = description
        self.buildtime = buildtime
        self.mediadir = mediadir
        self.supported_modes = supported_modes
        self._sections = {}

        if not self.buildtime:
            self.buildtime = int(time())

    def append_section(self, section: Section):
        self._sections[section.id] = section

    def dict_dump(self) -> dict:
        assert isinstance(self.name, str)
        assert isinstance(self.description, str) or self.description == None
        assert isinstance(self.supported_modes, list)
        assert isinstance(self.buildtime, int)

        res = {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'buildtime': self.buildtime,
            'supported_modes': self.supported_modes,
            'sections': {
                s.id: s.dict_dump() for s in self._sections.values()
            }
        }
        return res

    def get_question(self, section_id: str, question_id: str) -> _Question:
        return self._sections[section_id].get_question(question_id=question_id)

    def get_section(self, section_id: str=None, section_title: str=None) -> Section:
        if not section_id is None:
            return self._sections.get(section_id)
        
        if section_title:
            for s in self._sections.values():
                if section_title.lower() in s.name.lower():
                    return s
            return None

        return None

    def get_all_questions(self, section_id: str=None):
        sections = self._sections
        if section_id:
            sections = [self.get_section(section_id=section_id)]

        questions = []
        for s in sections.values():
            questions += s._questions

        return questions

    def get_all_sections(self):
        sections = []
        for key in sorted(self._sections.keys()):
            sections.append(self._sections[key])
        return sections

    def generate_index(self):
        for s in self._sections.values():
            for q in s._questions.values():
                q.section_id = s.id

def catalogue_from_dict(c: dict) -> Catalogue:
    new_catalogue = Catalogue(c['id'], c['name'], c['description'], c['buildtime'])
    for sec in c['sections'].values():
        new_catalogue.append_section(section_from_dict(sec))
    new_catalogue.generate_index()
    return new_catalogue


def copy_to_mediadir(filepath, mediadir='media') -> str:
    from hashlib import blake2b
    from os import path, makedirs
    from shutil import copyfile

    makedirs(mediadir, exist_ok=True)

    with open(filepath, 'rb') as f:
        filehash = blake2b()
        while True:
            chunk = f.read(8 * 1024)
            if not chunk:
                break
            filehash.update(chunk)

    old_filename = path.basename(filepath)
    new_filename = '{}.{}'.format(
        filehash.hexdigest()[:32],
        old_filename.split('.')[-1]
    )

    if path.isfile(mediadir + '/' + new_filename):
        return new_filename

    copyfile(filepath, mediadir + '/' + new_filename)
    
    return new_filename
