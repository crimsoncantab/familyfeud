import argparse
import collections
import csv
import sys
import os
import xml.etree.ElementTree as XML


def get_argparser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), default=sys.stdin,
                        help='csv file from google docs survey')
    parser.add_argument('-o', '--output', type=argparse.FileType('wb', 0), default=os.fdopen(sys.stdout.fileno(), 'wb'),
                        help='xml file formatted for family feud')
    return parser.parse_args()


def extract_responses(response_file):
    counters = collections.defaultdict(collections.Counter)
    responses = csv.DictReader(response_file)
    for response in responses:
        for k, v in response.items():
            v = v.strip()
            if v:
                counters[k][v.casefold()] += 1
    return counters


def build_answer(parent, answer, freq):
    a = XML.SubElement(parent, 'answer')
    a.set('text', answer)
    a.set('points', str(freq))


def build_question(parent, question, answers):
    q = XML.SubElement(parent, 'question')
    q.set('text', question)
    for answer, freq in answers.most_common():
        build_answer(q, answer, freq)


def build_xml(response_data):
    root = XML.Element('questions')
    for question, answers in sorted(response_data.items()):
        build_question(root, question, answers)
    tree = XML.ElementTree(root)
    return tree


if __name__ == '__main__':
    p = get_argparser()
    responses = extract_responses(p.file)
    xml = build_xml(responses)
    xml.write(p.output)
