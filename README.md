# AI Career Assistant

AI-ассистент, который анализирует соответствие резюме кандидата требованиям вакансии и даёт структурированные рекомендации по развитию.

Загружаешь PDF-резюме и текст вакансии — на выходе получаешь JSON с подтверждёнными навыками, пробелами и рекомендациями, что подтянуть.

## Возможности

- 📄 Извлечение текста из PDF-резюме (`pdfplumber`)
- 🤖 Анализ соответствия резюме вакансии через LLM (OpenRouter API)
- ✅ Строго структурированный вывод через Pydantic-схему — никакого произвольного текста
- 🚫 Модель не придумывает навыки, которых нет в резюме — только то, что можно подтвердить
- 🛡️ Обработка ошибок API (таймауты, невалидный JSON, сетевые сбои)
- 📚 RAG поверх базы знаний (ML, статистика, uplift-моделирование) для более точных рекомендаций
- 🌐 Парсинг вакансий напрямую с hh.ru

## Пример вывода

```json
{
  "matching_skills": ["Python", "FastAPI", "PyTorch"],
  "unconfirmed_skills": ["CatBoost", "MLflow"],
  "experience_match": true,
  "recommendations": ["Изучить MLflow для трекинга экспериментов", "Попрактиковаться в CatBoost на пет-проекте"]
}
```

## Стек

- **Python 3.10+**
- **OpenAI SDK** (через OpenRouter — модель `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`)
- **Pydantic** — валидация структурированного вывода
- **pdfplumber** — извлечение текста из PDF
- **python-dotenv** — управление секретами
- **RAG-слой** (`rag/`) — загрузка и препроцессинг базы знаний для контекстных рекомендаций

## Структура проекта

```
AI_career_assistant/
├── data/
│   └── knowledge_base/
│       ├── machine_learning.md    # база знаний по ML
│       ├── statistic.md           # база знаний по статистике
│       └── uplift.md              # база знаний по uplift-моделированию
├── model/
│   ├── __init__.py
│   ├── connection.py               # клиент OpenRouter API
│   ├── extract_from_hh_vacancy.py  # парсинг вакансий с hh.ru
│   ├── main_part_model.py          # основная логика анализа резюме
│   ├── model_schemas.py            # Pydantic-схема ответа
│   └── reading_pdf_files.py        # извлечение текста из PDF
├── rag/
│   ├── documaent_loader.py         # загрузка документов базы знаний
│   └── preprocessing_data.py       # препроцессинг данных для RAG
├── tests/
├── .env                            # OPENROUTER_SECRET_KEY (не коммитить!)
├── .gitignore
└── requirements.txt
```

## Установка

```bash
git clone https://github.com/your-username/AI_career_assistant.git
cd AI_career_assistant
pip install -r requirements.txt
```

Создай файл `.env` в корне проекта:

```
OPENROUTER_SECRET_KEY=your_api_key_here
```

Ключ можно получить на [openrouter.ai](https://openrouter.ai).

## Использование

```python
from model.main_part_model import answer
from model.reading_pdf_files import extract_text_from_pdf

resume_text = extract_text_from_pdf("path/to/resume.pdf")

result = answer(
    vacancy="Python, CatBoost, FastAPI, MLflow, PyTorch",
    user_resume=resume_text
)

print(result)
```

## Roadmap

- [ ] Завершить RAG-слой: embedding базы знаний и поиск релевантного контекста
- [ ] REST API на FastAPI для веб-интерфейса
- [ ] Тесты (`tests/`) для основных модулей
- [ ] Поддержка нескольких форматов резюме (DOCX, TXT)
- [ ] Кэширование повторных запросов
- [ ] Docker-контейнеризация

## Лицензия

MIT
