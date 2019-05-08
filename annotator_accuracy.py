import csv
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter


gold_standard = dict()
with open('../gold_standard/gold_standard_final.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        data = line.rsplit(':', 1)

        gold_standard[data[0].strip()] = data[1].strip()

    # motivation = sum(x.strip() == 'MOTIVATION' for x in gold_standard.values())
    # other = sum(x.strip() == 'OTHER' for x in gold_standard.values())
    # benefits = sum(x.strip() == 'BENEFITS' for x in gold_standard.values())
    # rapport = sum(x.strip() == 'RAPPORT' for x in gold_standard.values())
    # self_intro = sum(x.strip() == 'SELF-INTRO' for x in gold_standard.values())
    # purpose = sum(x.strip() == 'PURPOSE' for x in gold_standard.values())
    #
    # print(motivation,other,benefits,rapport,self_intro,purpose)



def accuracy(annotator):
    # get data
    tree = ET.parse('../deception_data_annotated/final batch/{}_dataset.txt.xml'.format(annotator))
    root = tree.getroot()
    data = defaultdict(str)
    # traverse <tags>
    for child in root[1]:
        data[child.attrib.get('text').strip()] = child.tag
    # {'First and foremost I wish to introduce myself properly to you.' : 'SELF-INTRO', ....}

    correct_count = 0
    for sent, tag in gold_standard.items():
        if data[sent] == tag:
            correct_count += 1
    return correct_count/200


# print(accuracy('John'))
# print(accuracy('Jiexin'))
# print(accuracy('Sarah'))

