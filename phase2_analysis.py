import argparse
from pathlib import Path
from sdf.yaml_schema import Schema
from typing import List


MAX_TOKENS_PER_DOCUMENT = 300
MAX_EVENTS_PER_SCHEMA = 10



events_per_schema = [22,9,5,6,31,10,12,9,10,9,21,11,13,18,12,20,11,21,15,38,6,12,15,12]


events_per_schema_only_10 = [x if x<MAX_EVENTS_PER_SCHEMA else MAX_EVENTS_PER_SCHEMA for x in events_per_schema ]
#events_per_schema_only_10 = [5]*len (events_per_schema)

events_per_schema = events_per_schema_only_10


average_tokens_per_event = 10

def get_retrieved_doc_details(path):
        full_docs = get_all_retrieved_docs_as_strings(RETRIEVED_IR_FILE_PATH)
        docs = " ".join(full_docs).split("#####################")
        docs_lengths = [len(x.split(" ")) for x in docs ]
        from statistics import mean
        average_doc_length = mean(docs_lengths)
        #remove docs of length greater than MAX_TOKENS_PER_DOCUMENT
        doc_reduced = [x for x in docs if len(x.split(" "))< MAX_TOKENS_PER_DOCUMENT and len(x.split(" "))> 1]
        docs= doc_reduced
        if len(docs) > len(set(docs)):
            docs= list(set(docs))

        doc_token_counter = 0
        total_output_token_count_docs = 0
        for doc in docs:
            for event_count in events_per_schema:
                    prompt = "does the passage" + doc+ "entail, contradict or is neutral to the sentence" \
                             + " Answer should be one of entail, contradict or neutral. Don't retype the whole passage again."
                    doc_token_counter += event_count * len(prompt.split(" "))+average_tokens_per_event
                    output = "the passage" + doc+ "is neutral to the sentence"
                    total_output_token_count_docs +=  event_count * len(output.split(" "))+average_tokens_per_event
        # print(f"number of tokens in all documents= {doc_token_counter}")
        # print(f"number of  tokens in the response of gpt across all documents= {total_output_token_count_docs}")


        paragraphs = " ".join(docs).split("~~~~~~~~~~")
        para_token_counter = 0
        total_output_count_para = 0

        for para in paragraphs:
            for event in events_per_schema:
                prompt = "return the answer in one word does the passage" + para + "entail, contradict or is neutral to the sentence"
                para_token_counter += event_count* len(prompt.split(" "))+average_tokens_per_event
                total_output_count_para += 1




        print(f"number of tokens in all paragraphs= {para_token_counter}")
        print(f"number of tokens in response of gpt in all paragraphs= {total_output_count_para}")
        print(f"total cost= {(0.03*para_token_counter/1000) + (0.06*total_output_count_para/1000)+50}")

        return paragraphs, docs


def get_all_retrieved_docs_as_strings(path):
    with open(path) as f:
        lines = f.readlines()
        full_docs = []
        for line in lines:
            line = line.strip()
            if "*****" not in line:
                if "query =" not in line:  # to remove the boiler plate and delimiters added to earmark paragraphs
                    if line and not line == "":
                        if ":" in line:
                            line = line.split(":")[1]
                        full_docs.append(line)
    return full_docs

def get_all_retrieved_docs_as_is(path):
    with open(path) as f:
        lines = f.readlines()
        query_docs_paragraphs={}
        found_query_break = False
        found_start_of_docs= False
        docs_this_query = []
        paragraphs_this_query = []
        query_string= ""

        for line in lines:
            line = line.strip()
            if line and not line == "":
                if "*****" in line: #now we know the new query is starting and the first line will be query ="phishing"
                    found_query_break = True
                    if query_string !="" and docs_this_query:
                        query_docs_paragraphs[query_string] = docs_this_query
                        docs_this_query =[]
                    continue
                if found_query_break:
                    query_string = line.split("=")[1].strip()
                    found_query_break = False
                    found_start_of_docs = True
                    continue
                if found_start_of_docs:
                    if "##############" in line: #### means its end of a document
                        docs_this_query.append(paragraphs_this_query)
                        paragraphs_this_query = []
                    else:
                        if "~~~" not in line:
                            paragraphs_this_query.append(line)
    return query_docs_paragraphs


def load_schemas_sdf(input_dir: Path) -> List[Schema]:
    """Read yaml files of Schemas.

    Args:
        input_dir: Path to load YAML schemas from

    Returns:
        Schemas
    """
    if not input_dir.is_dir():
        raise NotADirectoryError(
            f"Schema directory {input_dir} does not exist or is not a directory."
        )
    schema_paths = sorted(input_dir.glob("*.yaml"))
    schemas = [
        Schema.load(schema_path) for schema_path in tqdm(schema_paths, desc="Loading schemas")
    ]
    return schemas

def read_args() -> argparse.Namespace:
    """Read arguments from command line.

    Args:

    Returns:
        An instance of argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input_file_retrieved_docs", required=True, type=Path, help="Path to a single doc which contains all retrieved docs")
    parser.add_argument("--input_dir_yaml_schemas", required=True, type=Path, help="Input schema YAML files")
    return parser.parse_args()

def get_query_doc_string_mapping(query_docs_string, docs):
    queries = docs.split("**************************************************************************************************************")
    for query in queries:
        if query and query !="":
            query_split = query.split("query =")
            query_string = query_split[0]
            query_docs= query_split[0]
            query_docs_string[query_string] = query_docs
    return query_docs_string



def get_query_docs_mapping(input_file_retrieved_docs):
    query_doc_string = {} #store each query and its documents (as one single string) in a hashtable
    all_docs_lines = get_all_retrieved_docs_as_is(input_file_retrieved_docs)
    query_doc_string  = get_query_doc_string_mapping(query_doc_string, " ".join(all_docs_lines))

# def get_entailment(paragraphs, schemas):

def main() -> None:
    """Main functions for likelihood calculation."""
    args = read_args()
    input_file_retrieved_docs = str(args.input_file_retrieved_docs)
    input_dir_yaml_schemas = str(args.input_dir_yaml_schemas)
    # original_yaml_schemas = load_schemas_sdf(input_dir)
    paragraphs, docs = get_query_docs_mapping(input_file_retrieved_docs)


if __name__ == "__main__":
    main()
