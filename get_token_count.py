events_per_schema = [22,9,5,6,31,10,12,9,10,9,21,11,13,18,12,20,11,21,15,38,6,12,15,12]
average_tokens_per_event = 15

with open("data/ir_data/retrieved_docs_20perquery.txt") as f:
    docs = []
    paragraphs = []
    lines = f.readlines()
    full_docs=[]
    for line in lines:
        line = line.strip()
        if "*****" not in line:
            full_docs.append(line)
            if "query =" not in line  and "~~~" not in line  and "####" not in line :
                if line:
                    paragraphs.append(line)
    docs= " ".join(full_docs).split("#####################")
    doc_token_counter=0
    for doc in docs:
        for event_count in events_per_schema:
                prompt = "does the passage" + doc+ "entail, contradict or is neutral to the sentence" \
                         + " Answer should be one of entail, contradict or neutral. Don't retype the whole passage again."
                doc_token_counter += event_count* len(prompt.split(" "))+average_tokens_per_event
    print(f"number of tokens in all documents= {doc_token_counter}")

    para_token_counter = 0
    for para in paragraphs:
        for event in events_per_schema:
            prompt = "does the passage" + para + "entail, contradict or is neutral to the sentence" \
                     + " Answer should be one of entail, contradict or neutral. Don't retype the whole passage again."
            para_token_counter += event_count* len(prompt.split(" "))+average_tokens_per_event

    print(f"number of tokens in all paragraphs= {para_token_counter}")