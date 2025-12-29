import math
from typing import Dict, List, Tuple
from collections import defaultdict
from common.types import Posting_List, Document
from linguisticmodule import tokenize_document

def calculate_cosine_similarity_for_query(
    inverted_index: Dict[str, Posting_List],
    documents: Dict[str, Document],  # Document metadata including title and content
    query: List[str],
    number_of_results: int,
    champion_lists: Dict[str, List[Dict[str, int]]] = None,
    use_champion_list: bool = False
) -> List[Tuple[str, str, float, List[str]]]:
    # Total number of documents
    total_docs = len(set(posting['doc_id'] for postings in inverted_index.values() for posting in postings['postings']))
    
    # Step 1: Compute TF-IDF for the query
    query_term_freq = {term: query.count(term) for term in query}
    query_vector = {}
    query_magnitude = 0

    for term, freq in query_term_freq.items():
        if term not in inverted_index:
            continue  # Skip terms not in the inverted index
        idf = math.log((1 + total_docs) / (1 + len(inverted_index[term]['postings']))) + 1
        tf_idf = (math.log2(freq) + 1) * idf
        query_vector[term] = tf_idf
        query_magnitude += tf_idf ** 2

    query_magnitude = math.sqrt(query_magnitude)

    # Step 2: Identify relevant documents using Champion Lists or full postings
    relevant_docs = defaultdict(lambda: {"dot_product": 0, "doc_magnitude": 0, "positions": defaultdict(list)})

    for term, query_tf_idf in query_vector.items():
        if term not in inverted_index:
            continue
        
        # Use Champion List or full postings
        postings = champion_lists[term] if use_champion_list and term in champion_lists else inverted_index[term]['postings']
        
        for posting in postings:
            doc_id = posting['doc_id']
            term_freq = posting['term_freq']
            idf = math.log((1 + total_docs) / (1 + len(inverted_index[term]['postings']))) + 1
            doc_tf_idf = (math.log2(term_freq) + 1) * idf

            # Update dot product, document magnitude, and record positions
            relevant_docs[doc_id]["dot_product"] += query_tf_idf * doc_tf_idf
            relevant_docs[doc_id]["doc_magnitude"] += doc_tf_idf ** 2
            relevant_docs[doc_id]["positions"][term].extend(posting['positions'])

    # Step 3: Calculate cosine similarity and prepare results
    results = []
    for doc_id, scores in relevant_docs.items():
        doc_magnitude = math.sqrt(scores["doc_magnitude"])
        if query_magnitude * doc_magnitude > 0:
            cosine_similarity = scores["dot_product"] / (query_magnitude * doc_magnitude)
        else:
            cosine_similarity = 0.0

        # Extract document title
        title = documents[doc_id]["title"]

        # Extract parts of the document where query terms were used
        positions = scores["positions"]
        parts = []  # Use a set to avoid duplicate snippets
        content = tokenize_document(documents[doc_id]['content'])

        for term, pos_list in positions.items():
            for pos in pos_list:
                # Ensure the snippet contains the actual query term
                if content[pos] == term:
                    new_content = documents[doc_id]['content'].split()
                    start = max(pos - 5, 0)
                    end = min(pos + 6, len(new_content))
                    parts.append(" ".join(new_content[start:end]))

        results.append((doc_id, title, cosine_similarity, parts))

    # Step 4: Sort by similarity score and return top results
    return sorted(results, key=lambda x: x[2], reverse=True)[:number_of_results]