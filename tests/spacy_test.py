import json
import os
from spacy.kb import KnowledgeBase
import spacy  # version 3.0.6'
from pathlib import Path
import csv


def load_entities():
    # distributed alongside this notebook
    entities_loc = Path.cwd().parent / "assignment\data\sample-labels-cheat.txt"
    i = 0
    names = dict()
    wikilinks = dict()
    with entities_loc.open("r", encoding="utf8") as csvfile:
        # csvreader = csv.reader(csvfile, delimiter="\t")
        for row in csvfile:
            row = row.split('\t')
            qid = str(i)
            name = row[0]
            wikilink = row[1]
            names[qid] = name
            wikilinks[qid] = wikilink
            i += 1
    return names, wikilinks


name_dict, wikilink_dict = load_entities()
# for QID in name_dict.keys():
#     print(f"{QID}, name={name_dict[QID]}, wikilink={wikilink_dict[QID]}")


# nlp = spacy.load("en_core_web_md")
# kb = KnowledgeBase(vocab=nlp.vocab, entity_vector_length=300)

# for qid, wikilink in wikilink_dict.items():
#     wikilink_doc = nlp(wikilink)
#     wikilink_enc = wikilink_doc.vector
#     kb.add_entity(entity=qid, entity_vector=wikilink_enc, freq=342)

# for qid, name in name_dict.items():
#     kb.add_alias(alias=name, entities=[qid], probabilities=[1])

# print(f"Entities in the KB: {kb.get_entity_strings()}")
# print(f"Aliases in the KB: {kb.get_alias_strings()}")


# output_dir = Path.cwd().parent / "assignment"
# if not os.path.exists(output_dir):
#     os.mkdir(output_dir)
# nlp.to_disk(output_dir / "knowledgebase")

def jsontime(QID, name, wikilink):
    return({
        'QID': QID,
        'label': name,
        'wikilink': wikilink
    })


dataset = []
json_loc = Path.cwd().parent / "assignment\data\sample_annotations.tsv"
with json_loc.open("r", encoding="utf8") as jsonfile:
    for line in jsonfile:
        line = line.split('\t')
        line = jsontime(line[0], line[1], line[2])
        line = json.dumps(line)
        example = json.loads(line)
        print('example', example)
        text = example["label"]
        if example["answer"] == "accept":
            QID = example["accept"][0]
            offset = (example["spans"][0]["start"], example["spans"][0]["end"])
            links_dict = {QID: 1.0}
        dataset.append((text, {"links": {offset: links_dict}}))

print('dataset[0]', dataset[0])
