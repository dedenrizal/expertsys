import openai
openai.api_key = ''

def exstract_symptom_with_gpt(text):
    promp = f"""Ekstrak gejala-gejala dari teks berikut dan kembalikan dalam bentuk list kode gejala yang sesuai dengan sistem pakar berikut:
    Kode gejala: daun_menguning, bercak_basah, demam, pusing, batuk, sakit_kepala, apalah yang penting gejala! jangan sertakan yang lain sat!
    Teks: "{text}"    
    Jawaban (hanya dalam bentuk list kode gejala, tanpa penjelasan):"""
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages =[
            {'role': 'user', 'content':promp}
        ],
        max_token = 50,
        temperature=0
    )
    result = response.choices[0].message['content'].strip()
    return [item.strip() for item in result.split(",") if item.strip()]