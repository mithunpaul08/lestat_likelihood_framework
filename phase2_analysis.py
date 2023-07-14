import argparse
from pathlib import Path
from sdf.yaml_schema import Schema
from typing import List
from tqdm import tqdm

MAX_TOKENS_PER_DOCUMENT = 300
MAX_EVENTS_PER_SCHEMA = 10

masc_schema_ir_query_mapping={"q10.invasion.aph":"Invasion",
"q8.hold_a_summit_meeting.ldc":"summit",
"q10.kidnapping.jdlm":"Kidnapping",
"q11.disease_outbreak.jal.post_arg_review":"Disease outbreak",
"q8.cyber_attack_1.jal":"Hacking",
"q10.smuggling.aph":"Smuggling",
"q8.nonviolent_protest_march.ldc":"Peaceful demonstration",
"q10.bomb_threat_response.egl":"Bomb threat response",
"q10.car_bombing.md":"car bombing",
"q10.chemical_spill.hrs":"chemical spill",
"q10.fume_event.egl":"fume event",
"q10.military_coup.md":"military coup",
"q10.nuclear_meltdown.eny":"nuclear meltdown",
"q10.riot.aph":"riot",
"q8.quarantine.ldc":"quarantine",
"q8.spread_disinformation.ldc":"spread disinformation",
"q8.sub.treatment_or_vaccine_development.mrf":"treatment vaccine development",
"q9.develop_a_biological_agent_2.ldc.zh.egl":"develop biological agent"}



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

def get_query_docs_paragraphs_mapping(path):
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
                            if "document number" in line:
                                line = line.split(":")[1] #to get only the text out of sentences like "document number 3: Romanian authorities"
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


def similar(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio()

def clean_string(input):
    output = input.strip()
    output = output.lower()
    return output
def get_entailment_calculations(original_yaml_schemas,query_docs_mapping):
    entailment_counter = 0
    for schema in tqdm(original_yaml_schemas, desc="Checking entailment", total= len(original_yaml_schemas)):
        if schema.id in masc_schema_ir_query_mapping:
            corresponding_ir_query = masc_schema_ir_query_mapping[schema.id]
            if  corresponding_ir_query.lower() in query_docs_mapping:
                docs_for_this_query = query_docs_mapping[corresponding_ir_query.lower()]
                for each_event in schema.steps:
                    for each_docs in docs_for_this_query:
                        for each_paragraphs in each_docs:
                            #todo replace this with : if gpt says entail, add entailment counter
                            each_event_name = clean_string(each_event.id)
                            each_paragraph_clean = clean_string(each_paragraphs)
                            similarity_score = similar(each_event_name, each_paragraph_clean)
                            if similarity_score> 0.5:
                                entailment_counter += 1
    return entailment_counter






# def get_entailment(paragraphs, schemas):

def main() -> None:
    """Main functions for likelihood calculation."""
    args = read_args()
    input_file_retrieved_docs = str(args.input_file_retrieved_docs)
    input_dir_yaml_schemas = args.input_dir_yaml_schemas
    original_yaml_schemas = load_schemas_sdf(input_dir_yaml_schemas)
    query_docs_mapping = get_query_docs_paragraphs_mapping(input_file_retrieved_docs)
    entailment_score = get_entailment_calculations(original_yaml_schemas,query_docs_mapping)
    print(entailment_score)



if __name__ == "__main__":
    main()
