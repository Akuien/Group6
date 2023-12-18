from django.core.management.base import BaseCommand, CommandError
from loanApp.models import LoanApplicant
import csv
import os
import shortuuid  # Don't forget to import shortuuid

class Command(BaseCommand):
    help = "Import loan applicant data from a local CSV file into Django database"

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
                self.create_loan_applicant(row)

    def create_loan_applicant(self, row):
        loan_applicant, created = LoanApplicant.objects.get_or_create(
            LoanID=row['LoanID'],
            defaults={
                'Age': row['Age'],
                'Income': row['Income'],
                'LoanAmount': row['LoanAmount'],
                'CreditScore': row['CreditScore'],
                'MonthsEmployed': row['MonthsEmployed'],
                'LoanTerm': row['LoanTerm'],
                'DTIRatio': row['DTIRatio'],
                'EmploymentType': row['EmploymentType'],
                'Default': row['Default']
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created {loan_applicant}'))
        else:
            self.stdout.write(self.style.WARNING(f'Loan Applicant {loan_applicant} already exists'))

    def finalize(self):
        self.stdout.write(self.style.SUCCESS('Import completed successfully'))
