import csv
import sys

csv.field_size_limit(sys.maxsize)
from django.core.management.base import BaseCommand, CommandError
from Quiz.models import Question, Choice


class Command(BaseCommand):
    help = "Takes an input file and loads all the questions and choices."

    def add_arguments(self, parser):
        parser.add_argument("--filename", "-f", nargs="?", type=str)

    def handle(self, *args, **options):
        filename = options["filename"]
        if not filename:
            raise CommandError('Command must be provided with a filename!')

        with open(f"./{filename}", mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if '\x' in row[0]:
                    continue
                if line_count == 0:
                    line_count += 1
                question, choices_raw = row[2], row[3]
                choices = [i.replace("'", "") for i in choices_raw.strip('[]').split("' '")]
                q = Question.objects.create(question_text=question.strip())
                for choice in [c.strip() for c in choices]:
                    Choice.objects.create(question=q, choice_text=choice)
                line_count += 1
            print(f'Processed {line_count} lines.')
        print('Successfully added all questions and choices!')