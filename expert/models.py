from django.db import models

class Symptom(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Conclusion(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Rule(models.Model):
    rule_id = models.CharField(max_length=10, unique=True)
    conditions = models.JSONField()
    conclusion = models.JSONField()
    description = models.TextField()
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.rule_id}: {self.description}"

class DiagnosisResult(models.Model):
    user_input = models.JSONField()
    final_facts = models.JSONField()
    explanations = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnosis {self.id} - {self.created_at}"