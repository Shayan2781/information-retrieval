from invertedindex import create_inverted_index, create_champion_lists
from retrievingmodule import calculate_cosine_similarity_for_query
from linguisticmodule import tokenize_document
from transformers import AutoTokenizer, AutoModel
from bert.retrievingmodule import find_top_d_docs, compute_embedding
from bert.clusteringmodule import cluster_documents, load_docs_embeddings, predict_query_cluster, KMeans, load_all_clustered_docs_embeddings
from bert import process_documents
from bert.faiss import build_faiss_index, search_faiss

if __name__ == '__main__':
    # Original Project
    inverted_index, docs = create_inverted_index('Data/IR_data_news_12k.json')
    champion_lists = create_champion_lists(inverted_index, 10)


    while True:
        query = input("\nEnter Query:")
        query_tokens = tokenize_document(query)

        result = calculate_cosine_similarity_for_query(inverted_index, docs, query_tokens, 10, champion_lists, True)
        for res in result:
            print(f"doc_id: { res[0] }")
            print(f"title: { res[1] }")
            print(f"similarity: { res[2] }")
            print(f"sentences: { res[3] }")
            print(">>>>>>>>>>>")




    #Bonus Project
    

    ## P1-2
    # model_name = "bert-fa-zwnj-base"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModel.from_pretrained(model_name)
    # model.eval()
    # process_documents('Data/IR_bonus_dataset.json', tokenizer, model)
    # query_text = "باشگاه فوتبال" 
    # d = 3 
    # docs_folder = "bert_datas" 

    # top_docs = find_top_d_docs(query_text, d, docs_folder, tokenizer, model)

    # print("شبیه‌ترین اسناد به کوئری:")
    # for sim_score, doc_id, content in top_docs:
    #     print(f"\nDoc ID: {doc_id}")
    #     print(f"Similarity: {sim_score:.4f}")
    #     print(f"Content: {content}")

    ##P3
    # docs_folder = "bert_datas"

    # n_clusters = 10
    # cluster_documents(docs_folder, n_clusters, 'clusters' )
    # doc_ids, embeddings = load_all_clustered_docs_embeddings("clusters")
    # kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    # kmeans.fit(embeddings)

    # model_name = "bert-fa-zwnj-base"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModel.from_pretrained(model_name)
    # model.eval()
 
    # query_text = "باشگاه فوتبال"
    # predicted_cluster = predict_query_cluster(query_text, None, kmeans, tokenizer, model)
    # print(f"The queries predicted cluster was cluster_{predicted_cluster}")
    # top_docs = find_top_d_docs(query_text, 10, f'clusters/cluster_{predicted_cluster}', tokenizer, model)
    # for sim_score, doc_id, content in top_docs:
    #     print(f"\nDoc ID: {doc_id}")
    #     print(f"Similarity: {sim_score:.4f}")
    #     print(f"Content: {content}")    
        



    #P4
    # docs_folder = "bert_datas"

    # doc_ids, embeddings, _ = load_docs_embeddings(docs_folder)
    # index = build_faiss_index(embeddings) 

    # model_name = "bert-fa-zwnj-base"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModel.from_pretrained(model_name)
    # model.eval()
    # query_text = "باشگاه فوتبال"
    # query_emb = compute_embedding(query_text, tokenizer, model)
    # top_k = 5
    # distances, indices = search_faiss(index, query_emb, top_k=top_k)
    # print("Results (nearest neighbors):")

    # for rank, (dist, idx) in enumerate(zip(distances[0], indices[0]), start=1):
    #     doc_id = doc_ids[idx]
    #     print(f"{rank}) doc_id={doc_id}, distance={dist:.4f}")
  

    

