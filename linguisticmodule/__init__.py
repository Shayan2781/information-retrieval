import re
from parsivar import FindStems
stemmer = FindStems()
def tokenize_document(content: str):
      normalized_content = _normalize_persian(content)
      token_list = normalized_content.split()
      stemmed_list = list(map(stem_word, token_list))
      return stemmed_list


      
def _normalize_persian(text: str) -> str:
      half_space = chr(8204)
      text = re.sub(r'\b(می|ها|تر|ترین)\s+', r'\1' + half_space, text)
      text = re.sub(r'\s+(می|ها|تر|ترین)\b', half_space + r'\1', text)
      text = text.replace('ك', 'ک').replace('ي', 'ی').replace(',', '').replace(':', '').replace('.', '')
      text = re.sub(r'\s+', ' ', text).strip()
      text = re.sub(r'[\u064B-\u0652\u06CC\u064E\u064F\u0650\u0670\u0651\u0654\u0653\u0655\u0656]', '', text)
      text = re.sub(r'[!-@[-_\]*)]', '', text)
      return text

def stem_word(word: str) -> str:
      return stemmer.convert_to_stem(word)




   