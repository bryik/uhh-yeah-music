from dataclasses import dataclass
from typing import Union


@dataclass
class Episode:
    date: str
    number: int
    linkToNotes: str
    intro: Union[str, None] = None
    outro: Union[str, None] = None

    def todict(self):
        return {
            "date": self.date,
            "number": self.number,
            "linkToNotes": self.linkToNotes,
            "intro": self.intro,
            "outro": self.outro,
        }

    # To allow compatability with Set.
    def __eq__(self, other):
        return self.number == other.number

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.number)

