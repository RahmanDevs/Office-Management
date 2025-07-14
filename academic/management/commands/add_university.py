from django.core.management.base import BaseCommand
from teachers.models import University

class Command(BaseCommand):
    help = 'Populate the University model with initial data'

    def handle(self, *args, **kwargs):
        universities = [
            {
                "name_en": "University of Dhaka",
                "name_ansi": "XvKv wek¦we`¨vjq",
                "name_uni": "ঢাকা বিশ্ববিদ্যালয়",
                "short_name_en": "DU",
                "short_name_ansi": "Xvwe",
                "short_name_uni": "ঢাবি",
                "location_en": "Dhaka",
                "location_ansi": "XvKv",
                "location_uni": "ঢাকা",
                "website": "https://www.du.ac.bd"
            },
            {
                "name_en": "Jahangirnagar University",
                "name_ansi": "Rvnv½xibMi wek¦we`¨vjq",
                "name_uni": "জাহাঙ্গীরনগর বিশ্ববিদ্যালয়",
                "short_name_en": "JU",
                "short_name_ansi": "Rvwe",
                "short_name_uni": "জাবি",
                "location_en": "Savar, Dhaka",
                "location_ansi": "mvfvi, XvKv",
                "location_uni": "সাভার, ঢাকা",
                "website": "https://www.juniv.edu"
            },
            {
                "name_en": "Jagannath University",
                "name_ansi": "RMbœv_ wek¦we`¨vjq",
                "name_uni": "জগন্নাথ বিশ্ববিদ্যালয়",
                "short_name_en": "JnU",
                "short_name_ansi": "Rwe",
                "short_name_uni": "জবি",
                "location_en": "Dhaka",
                "location_ansi": "XvKv",
                "location_uni": "ঢাকা",
                "website": "https://www.jnu.ac.bd"
            },
            {
                "name_en": "University of Rajshahi",
                "name_ansi": "ivRkvnx wek¦we`¨vjq",
                "name_uni": "রাজশাহী বিশ্ববিদ্যালয়",
                "short_name_en": "RU",
                "short_name_ansi": "ivwe",
                "short_name_uni": "রাবি",
                "location_en": "Rajshahi",
                "location_ansi": "ivRkvnx",
                "location_uni": "রাজশাহী",
                "website": "https://www.ru.ac.bd"
            },
            {
                "name_en": "Islamic University, Bangladesh",
                "name_ansi": "Bmjvgx wek¦we`¨vjq",
                "name_uni": "ইসলামী বিশ্ববিদ্যালয়",
                "short_name_en": "IU",
                "short_name_ansi": "Bwe",
                "short_name_uni": "ইবি",
                "location_en": "Kushtia",
                "location_ansi": "Kzwóqv",
                "location_uni": "কুষ্টিয়া",
                "website": "https://www.iu.ac.bd"
            },
            {
                "name_en": "University of Chittagong",
                "name_ansi": "PÆMÖvg wek¦we`¨vjq",
                "name_uni": "চট্টগ্রাম বিশ্ববিদ্যালয়",
                "short_name_en": "CU",
                "short_name_ansi": "Pwe",
                "short_name_uni": "চবি",
                "location_en": "Chittagong",
                "location_ansi": "PÆMÖvg",
                "location_uni": "চট্টগ্রাম",
                "website": "https://www.cu.ac.bd"
            },
        ]

        created_count = 0
        for uni in universities:
            obj, created = University.objects.get_or_create(name_en=uni["name_en"], defaults=uni)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added: {obj.name_en}"))
                created_count += 1
            else:
                self.stdout.write(f"Skipped (already exists): {obj.name_en}")
        
        self.stdout.write(self.style.SUCCESS(f"Total universities added: {created_count}"))




#   python manage.py populate_universities
