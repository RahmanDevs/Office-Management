from django.core.management.base import BaseCommand
from teachers.models import University
"""
University Fields are

name_en
name_ansi
name_uni
short_name_en
short_name_ansi
short_name_uni
location_en
location_ansi
location_uni
website
"""

# Example Data

universities = [
            {
                "name_en": "University of Dhaka",
                "name_ansi": "ঢাকা বিশ্ববিদ্যালয়",
                "name_uni": "ঢাকা বিশ্ববিদ্যালয়",
                "short_name_en": "DU",
                "short_name_ansi": "DU",
                "short_name_uni": "ডিইউ",
                "location_en": "Dhaka",
                "location_ansi": "Dhaka",
                "location_uni": "ঢাকা",
                "website": "https://www.du.ac.bd"
            },
            {
                "name_en": "Bangladesh University of Engineering and Technology",
                "name_ansi": "বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয়",
                "name_uni": "বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয়",
                "short_name_en": "BUET",
                "short_name_ansi": "BUET",
                "short_name_uni": "বুয়েট",
                "location_en": "Dhaka",
                "location_ansi": "Dhaka",
                "location_uni": "ঢাকা",
                "website": "https://www.buet.ac.bd"
            },
            {
                "name_en": "University of Rajshahi",
                "name_ansi": "রাজশাহী বিশ্ববিদ্যালয়",
                "name_uni": "রাজশাহী বিশ্ববিদ্যালয়",
                "short_name_en": "RU",
                "short_name_ansi": "RU",
                "short_name_uni": "আরইউ",
                "location_en": "Rajshahi",
                "location_ansi": "Rajshahi",
                "location_uni": "রাজশাহী",
                "website": "https://www.ru.ac.bd"
            },
            {
                "name_en": "Jahangirnagar University",
                "name_ansi": "জাহাঙ্গীরনগর বিশ্ববিদ্যালয়",
                "name_uni": "জাহাঙ্গীরনগর বিশ্ববিদ্যালয়",
                "short_name_en": "JU",
                "short_name_ansi": "JU",
                "short_name_uni": "জেইউ",
                "location_en": "Savar, Dhaka",
                "location_ansi": "Savar, Dhaka",
                "location_uni": "সাভার, ঢাকা",
                "website": "https://www.juniv.edu"
            },
            {
                "name_en": "Chittagong University of Engineering and Technology",
                "name_ansi": "চট্টগ্রাম প্রকৌশল ও প্রযুক্তি বিশ্ববিদ্যালয়",
                "name_uni": "চট্টগ্রাম প্রকৌশল ও প্রযুক্তি বিশ্ববিদ্যালয়",
                "short_name_en": "CUET",
                "short_name_ansi": "CUET",
                "short_name_uni": "চুয়েট",
                "location_en": "Chittagong",
                "location_ansi": "Chittagong",
                "location_uni": "চট্টগ্রাম",
                "website": "https://www.cuet.ac.bd"
            },
            {
                "name_en": "Islamic University",
                "name_ansi": "ইসলামী বিশ্ববিদ্যালয়",
                "name_uni": "ইসলামী বিশ্ববিদ্যালয়",
                "short_name_en": "IU",
                "short_name_ansi": "IU",
                "short_name_uni": "ইবি",
                "location_en": "Kushtia",
                "location_ansi": "Kushtia",
                "location_uni": "কুষ্টিয়া",
                "website": "https://www.iu.ac.bd"
            },
            {
                "name_en": "University of Chittagong",
                "name_ansi": "চট্টগ্রাম বিশ্ববিদ্যালয়",
                "name_uni": "চট্টগ্রাম বিশ্ববিদ্যালয়",
                "short_name_en": "CU",
                "short_name_ansi": "CU",
                "short_name_uni": "চবি",
                "location_en": "Chittagong",
                "location_ansi": "Chittagong",
                "location_uni": "চট্টগ্রাম",
                "website": "https://www.cu.ac.bd"
            },
            {
                "name_en": "Islamic Arabic University",
                "name_ansi": "ইসলামি আরবি বিশ্ববিদ্যালয়",
                "name_uni": "ইসলামি আরবি বিশ্ববিদ্যালয়",
                "short_name_en": "IAU",
                "short_name_ansi": "IAU",
                "short_name_uni": "আইএইউ",
                "location_en": "Dhaka",
                "location_ansi": "Dhaka",
                "location_uni": "ঢাকা",
                "website": "https://www.iau.edu.bd"
            }
        ]
