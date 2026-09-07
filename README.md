# 🧠 Drunost Project

> **Open-source AI model router for Python with a native GUI.**

Drunost — это экспериментальный Python-фреймворк для **маршрутизации запросов между различными ИИ-моделями и API-провайдерами** через единый интерфейс.

Проект объединяет:

* 🤖 AI Model Routing
* 🖥️ GUI на Python
* 🔌 поддержку нескольких API
* ⚡ автоматический выбор модели
* 🧩 расширяемую архитектуру
* 📊 статистику запросов
* 🛠️ полностью открытый исходный код

Drunost создан с простой идеей:

> **Не выбирай модель вручную — пусть это делает роутер.**

---

## ✨ Возможности

### 🤖 Intelligent Model Routing

Drunost может анализировать входящий запрос и выбирать подходящую модель.

Например:

```text
"Напиши REST API на FastAPI"
        ↓
   Code Router
        ↓
   Coding Model
```

А для обычного вопроса:

```text
"Объясни теорию относительности"
        ↓
   General Router
        ↓
   General Purpose Model
```

---

### 🔀 Multi-Provider

Drunost не привязан к одному AI-провайдеру.

Архитектура позволяет подключать различные источники моделей:

```text
OpenAI
Anthropic
Google
OpenRouter
Local Models
Custom APIs
        ↓
     Drunost
        ↓
      Router
```

Каждый провайдер представляет собой отдельный backend.

---

## 🖥️ GUI

Drunost поставляется с графическим интерфейсом для управления моделями, маршрутами и настройками.

Интерфейс позволяет:

* добавлять API providers;
* создавать routing rules;
* выбирать модели;
* просматривать историю запросов;
* смотреть latency;
* включать fallback;
* тестировать модели;
* изменять параметры генерации.

Пример:

```text
┌──────────────────────────────────────────────┐
│ DRUNOST PROJECT                         v1.0 │
├──────────────────────────────────────────────┤
│                                              │
│  Provider          Model                     │
│  ┌─────────────┐   ┌─────────────────────┐  │
│  │ OpenRouter  │   │ auto                ▼│  │
│  └─────────────┘   └─────────────────────┘  │
│                                              │
│  Routing Strategy                            │
│  ┌────────────────────────────────────────┐  │
│  │ Intelligent                            │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  [ Send Request ]                            │
│                                              │
├──────────────────────────────────────────────┤
│ Status: ● Connected                          │
│ Latency: 842ms                               │
└──────────────────────────────────────────────┘
```

GUI реализован полностью на Python и не требует отдельного frontend-сервера.

---

# 🧩 Архитектура

Drunost разделён на несколько независимых компонентов.

```text
                 ┌───────────────┐
                 │      GUI      │
                 └───────┬───────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Drunost Core  │
                └────────┬────────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
          Router      Providers   Storage
              │          │
              ▼          ▼
          Strategy     API Layer
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
          Model A      Model B      Model C
```

Основная логика маршрутизации не зависит от GUI.

Это позволяет использовать Drunost как библиотеку:

```python
from drunost import Router

router = Router()

response = router.generate(
    "Write a Python HTTP server"
)

print(response)
```

---

# 🚦 Routing Strategies

Drunost поддерживает несколько стратегий маршрутизации.

### `manual`

Использовать указанную пользователем модель.

```python
router.strategy = "manual"
```

### `fastest`

Выбирать модель с минимальной измеренной задержкой.

```python
router.strategy = "fastest"
```

### `cheap`

Приоритизировать минимальную стоимость запроса.

```python
router.strategy = "cheap"
```

### `quality`

Выбирать наиболее качественную доступную модель.

```python
router.strategy = "quality"
```

### `intelligent`

Автоматически определять тип запроса.

```python
router.strategy = "intelligent"
```

---

# 🧠 Intelligent Router

Intelligent Router классифицирует запрос перед отправкой.

Условный pipeline:

```text
User Prompt
    │
    ▼
Prompt Analyzer
    │
    ├── Coding
    ├── Reasoning
    ├── Creative
    ├── Translation
    ├── General
    └── Long Context
          │
          ▼
     Model Selector
          │
          ▼
       Provider
```

Например:

```python
router.generate(
    "Find the bug in this C++ memory allocator"
)
```

может привести к:

```text
Category: coding
Complexity: high
Context: medium
Selected model: coding-high
```

---

# 🔁 Fallback System

Если выбранная модель недоступна, Drunost может автоматически переключиться на другую.

```text
Primary Model
     │
     ├── ❌ Error
     │
     ▼
Fallback #1
     │
     ├── ❌ Error
     │
     ▼
Fallback #2
     │
     ▼
Response
```

Пример конфигурации:

```yaml
fallback:
  enabled: true

  models:
    - provider/model-a
    - provider/model-b
    - provider/model-c
```

---

# 📊 Request Statistics

Drunost собирает локальную статистику запросов:

