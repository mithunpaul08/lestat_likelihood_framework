to run one query:

`python likelihood_ir.py --query "disease outbreak" --data_dir "/Users/mitch/research/lestat/LDC/LDC2020E24_KAIROS_Schema_Learning_Corpus_Phase_1_Complex_Event_Source_Data_Part_1/data/ltf/K0C03N.ltf/ltf_text"`

to run multiple queries:

`python likelihood_ir.py --queries "phishing, invasion, summit, kidnapping, cyber bullying, disease outbreak, hacking, assasination, smuggling, evacuation, peaceful demonstration, video game development, develop treatment, disaster recovery, search rescue, bomb threat response, car bombing,chemical spill,coup,fume event, military coup, nuclear meltdown, riot, quarantine, spread disinformation, treatment or vaccine development, develop biological agent" --data_dir "/Users/mitch/research/lestat/LDC/only_english_files_txt_format"`


for server:

`python likelihood_ir.py --query "travel documents" --data_dir "/nas/home/mithun/ldc_only_txt"`

            python likelihood_ir.py --queries "phishing, invasion, summit, kidnapping, cyber bullying, disease outbreak, hacking, assasination, smuggling, evacuation, peaceful demonstration, video game development, develop treatment, disaster recovery, search rescue, bomb threat response, car bombing,chemical spill,coup,fume event, military coup, nuclear meltdown, riot, quarantine, spread disinformation, treatment or vaccine development, develop biological agent" --data_dir "/nas/home/mithun/ldc_only_txt"


#Data  stuff:

#LDC Corpora used:
DOwnload the following files from the LDC corpus homepage
`https://catalog.ldc.upenn.edu/organization/downloads`

to recursively unzip each of the LDC files in a given dir 
`find . -name "*.zip" | xargs -P 5 -I fileName sh -c 'unzip -o -d "$(dirname "fileName")/$(basename -s .zip "fileName")" "fileName"'`