class Command(BaseCommand):
    help = 'Populates the database with major Bangladesh universities.'

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
        confirm=input("Do you want to delete all universities? (yes/no): ")
        if confirm.lower()!='yes':
            self.stdout.write(self.style.ERROR('University not deleted'))
            return
        # print all universities with name_en and total count
        self.stdout.write(self.style.SUCCESS(f'Total universities: {University.objects.count()}'))
        if University.objects.count()==0:
            self.stdout.write(self.style.ERROR('No universities found'))
            return    
        for university in University.objects.all():
            self.stdout.write(self.style.SUCCESS(university.name_en))
        # delete all universities
        University.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all universities'))

    def add_one(self):
        name_en=input("Enter university name in English: ")
        name_ansi=input("Enter university name in Arabic: ")
        name_uni=input("Enter university name in Urdu: ")
        short_name_en=input("Enter short name in English: ")
        short_name_ansi=input("Enter short name in Arabic: ")
        short_name_uni=input("Enter short name in Urdu: ")
        location_en=input("Enter location in English: ")
        location_ansi=input("Enter location in Arabic: ")
        location_uni=input("Enter location in Urdu: ")
        website=input("Enter website: ")
        #confirm input data
        self.stdout.write(self.style.SUCCESS(f'Name in English: {name_en}'))
        self.stdout.write(self.style.SUCCESS(f'Name in Arabic: {name_ansi}'))
        self.stdout.write(self.style.SUCCESS(f'Name in Urdu: {name_uni}'))
        self.stdout.write(self.style.SUCCESS(f'Short name in English: {short_name_en}'))
        self.stdout.write(self.style.SUCCESS(f'Short name in Arabic: {short_name_ansi}'))
        self.stdout.write(self.style.SUCCESS(f'Short name in Urdu: {short_name_uni}'))
        self.stdout.write(self.style.SUCCESS(f'Location in English: {location_en}'))
        self.stdout.write(self.style.SUCCESS(f'Location in Arabic: {location_ansi}'))
        self.stdout.write(self.style.SUCCESS(f'Location in Urdu: {location_uni}'))
        self.stdout.write(self.style.SUCCESS(f'Website: {website}'))
        confirm=input("Do you want to save this university? (yes/no): ")
        if confirm.lower()!='yes':
            self.stdout.write(self.style.ERROR('University not added'))
            return
        university, created = University.objects.get_or_create(
            name_en=name_en,
            name_ansi=name_ansi,
            name_uni=name_uni,
            short_name_en=short_name_en,
            short_name_ansi=short_name_ansi,
            short_name_uni=short_name_uni,
            location_en=location_en,
            location_ansi=location_ansi,
            location_uni=location_uni,
            website=website
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully added: {university.name_en}'))
        else:
            self.stdout.write(self.style.WARNING(f'Already exists: {university.name_en}'))

    def add_all(self):
        for data in universities:
            university, created = University.objects.get_or_create(
                name_en=data["name_en"],
                name_ansi=data["name_ansi"],
                name_uni=data["name_uni"],
                short_name_en=data["short_name_en"],
                short_name_ansi=data["short_name_ansi"],
                short_name_uni=data["short_name_uni"],
                location_en=data["location_en"],
                location_ansi=data["location_ansi"],
                location_uni=data["location_uni"],
                website=data["website"]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added: {university.name_en}'))
            else:
                self.stdout.write(self.style.WARNING(f'Already exists: {university.name_en}'))