```text
Requests        1,284
Successful      1,247
Failed             37

Average latency  1.42s
Fastest          312ms
Slowest          8.91s

Fallback rate     4.2%
```

Статистика хранится локально и не отправляется на сторонние серверы самим Drunost.

---

# 📁 Project Structure

```text
drunost/
│
├── drunost/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── router.py
│   │   ├── engine.py
│   │   ├── strategy.py
│   │   └── fallback.py
│   │
│   ├── providers/
│   │   ├── base.py
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── openrouter.py
│   │   └── local.py
│   │
│   ├── gui/
│   │   ├── app.py
│   │   ├── windows.py
│   │   ├── settings.py
│   │   └── widgets.py
│   │
│   ├── storage/
│   │   ├── database.py
│   │   └── config.py
│   │
│   └── utils/
│       ├── logger.py
│       └── metrics.py
│
├── tests/
│
├── examples/
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# 📦 Installation

Требуется:

* Python 3.10+
* pip
* доступ к API выбранного провайдера

Установка:

```bash
git clone https://github.com/example/drunost.git
cd drunost

python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

---

# 🚀 Запуск

GUI:

```bash
python -m drunost.gui
```

CLI:

```bash
python -m drunost
```

Или:

```bash
drunost
```

---

# 🔐 API Keys

API-ключи рекомендуется хранить в переменных окружения.

```bash
DRUNOST_OPENAI_KEY=...
DRUNOST_ANTHROPIC_KEY=...
DRUNOST_OPENROUTER_KEY=...
```

Drunost не требует передавать API-ключ непосредственно в код:

```python
# ❌ Не рекомендуется

router = Router(
    api_key="sk-..."
)
```

Используйте конфигурацию окружения:

```python
router = Router()
```

---

# 🛠️ Configuration

Пример `config.yaml`:

```yaml
router:
  strategy: intelligent

  fallback: true

  timeout: 30

providers:

  - name: primary
    type: openai
    model: default

  - name: secondary
    type: openrouter
    model: auto

logging:
  enabled: true
  level: info

gui:
  theme: dark
  animations: true
```

---

# 🔌 Custom Providers

Можно создавать собственные провайдеры.

```python
from drunost.providers import BaseProvider


class MyProvider(BaseProvider):

    def generate(self, prompt, **kwargs):
        return {
            "text": "Hello from MyProvider"
        }
```

После регистрации:

```python
router.register_provider(
    "my_provider",
    MyProvider()
)
```

---

# 🧪 Development

Клонируйте репозиторий:

```bash
git clone https://github.com/example/drunost.git
cd drunost
```

Установите dev-зависимости:

```bash
pip install -r requirements-dev.txt
```

Запустите тесты:

```bash
pytest
```

Проверка типов:

```bash
mypy drunost/
```

Форматирование:

```bash
ruff format .
```

---

# 🗺️ Roadmap

### v0.1

* [x] Core Router
* [x] Basic GUI
* [x] Provider API
* [x] Configuration system

### v0.2

* [ ] Intelligent routing
* [ ] Advanced fallback
* [ ] Request analytics
* [ ] Plugin system

### v0.3

* [ ] Local model support
* [ ] Custom routing models
* [ ] Streaming
* [ ] Multi-user profiles

### v1.0

* [ ] Stable API
* [ ] Full plugin ecosystem
* [ ] Production-ready routing engine
* [ ] Documentation
* [ ] Performance optimizations

---

# 🤝 Contributing

Pull requests приветствуются.

Перед созданием PR:

1. Создайте fork.
2. Создайте отдельную ветку.
3. Добавьте изменения.
4. Запустите тесты.
5. Создайте Pull Request.

Пожалуйста, не добавляйте API-ключи, приватные конфигурации или другие секреты в репозиторий.

---

# 📜 License

Drunost Project распространяется под лицензией **MIT**.

Вы можете:

* использовать проект;
* изменять его;
* распространять;
* использовать в коммерческих проектах.

При этом сохраняется оригинальное уведомление об авторских правах.

---

# 🧠 Philosophy

Drunost не пытается создать «ещё одну AI-модель».

Он пытается решить другую проблему:

> **Моделей становится слишком много.**

Сегодня существует одна модель для reasoning, другая для кода, третья для скорости, четвёртая для огромного контекста.

Drunost объединяет их в единый routing layer.

```text
              MANY MODELS
                   │
          ┌────────▼────────┐
          │     DRUNOST     │
          │                 │
          │  ROUTE          │
          │  FALLBACK       │
          │  ANALYZE        │
          │  MONITOR        │
          └────────┬────────┘
                   │
                   ▼
              ONE INTERFACE
```

**One API.
Many models.
Automatic routing.**

---

## ⭐ Star the project

Если Drunost оказался полезен — поставьте ⭐ репозиторию.

Это помогает проекту развиваться.

**Drunost Project — open source AI routing for Python.**
