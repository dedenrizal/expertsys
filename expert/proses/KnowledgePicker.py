from django.db.models import Q
from ..models import *

class KnowledgePicker:
    def __init__(self):
        self.rules = Rule.objects.all()
        self.symptoms = Symptom.objects.all()
        self.conclusions = Conclusion.objects.all()

    def get_symptom_by_code(self, code):
        return self.symptoms.filter(code=code).first()

    def get_conclusion_by_code(self, code):
        return self.conclusions.filter(code=code).first()

    def get_all_rules(self):
        return self.rules