import csv
import datetime as db
import logging

from prettytable import PrettyTable

from constants import (CSV_OUTPUT,
                       DATETIME_FORMAT,
                       PRETTY_OUTPUT,
                       RESULTS_DIR_NAME,
                       BASE_DIR)


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    pretty_table = PrettyTable()
    pretty_table.field_names = results[0]
    pretty_table.align = 'l'
    pretty_table.add_rows(results[1:])
    print(pretty_table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / RESULTS_DIR_NAME
    results_dir.mkdir(exist_ok=True)

    parse_mode = cli_args.mode
    now = db.datetime.now()
    new_now = now.strftime(DATETIME_FORMAT)
    file_name = f'{parse_mode}_{new_now}.csv'
    file_path = results_dir / file_name

    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect='unix', delimiter=' ', quotechar='|')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


OUTPUT_ACTIONS = {
        PRETTY_OUTPUT: pretty_output,
        CSV_OUTPUT: file_output,
        None: default_output
    }


def control_output(results, cli_args):
    OUTPUT_ACTIONS[cli_args.output](results, cli_args)
