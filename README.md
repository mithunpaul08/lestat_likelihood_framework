to run one query:

on sample data:

`python likelihood_ir.py  --query "cartoons" --data_dir data/sample_input`

`python likelihood_ir.py --query "assassination" --data_dir "/Users/mitch/research/lestat/GIGAWORD/only_2010_data_flattened_one_article_per_document"`

to run multiple queries:


`python likelihood_ir.py --queries "phishing, invasion, summit, kidnapping, cyber bullying, disease outbreak, hacking, assassination, smuggling, evacuation, peaceful demonstration, video game development, disaster recovery, search rescue, bomb threat response, car bombing,chemical spill,fume event, military coup, nuclear meltdown, riot, quarantine, spread disinformation, treatment or vaccine development, develop biological agent" --data_dir "/Users/mitch/research/lestat/GIGAWORD/only_2010_data_flattened_one_article_per_document"`

server:
`python likelihood_ir.py --queries "phishing, invasion, summit, kidnapping, cyber bullying, disease outbreak, hacking, assassination, smuggling, evacuation, peaceful demonstration, video game development, disaster recovery, search rescue, bomb threat response, car bombing,chemical spill,fume event, military coup, nuclear meltdown, riot, quarantine, spread disinformation, treatment or vaccine development, develop biological agent" --data_dir "/nas/home/mithun/GIGAWORD/only_2010_data_flattened_one_article_per_document"


#Data  stuff:

#LDC Corpora used:
DOwnload the following files from the LDC corpus homepage
`https://catalog.ldc.upenn.edu/organization/downloads`

to recursively unzip each of the LDC files in a given dir 
`find . -name "*.zip" | xargs -P 5 -I fileName sh -c 'unzip -o -d "$(dirname "fileName")/$(basename -s .zip "fileName")" "fileName"'`