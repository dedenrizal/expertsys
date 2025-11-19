from django.core.management.base import BaseCommand
from expert.models import Symptom, Conclusion, Rule

class Command(BaseCommand):
    help = 'Isi database dengan data fiktif untuk sistem pakar'

    def handle(self, *args, **options):
        # Hapus data lama (opsional)
        Symptom.objects.all().delete()
        Conclusion.objects.all().delete()
        Rule.objects.all().delete()

        # Tambahkan Symptom
        symptoms_data = [
            {'code': 'daun_menguning', 'name': 'Daun Menguning'},
            {'code': 'bercak_basah', 'name': 'Bercak Basah di Daun'},
            {'code': 'bercak_kering', 'name': 'Bercak Kering di Daun'},
            {'code': 'tanaman_layu', 'name': 'Tanaman Layu'},
            {'code': 'akar_busuk', 'name': 'Akar Busuk'},
            {'code': 'buah_busuk', 'name': 'Buah Busuk'},
            {'code': 'bunga_rontok', 'name': 'Bunga Rontok'},
            {'code': 'daun_keriting', 'name': 'Daun Keriting'},
            {'code': 'cuaca_lembab', 'name': 'Cuaca Lembab'},
            {'code': 'serangan_hama', 'name': 'Serangan Hama'},
        ]

        for s in symptoms_data:
            Symptom.objects.get_or_create(code=s['code'], defaults={'name': s['name']})

        # Tambahkan Conclusion
        conclusions_data = [
            {'code': 'penyakit_bakteri', 'name': 'Penyakit Bakteri'},
            {'code': 'penyakit_virus', 'name': 'Penyakit Virus'},
            {'code': 'penyakit_fusarium', 'name': 'Penyakit Fusarium'},
            {'code': 'pengobatan_antibiotik', 'name': 'Pengobatan Antibiotik'},
            {'code': 'pengobatan_fungisida', 'name': 'Pengobatan Fungisida'},
            {'code': 'pengobatan_insektisida', 'name': 'Pengobatan Insektisida'},
            {'code': 'gejala_umum', 'name': 'Gejala Umum'},
            {'code': 'tanaman_sehat', 'name': 'Tanaman Sehat'},
            {'code': 'tanaman_sakit', 'name': 'Tanaman Sakit'},
            {'code': 'butuh_pemupukan', 'name': 'Butuh Pemupukan'},
        ]

        for c in conclusions_data:
            Conclusion.objects.get_or_create(code=c['code'], defaults={'name': c['name']})

        # Tambahkan Rule
        rules_data = [
            {
                "id": "R1",
                "conditions": {
                    "type": "AND",
                    "items": [
                        {"fact": "daun_menguning", "weight": 0.8},
                        {"fact": "bercak_basah", "weight": 0.9}
                    ]
                },
                "conclusion": {"fact": "penyakit_bakteri", "weight": 0.85},
                "description": "Gejala daun menguning dan bercak basah menunjukkan bakteri.",
                "priority": 10
            },
            {
                "id": "R2",
                "conditions": {
                    "type": "OR",
                    "items": [
                        {"fact": "daun_menguning", "weight": 0.8},
                        {"fact": "bercak_kering", "weight": 0.7}
                    ]
                },
                "conclusion": {"fact": "gejala_umum", "weight": 0.6},
                "description": "Gejala umum ditemukan.",
                "priority": 5
            },
            {
                "id": "R3",
                "conditions": {
                    "type": "AND",
                    "items": [
                        {"fact": "tanaman_layu", "weight": 0.9},
                        {"fact": "akar_busuk", "weight": 0.95}
                    ]
                },
                "conclusion": {"fact": "penyakit_fusarium", "weight": 0.9},
                "description": "Tanaman layu dan akar busuk disebabkan oleh jamur Fusarium.",
                "priority": 15
            },
            {
                "id": "R4",
                "conditions": {
                    "type": "AND",
                    "items": [
                        {"fact": "penyakit_bakteri", "weight": 0.85},
                        {"fact": "cuaca_lembab", "weight": 0.7}
                    ]
                },
                "conclusion": {"fact": "pengobatan_antibiotik", "weight": 0.9},
                "description": "Jika bakteri dan cuaca lembab, gunakan antibiotik.",
                "priority": 12
            },
            {
                "id": "R5",
                "conditions": {
                    "type": "NOT",
                    "items": [
                        {"fact": "tanaman_sehat", "weight": 1.0}
                    ]
                },
                "conclusion": {"fact": "tanaman_sakit", "weight": 0.5},
                "description": "Jika bukan tanaman sehat, maka tanaman sakit.",
                "priority": 3
            },
            {
                "id": "R6",
                "conditions": {
                    "type": "AND",
                    "items": [
                        {"fact": "buah_busuk", "weight": 0.9},
                        {"fact": "serangan_hama", "weight": 0.85}
                    ]
                },
                "conclusion": {"fact": "pengobatan_insektisida", "weight": 0.88},
                "description": "Buah busuk dan hama menunjukkan perlunya insektisida.",
                "priority": 11
            },
            {
                "id": "R7",
                "conditions": {
                    "type": "AND",
                    "items": [
                        {"fact": "daun_keriting", "weight": 0.85},
                        {"fact": "serangan_hama", "weight": 0.8}
                    ]
                },
                "conclusion": {"fact": "penyakit_virus", "weight": 0.82},
                "description": "Daun keriting dan hama menunjukkan virus.",
                "priority": 13
            },
            {
                "id": "R8",
                "conditions": {
                    "type": "AND",
                    "items": [
                        {"fact": "bunga_rontok", "weight": 0.7},
                        {"fact": "cuaca_lembab", "weight": 0.6}
                    ]
                },
                "conclusion": {"fact": "butuh_pemupukan", "weight": 0.65},
                "description": "Bunga rontok dan cuaca lembab menunjukkan kebutuhan pemupukan.",
                "priority": 6
            },
        ]

        for r in rules_data:
            Rule.objects.get_or_create(
                rule_id=r["id"],
                defaults={
                    'conditions': r['conditions'],
                    'conclusion': r['conclusion'],
                    'description': r['description'],
                    'priority': r['priority']
                }
            )

        self.stdout.write(
            self.style.SUCCESS('Berhasil mengisi database dengan data fiktif!')
        )