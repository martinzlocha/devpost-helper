import csv
import re
import sys

POSSIBLE_REGEXES = ['What it does(?:[^\n])*(?:[^\w])*(.*)', '^(.*)', '^(?:.*)[^\w]+(.*)']


def extract_line(line):
    title = line['Submission Title']
    table_number = line['Table Number']
    description = ''

    for regex in POSSIBLE_REGEXES:
        match = re.search(regex, line['Plain Description'])

        if match and len(match.group(1)) > 15:
            description = match.group(1)
            break
    return [title, table_number, description]


def save_export(file_name, rows):
    with open(file_name, 'w+', newline='', encoding="utf8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError('Requires source file as a parameter.')

    categories = {}
    gavel_export = []
    previous_title = None

    with open(sys.argv[1], 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)
        for line in reader:
            row = extract_line(line)

            if line['Opt-in prize'] not in categories:
                categories[line['Opt-in prize']] = []

            categories[line['Opt-in prize']].append(row)

            if previous_title != row[0]:
                gavel_export.append(row)

            previous_title = row[0]

    for category in categories:
        save_export('{}.csv'.format(category), categories[category])

    save_export('gavel.csv', gavel_export)
