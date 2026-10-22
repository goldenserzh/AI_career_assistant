from model.connection import connection
from openai import APIError, APIConnectionError
from model_schemas import VacancyAnalysis
from pydantic import ValidationError
from reading_pdf_files import extract_text_from_pdf

MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

SYSTEM_PROMPT = """
Ты — HR-специалист, который анализирует соответствие резюме кандидата требованиям вакансии.

Используй только информацию из предоставленных вакансии и резюме.
Не придумывай навыки, опыт работы и требования, которых нет в исходных данных.

Твоя задача:
1. Определить требования вакансии, которым кандидат соответствует.
2. Выделить требования, соответствие которым нельзя подтвердить по резюме.
3. Оценить, соответствует ли опыт кандидата требованиям вакансии.
4. Предложить рекомендации по устранению выявленных пробелов.

Правила:
- matching_skills — список требований и навыков из вакансии, которые подтверждены резюме.
- unconfirmed_skills — список требований из вакансии, наличие которых нельзя подтвердить по резюме. Не утверждай, что кандидат не владеет навыком, только потому что он не указан в резюме.
- experience_match — булево значение: true, если кандидат соответствует требованиям вакансии по опыту работы и обязательным навыкам, которые можно проверить по резюме; иначе false.
- recommendations — список конкретных тем или навыков для изучения, связанных с неподтверждёнными требованиями. Не добавляй технологии, которые не нужны для вакансии.

Верни только валидный JSON со следующими полями:
{
    "matching_skills": [],
    "unconfirmed_skills": [],
    "experience_match": false,
    "recommendations": []
}

Не добавляй Markdown, комментарии или пояснения за пределами JSON.
"""





def answer(vacancy: str, user_resume: str):
    user_prompt = f"""
       Проанализируй соответствие кандидата вакансии.

       ВАКАНСИЯ:
       {vacancy}

       РЕЗЮМЕ КАНДИДАТА:
       {user_resume}

       Выполни следующие задачи:
       1. Перечисли требования, которым кандидат соответствует.
       2. Укажи навыки и требования, которым он не соответствует
          или соответствие которым нельзя подтвердить.
       3. Оцени соответствие опыта кандидата вакансии.
       4. Предложи, какие навыки стоит подтянуть. Опыт работы не является навыком

       Не делай выводов о навыках кандидата, которые не подтверждаются предоставленными данными.
       """
    try:
        client = connection()
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )

        if not response.choices:
            raise ValueError("Модель не дала ответ")

        answer = response.choices[0].message.content

        if not answer:
            raise ValueError("Модель вернула пустой ответ")
        try:
            analysis = VacancyAnalysis.model_validate_json(answer)
        except ValidationError as ve:
            print(f"Формат данных не соответствует схеме: {ve}")

        return analysis

    except APIError as e:
        return f"Ошибка в API: {e}"

    except APIConnectionError as api_err:
        return f"Не удалось подключиться к API: {api_err}"

    except ValueError as ve:
        return f"Ошибка в данных: {ve}"




if __name__ == "__main__":
    result = answer(
        vacancy="Python, catboost, fastapi, mlflow, pytorch",
        user_resume= extract_text_from_pdf("C:/Users/serge/OneDrive/Desktop/AI_career_assistant/tests/резюме_Голдаев.pdf")
    )
    print(result)