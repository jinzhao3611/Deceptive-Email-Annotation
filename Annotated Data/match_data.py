import xml.etree.ElementTree as ET
from collections import defaultdict

with open('John_dataset.xml', 'r', encoding='utf-8') as john_file:
    john_tree = ET.parse(john_file)

with open('Annotated_Jiexin_dataset.xml', encoding='utf-8') as jiexin_file:
    jiexin_tree = ET.parse(jiexin_file)

john_root = john_tree.getroot()
jiexin_root = jiexin_tree.getroot()

john_dict = defaultdict(list)
jiexin_dict = defaultdict(list)
agreement_dict = defaultdict(list)
john_all = set()
jiexin_all = set()
overlapping_data = set()
agree_all = set()

for john_child, jiexin_child in zip(john_root.iter(), jiexin_root.iter()):
    john_att = dict(john_child.attrib)
    jiexin_att = dict(jiexin_child.attrib)
    for john_item, jiexin_item in zip(john_att.items(), jiexin_att.items()):
        if john_item[0] == 'text':
            john_dict[john_child.tag].append(john_item[1].rstrip().lstrip())
        if jiexin_item[0] == 'text':
            jiexin_dict[jiexin_child.tag].append(jiexin_item[1].rstrip().lstrip())

print(john_dict)
print(jiexin_dict)

for john_key, jiexin_key in zip(john_dict.keys(), jiexin_dict.keys()):
    john_all.update(john_dict[john_key])
    jiexin_all.update(jiexin_dict[john_key])
    john_set = set(john_dict[john_key])
    jiexin_set = set(jiexin_dict[jiexin_key])
    agree_set = john_set.intersection(jiexin_set)
    agree_all.update(agree_set)
    agreement_dict[john_key] = list(agree_set)

overlapping_data = john_all.intersection(jiexin_all)
# print(overlapping_data)

disagree_file = open('John_Jiexin_disagreement.txt', 'w', encoding='utf-8')
disagree_set = set()

for data in overlapping_data:
    for key in john_dict.keys():
        if data in john_dict[key] and data not in jiexin_dict[key]:
            print('JOHN')
            print(key)
            print(data)
            print('---------')
            if data not in agree_all:
                disagree_set.add(data)
        if data not in john_dict[key] and data in jiexin_dict[key]:
            print('JIEXIN')
            print(key)
            print(data)
            print('---------')
            if data not in agree_all:
                disagree_set.add(data)

# print(agreement_dict)
print(disagree_set)

for data in disagree_set:
    disagree_file.write(data)
    for key in john_dict.keys():
        if data in john_dict[key]:
            disagree_file.write(' : JOHN- ' + key)
        elif data in jiexin_dict[key]:
            disagree_file.write(' : JIEXIN- ' + key)
    disagree_file.write('\n')

with open('John_Jiexin_agreement.txt', 'w', encoding='utf-8') as agree_file:
    for key in agreement_dict.keys():
        for sents in agreement_dict[key]:
            agree_file.write(sents + " : " + key + '\n')
