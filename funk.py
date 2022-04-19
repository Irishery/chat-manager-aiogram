import csv


def see_rew(number_file_read):
    with open(f"data/reviews{number_file_read}.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        dtk = []
        for row in file_reader:
            dtk.append([row[0], row[1]])
        return dtk


def see_rew_dict(number_file_write):
    with open(f"data/reviews{number_file_write}.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        dtk = {}
        for row in file_reader:
            dtk[row[0]] = row[1]
        return dtk


def add_post(file_id, caption, number_file_write):
    rev = see_rew_dict(number_file_write)
    if file_id not in rev:
        with open(f'data/reviews{number_file_write}.csv', 'a') as csvFile:
            row = [file_id, caption]
            writer = csv.writer(csvFile)
            writer.writerow(row)
            csvFile.close()


def write_new_post(file_id, caption, number_file_write):
    with open(f'data/reviews{number_file_write}.csv', 'w') as csvFile:
        row = [file_id, caption]
        writer = csv.writer(csvFile)
        writer.writerow(row)
        csvFile.close()


def sort_reviews(all_reviews):
    tail = len(all_reviews) % 3
    full_pag = len(all_reviews) // 3
    reviews = []
    if tail == 0:
        for i in range(0, full_pag * 3, 3):
            reviews.append(all_reviews[i:i + 3])
    else:
        for i in range(0, (full_pag + 1) * 3, 3):
            reviews.append(all_reviews[i:i + 3])
    return reviews


def number_button(number):
    if number == 0:
        numbers = number + 1, number + 2, number + 3
    else:
        numbers = (number * 3) + 1, (number * 3) + 2, (number * 3) + 3
    return numbers
