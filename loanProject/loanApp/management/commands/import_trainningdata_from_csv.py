from django.core.management.base import BaseCommand, CommandError
from loanApp.models import Applicant
import csv
import os

class Command(BaseCommand):
    help = "Import applicant training data from a local CSV file into Django database"

    def add_arguments(self, parser):
        parser.add_argument("file_path", nargs=1, type=str)

    def handle(self, *args, **options):
        self.options = options
        self.prepare()
        self.main()
        self.finalize()

    def prepare(self):
        file_path = self.options['file_path'][0]
        if not os.path.exists(file_path):
            raise CommandError(f"File {file_path} does not exist")

    def main(self):
        file_path = self.options['file_path'][0]
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.create_applicant(row)

    def create_applicant(self, row):
        applicant, created = Applicant.objects.get_or_create(
            id=row['Id'],
            defaults={
                'income': row['Income'],
                'age': row['Age'],
                'experience': row['Experience'],
                'marital_status': 'single' if row['Married/Single'] == 'single' else 'married',
                'house_ownership': 'rented' if row['House_Ownership'] == 'rented' else 'owned',
                'car_ownership': True if row['Car_Ownership'] == 'yes' else False,
                'profession': row['Profession'],
                'city': row['CITY'],
                'state': row['STATE'],
                'current_job_years': row['CURRENT_JOB_YRS'],
                'current_house_years': row['CURRENT_HOUSE_YRS'],
                'risk_flag': True if row['Risk_Flag'] == '1' else False
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created {applicant}'))
        else:
            self.stdout.write(self.style.WARNING(f'Applicant {applicant} already exists'))

    def finalize(self):
        self.stdout.write(self.style.SUCCESS('Import completed successfully'))
