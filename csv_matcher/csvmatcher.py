import csv

with open('csv_matcher/file1.csv', 'r') as f1, open('csv_matcher/file2.csv', 'r') as f2, open('csv_matcher/output.csv', 'w', newline='') as out_file:
    reader1 = csv.reader(f1, delimiter=',')
    reader2 = csv.reader(f2, delimiter=',')
    writer = csv.writer(out_file, delimiter=',')

    responses = {}
    for row in reader2:
        request = row[0]
        response = row[1:]
        responses[request] = response
    print(responses)

    # Compare the responses in file1 with the corresponding responses in file2
    for row in reader1:
        request = row[0]
        response = row[1:]
        if request in responses:
            if response == responses[request]:
                row.append('Yes')
            else:
                row.append('No')
        else:
            row.append('No')
        writer.writerow(row)
