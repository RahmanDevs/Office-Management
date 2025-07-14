
from django.core.management.base import BaseCommand
from teachers.models import Teacher  # Adjust the import based on your app name
from datetime import datetime

teacher_data = [
    {'full_name_uni': 'ড. আ.ব.ম. সাইফুল ইসলাম সিদ্দিকী', 'full_name_ansi': 'W. Av.e.g. mvBdzj Bmjvg wmwÏKx', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003121380', 'email': 'drsaif.siddiqi@gmail.com', 'phone_number': '01766165604', 'tin_number': '349687589512', 'data_of_birth': '1965-08-10'},
    {'full_name_uni': 'ড. এ.বি.এম. ফারুক', 'full_name_ansi': 'W. G.we.Gg. dviæK', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003127407', 'email': 'abmfaruqiu@gmail.com', 'phone_number': '01718161373', 'tin_number': '01795216837', 'data_of_birth': '1964-03-01'},
    {'full_name_uni': 'ড. আ.ফ.ম. আকবর হোসাইন', 'full_name_ansi': 'W. Av.d.g. AvKei †nvmvBb', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003105264', 'email': 'alquraniukbd@gmail.com', 'phone_number': '01712946096', 'tin_number': '427-109-8087', 'data_of_birth': '1963-01-12'},
    {'full_name_uni': 'ড. হাফেজ আবু নোমান মোঃ এরশাদ উল্লাহ', 'full_name_ansi': 'W. nv‡dR Avey †bvgvb †gvt Gikv` Djøvn', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003112977', 'email': 'ershadullah219@gmail.com', 'phone_number': '01623517084', 'tin_number': '354339897744', 'data_of_birth': '1966-01-01'},
    {'full_name_uni': 'ড. আ.ব.ম. ছিদ্দিকুর রহমান আশ্রাফী', 'full_name_ansi': 'W. Av.e.g. wQwÏKzi ingvb AvkÖvdx', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003122910', 'email': 'asrafiiuk@gmail.com', 'phone_number': '01716288031', 'tin_number': '174328550972', 'data_of_birth': '1968-12-01'},
    {'full_name_uni': 'ড. মোহাঃ লোকমান হোসেন', 'full_name_ansi': 'W. †gvnvt †jvKgvb †nv‡mb', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003127173', 'email': 'drloqmanhusain@gmail.com', 'phone_number': '01718679586', 'tin_number': '411796618151', 'data_of_birth': '1969-03-01'},
    {'full_name_uni': 'ড. এম. এয়াকুব আলী', 'full_name_ansi': 'W. Gg. GqvKze Avjx', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003121133', 'email': 'dryeaqubiuk@gmail.com', 'phone_number': '01711130810', 'tin_number': '416710514046', 'data_of_birth': '1970-03-01'},
    {'full_name_uni': 'ড. মোঃ নাছির উদ্দিন মিঝি', 'full_name_ansi': 'W. †gvt bvwQi DwÏb wgwS', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003112636', 'email': 'mizy1969@gmail.com', 'phone_number': '01711108088', 'tin_number': '4271108660', 'data_of_birth': '1969-05-10'},
    {'full_name_uni': 'ড. মোহাঃ জালাল উদ্দীন', 'full_name_ansi': 'W. †gvnvt Rvjvj DÏxb', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003119258', 'email': 'pdrjalal@gmail.com', 'phone_number': '01712640688', 'tin_number': '340454171930', 'data_of_birth': '1973-12-01'},
    {'full_name_uni': 'ড. মুহাম্মদ গোলাম রব্বানী', 'full_name_ansi': 'W. gynv¤§` †Mvjvg ieŸvbx', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003112018', 'email': 'drgolamr74@gmail.com', 'phone_number': '01716767080', 'tin_number': '689291271050', 'data_of_birth': '1974-03-01'},
    {'full_name_uni': 'ড. খান মুহাম্মদ ইলিয়াস', 'full_name_ansi': 'W. Lvb gynv¤§` Bwjqvm', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003112147', 'email': 'yliasiuk@gmail.com', 'phone_number': '01718553936', 'tin_number': '199957638541', 'data_of_birth': '1977-01-01'},
    {'full_name_uni': 'ড. মোঃ আমিনুল ইসলাম', 'full_name_ansi': 'W. †gvt Avwgbyj Bmjvg', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003119267', 'email': 'aminiuk@gmail.com', 'phone_number': '01718100594', 'tin_number': '4271145621', 'data_of_birth': '1974-03-01'},
    {'full_name_uni': 'ড. শেখ এ.বি.এম. জাকির হোসেন', 'full_name_ansi': 'W. †kL G.we.Gg. RvwKi †nv‡mb', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003119795', 'email': 'zakiriuk73@gmail.com', 'phone_number': '01712640020', 'tin_number': '579799340452', 'data_of_birth': '1973-02-02'},
    {'full_name_uni': 'ড. এ.কে.এম. রাশেদুজ্জামান', 'full_name_ansi': 'W. G.†K.Gg. iv‡k`y¾vgvb', 'designation': 'অধ্যাপক', 'bank_account_number': '0200003127576', 'email': 'rashedzamaniu@gmail.com', 'phone_number': '01715041242', 'tin_number': '380266877674', 'data_of_birth': '1979-01-01'},
]

class Command(BaseCommand):
    help = 'Populate the Teacher model with data'

    def handle(self, *args, **kwargs):
        for data in teacher_data:
            teacher, created = Teacher.objects.get_or_create(
                full_name_uni=data.get('full_name_uni'),
                full_name_ansi=data.get('full_name_ansi'),
                designation='professor',
                email=data.get('email'),
                phone_number=data.get('phone_number'),
                bank_account_number=data.get('bank_account_number'),
                tin_number=data.get('tin_number'),
                data_of_birth=datetime.strptime(data.get('data_of_birth'), '%Y-%m-%d').date()
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created teacher: {teacher.full_name_uni}'))
            else:
                self.stdout.write(self.style.WARNING(f'Teacher already exists: {teacher.full_name_uni}'))
