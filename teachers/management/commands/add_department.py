from django.core.management.base import BaseCommand
from teachers.models import Department,University

# Example Data

Departments = [
    {
        "name_en": "Department of Al-Quran & Islamic Studies",
        "name_ansi": "Avj-KzivAvb GÐ BmjvwgK ÷vwWm wefvM",
        "name_uni": "আল-কুরাআন এণ্ড ইসলামিক স্টাডিস বিভাগ",
        "university": "Islamic University"
    },
    
]

class Command(BaseCommand):
    help = 'Populates the database with major Departments of Bangladeshi universities.'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action to perform')

    def handle(self, *args, **options):
        action=options['action']
        if action=='add_one':
            self.add_one()
        elif action=='add_all':
            self.add_all()
        elif action=='delete_all':
            self.delete_all()
        else:
            self.stdout.write(self.style.ERROR('Invalid action'))
    def delete_all(self):
        confirm=input("Do you want to delete all departments? (yes/no): ")
        if confirm.lower()!='yes':
            self.stdout.write(self.style.ERROR('Department not deleted'))
            return

        Department.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All departments deleted'))
    def add_one(self):
        confirm=input("Do you want to add a department? (yes/no): ")
        if confirm.lower()!='yes':
            self.stdout.write(self.style.ERROR('Department not added'))
            return
    def add_all(self):
        confirm=input("Do you want to add all departments? (yes/no): ")
        if confirm.lower()!='yes':
            self.stdout.write(self.style.ERROR('Department not added'))
            return
        for department in Departments:
            get_university=University.objects.get(name_en=department['university'])
            department['university']=get_university
            Department.objects.create(**department)
            self.stdout.write(self.style.SUCCESS(f'{department["name_en"]} added'))
        self.stdout.write(self.style.SUCCESS('All departments added'))