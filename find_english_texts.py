DOCUMENT_PROFILE_PATH="/Users/mitch/Downloads/LDC2021E06_KAIROS_Schema_Learning_Corpus_Complex_Event_Source_Data_Part_4_V1.0/docs/document_profile.tab"

only_english_filenames=[]
with open(DOCUMENT_PROFILE_PATH) as f:
    lines=f.readlines()
    for line in lines:
        line_split = line.split("\t")
        if line_split[1] and line_split[2]:
            language=line_split[1]
            filename=line_split[2]
            if "english" in language.lower():
                only_english_filenames.append(filename.strip())

print(len(only_english_filenames))
