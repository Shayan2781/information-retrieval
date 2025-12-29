import json
from common.types import Document, Posting_List
from typing import Dict, List
from linguisticmodule import tokenize_document

def create_inverted_index(path: str):
      print("\033[33mCreating Inverted Index\033[0m")
      data = _load_documents(path)
      inverted_index: Dict[str, Posting_List] = {}
      bar_length = 30  # Length of the progress bar


      num_of_docs = len(data.items())
      for doc_id, document in data.items():
            percentage = (int(doc_id) + 1) / num_of_docs * 100
            progress = int(bar_length * (int(doc_id) + 1) / num_of_docs)
            bar = "#" * progress + "-" * (bar_length - progress)
            print(f"\r[{bar}] {int(doc_id) + 1}/{num_of_docs} ({percentage:.2f}%)", end="")
            tokens = tokenize_document(document['content'])

            term_positions: Dict[str, List[int]] = {}
            
            for position, token in enumerate(tokens):
                  if token not in term_positions:
                        term_positions[token] = []
                  term_positions[token].append(position)
            
            for token, positions in term_positions.items():
                  if token not in inverted_index:
                        inverted_index[token] = {
                        'freq': 0,
                        'postings': []
                        }
                  
                  inverted_index[token]['freq'] += 1
                  inverted_index[token]['postings'].append({
                  'doc_id': doc_id,
                  'positions': positions,
                  'term_freq': len(positions)
                  })
      
      print("\n\033[92mInverted Index Created!\033[0m")
      
      return _remove_top_terms(inverted_index), data
                 


           

def _load_documents(path: str) -> Dict[str, Document]:
      with open(path, 'r') as file:
        data = json.load(file) 
      documents: Dict[str, Document] = {}
      for doc_id, doc_data in data.items():
            document = Document(
                 id=doc_id,
                 title=doc_data.get("title", ""),
                 content=doc_data.get("content", ""),
                 tags=doc_data.get("tags", []),
                 date=doc_data.get("date", ""),
                 url=doc_data.get("url", ""),
                 category=doc_data.get("category", ""),
            )
            documents[doc_id] = document
      return documents


def _remove_top_terms(inverted_index: Dict[str, Posting_List], top_n: int = 50) -> Dict[str, Posting_List]:

    sorted_terms = sorted(inverted_index.items(), key=lambda x: x[1]['freq'], reverse=True)
    
    terms_to_remove = [term for term, _ in sorted_terms[:top_n]]
    
    print(f"\033[33mRemoving top {top_n} terms\033[0m")
    for term in terms_to_remove:
        print(f"{term}, freq: {inverted_index[term]['freq']}")
        inverted_index.pop(term, None)
    
    return inverted_index

def create_champion_lists(inverted_index: Dict[str, Posting_List], k: int) -> Dict[str, List[Dict[str, int]]]:
    champion_lists = {}
    print("\033[33mCreating Champions Lists\033[0m")
    bar_length = 30  # Length of the progress bar
    num_of_docs = len(inverted_index.items())
    current = 0

    for term, posting_list in inverted_index.items():
      percentage = (int(current) + 1) / num_of_docs * 100
      progress = int(bar_length * (int(current) + 1) / num_of_docs)
      bar = "#" * progress + "-" * (bar_length - progress)
      print(f"\r[{bar}] {int(current) + 1}/{num_of_docs} ({percentage:.2f}%)", end="")
      sorted_postings = sorted(posting_list['postings'], key=lambda x: x['term_freq'], reverse=True)
      champion_lists[term] = sorted_postings[:k]
      current += 1

    return champion_lists
