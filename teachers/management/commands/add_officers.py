"""Django management command to populate Officers model with initial data."""

from datetime import datetime

from django.core.management.base import BaseCommand
from pandas import options

from teachers.models import Officers


# TODO: Populate with officer records. Each dict should mirror Officers fields.
OFFICER_DATA = [
	# Example:
	{
	    'full_name_en': 'Md. Zahidul Islam',
	    'full_name_uni': 'মোঃ জাহিদুল ইসলাম',
	    'full_name_ansi': '†gvt Rvwn`yj Bmjvg',
	    'full_name_ar': None,
	    'short_name_en': 'ZI',
	    'designation': 'assistant_registrar',
	    'email': 'zahidul.islam@example.com',
	    'phone_number': '0123456789',
	    'office_phone_number': None,
	    'home_phone_number': None,
	    'bank_account_number': None,
	    'tin_number': None,
	    'data_of_birth': '1980-01-01',
	    'address': None,
	    'profile_picture': 'profile_pictures/john_doe.jpg',
	    'joining_date': '2020-01-15',
	},
	{
	    'full_name_en': 'Maksud Hossain Talukdar',
	    'full_name_uni': 'মাকসুদ হোসেন তালুকদার',
	    'full_name_ansi': 'gvKmy` †nv‡mb ZvjyK`vi',
	    'full_name_ar': None,
	    'short_name_en': 'MHT',
	    'designation': 'assistant_registrar',
	    'email': 'maksud.talukdar@example.com',
	    'phone_number': '0123456789',
	    'office_phone_number': None,
	    'home_phone_number': None,
	    'bank_account_number': None,
	    'tin_number': None,
	    'data_of_birth': '1980-01-01',
	    'address': None,
	    'profile_picture': 'profile_pictures/john_doe.jpg',
	    'joining_date': '2021-01-15',
	},
	{
	    'full_name_en': 'Md. Moniruzzaman',
	    'full_name_uni': 'মোঃ মনিরুজ্জামান',
	    'full_name_ansi': '†gvt gwbiæ¾vgvb',
	    'full_name_ar': None,
	    'short_name_en': 'MM',
	    'designation': 'assistant_registrar',
	    'email': 'moniruzzaman@example.com',
	    'phone_number': '0123456789',
	    'office_phone_number': None,
	    'home_phone_number': None,
	    'bank_account_number': None,
	    'tin_number': None,
	    'data_of_birth': '1980-01-01',
	    'address': None,
	    'profile_picture': 'profile_pictures/john_doe.jpg',
	    'joining_date': '2021-06-15',
	},
	{
	    'full_name_en': 'Md. Shakhawat Hossain',
	    'full_name_uni': 'মোঃ শাখাওয়াৎ হোসেন',
	    'full_name_ansi': '†gvt kvLvIqvr †nv‡mb',
	    'full_name_ar': None,
	    'short_name_en': 'SH',
	    'designation': 'assistant_registrar',
	    'email': 'shakhawat@example.com',
	    'phone_number': '0123456789',
	    'office_phone_number': None,
	    'home_phone_number': None,
	    'bank_account_number': None,
	    'tin_number': None,
	    'data_of_birth': '1980-01-01',
	    'address': None,
	    'profile_picture': 'profile_pictures/john_doe.jpg',
	    'joining_date': '2021-12-15',
	},
	{
	    'full_name_en': 'Md. Abdur Rahim',
	    'full_name_uni': 'মোঃ আব্দুর রহিম',
	    'full_name_ansi': '†gvt Avãyi iwng',
	    'full_name_ar': None,
	    'short_name_en': 'AR',
	    'designation': 'assistant_registrar',
	    'email': 'abdur.rahim@example.com',
	    'phone_number': '0123456789',
	    'office_phone_number': None,
	    'home_phone_number': None,
	    'bank_account_number': None,
	    'tin_number': None,
	    'data_of_birth': '1980-01-01',
	    'address': None,
	    'profile_picture': 'profile_pictures/john_doe.jpg',
	    'joining_date': '2023-12-15',
	},
	{
	    'full_name_en': 'Nazma Khatun',
	    'full_name_uni': 'মোছাঃ নাজমা খাতুন',
	    'full_name_ansi': '†gvQvt bvRgv LvZzb',
	    'full_name_ar': None,
	    'short_name_en': 'NK',
	    'designation': 'assistant_registrar',
	    'email': 'nazma.khatun@example.com',
	    'phone_number': '0123456789',
	    'office_phone_number': None,
	    'home_phone_number': None,
	    'bank_account_number': None,
	    'tin_number': None,
	    'data_of_birth': '1980-01-01',
	    'address': None,
	    'profile_picture': 'profile_pictures/john_doe.jpg',
	    'joining_date': '2024-01-15',
	},
	
	{
	    'full_name_en': 'Billal Hossain',
	    'full_name_uni': 'মোঃ বিল্লাল হোসেন',
	    'full_name_ansi': '†gvt wejøvj †nv‡mb',
	    'full_name_ar': None,
	    'short_name_en': 'BH',
	    'designation': 'assistant_registrar',
	    'email': 'billal.hossain@example.com',
	    'phone_number': '0123456789',
	    'office_phone_number': None,
	    'home_phone_number': None,
	    'bank_account_number': None,
	    'tin_number': None,
	    'data_of_birth': '1980-01-01',
	    'address': None,
	    'profile_picture': 'profile_pictures/john_doe.jpg',
	    'joining_date': '2024-12-15',
	},
	
]


def _parse_date(value: str | None):
	if not value:
		return None
	return datetime.strptime(value, "%Y-%m-%d").date()


class Command(BaseCommand):
	"""Django management command to add officers to the database."""
	
   

	help = 'Populate the Officers model with data'

	def add_arguments(self, parser):
		parser.add_argument(
			'--reset',
			action='store_true',
			help='Delete existing officers before loading new data.',
		)

	def handle(self, *args, **options):
		if options.get('reset'):
			Officers.objects.all().delete()
			self.stdout.write(self.style.WARNING('Deleted existing officers'))
			

		if not OFFICER_DATA:
			self.stdout.write(self.style.WARNING('OFFICER_DATA is empty; no officers created.'))
			return

		for data in OFFICER_DATA:
			lookup_email = data.get('email')
			if not lookup_email:
				self.stdout.write(self.style.WARNING('Skipped entry without email (required for lookup).'))
				continue

			officer, created = Officers.objects.update_or_create(
				email=lookup_email,
				defaults={
					'full_name_en': data.get('full_name_en'),
					'full_name_uni': data.get('full_name_uni'),
					'full_name_ansi': data.get('full_name_ansi'),
					'full_name_ar': data.get('full_name_ar'),
					'short_name_en': data.get('short_name_en'),
					'designation': data.get('designation'),
					'phone_number': data.get('phone_number'),
					'office_phone_number': data.get('office_phone_number'),
					'home_phone_number': data.get('home_phone_number'),
					'bank_account_number': data.get('bank_account_number'),
					'tin_number': data.get('tin_number'),
					'data_of_birth': _parse_date(data.get('data_of_birth')),
					'address': data.get('address'),
					'profile_picture': data.get('profile_picture'),
					'joining_date': _parse_date(data.get('joining_date')),
				},
			)

			if created:
				self.stdout.write(
					self.style.SUCCESS(f"Created officer: {officer.full_name_en or officer.full_name_uni}")
				)
			else:
				self.stdout.write(
					self.style.SUCCESS(f"Updated officer: {officer.full_name_en or officer.full_name_uni}")
				)
