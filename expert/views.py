from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Symptom, Conclusion, Rule, DiagnosisResult
from .proses.InferenceEngine import InferenceEngine

def diagnose_view(request):
    symptoms = Symptom.objects.all()
    results = []
    explanations = []

    if request.method == 'POST':
        selected_codes = request.POST.getlist('symptoms')  
        confidence = float(request.POST.get('confidence', 1.0))

        initial_facts_with_weights = {
            code: confidence for code in selected_codes if Symptom.objects.filter(code=code).exists()
        }

        if not initial_facts_with_weights:
            results = [("Pilih setidaknya satu gejala.", None)]
        else:
            engine = InferenceEngine()
            final_facts, explanations = engine.forward_chain(initial_facts_with_weights)

            for fact_code, weight in final_facts.items():
                conclusion = Conclusion.objects.filter(code=fact_code).first()
                symptom = Symptom.objects.filter(code=fact_code).first()

                if conclusion:
                    results.append((conclusion.name, weight))
                elif symptom:
                    results.append((symptom.name, weight))
                else:
                    results.append((fact_code, weight))

            # Simpan ke database
            DiagnosisResult.objects.create(
                user_input=initial_facts_with_weights,
                final_facts=final_facts,
                explanations=explanations
            )

    return render(request, 'diagnose.html', {
        'symptoms': symptoms,
        'results': results,
        'explanations': explanations
    })