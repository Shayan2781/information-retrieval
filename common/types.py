from typing import TypedDict, List
class Document(TypedDict):
      id: str
      title: str
      content: str
      tags: List[str]
      date: str
      url: str
      category: str

class Posting(TypedDict):
      doc_id: str
      positions: List[int]
      term_freq: str

class Posting_List(TypedDict):
      freq: int
      postings: List[Posting] 
