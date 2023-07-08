

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
    events = [0]*10
    for doc in docs:
        for event in events:
            prompt = "does the passage" + doc+ "entail, contradict or is neutral to the sentence" \
                     +"A phisher sends a message to a target's email address" \
                     + " Answer should be one of entail, contradict or neutral. Don't retype the whole passage again."
            doc_token_counter += len(prompt.split(" "))

    print(f"number of tokens in all documents= {doc_token_counter}")

    para_token_counter = 0
    for para in paragraphs:
        for event in events:
            prompt = "does the passage" + para + "entail, contradict or is neutral to the sentence" \
                     +"A phisher sends a message to a target's email address" \
                     + " Answer should be one of entail, contradict or neutral. Don't retype the whole passage again."
            para_token_counter += len(prompt.split(" "))

    print(f"number of tokens in all documents= {para_token_counter}")