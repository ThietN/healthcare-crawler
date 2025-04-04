import json
import re
from bs4 import BeautifulSoup

def main() -> None:
    regex = re.compile('Symptoms')
    with open("../mayoclinic/output.json", 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    for entry in data:
        html = BeautifulSoup(entry['content'], features='lxml')

        symp_elem = html.find(['h2','h3'], string=regex)
        if symp_elem is None:
            continue

        symptoms = ''
        elem = symp_elem
        while True:
            elem = elem.next_sibling
            if elem is None or 'When to see a doctor' in elem.text or 'Request an appointment' in elem.text:
                break
            symptoms += f'{elem.text}\n'
        # content migt not have h2 and h3 with text symptom
        if not symptoms:
            section = symp_elem.find_parent('section')
            if section:
                symptoms = section.text
# return those url not have any symptom 
        if not symptoms:
            raise ValueError(entry['url'])

        entry.pop('content')
        entry['symptoms'] = symptoms.strip()

    with open('output-symps.json', 'w') as fp:
        json.dump(data, fp, indent=1)


if __name__ == '__main__':
    raise SystemExit(main())

