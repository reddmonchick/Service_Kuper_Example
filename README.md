# 🧠 Parser API Microservice

> **MicroService**, который принимает команды через FastAPI, парсит данные из Android-приложения Kuper (и других магазинов), и отправляет результаты в Django API.

## 🎯 Описание

Этот сервис реализует гибкую систему парсинга данных из мобильных приложений с поддержкой:
- Множества магазинов (Kuper, Ozon и другие)
- Различных команд (`all_update`, `update_list_id`, `search_request`)
- Чистой архитектуры и расширяемости
- Автоматического выбора парсера на основе запроса

Сервис построен с применением современных практик проектирования и программирования, что делает его **легким для тестирования, поддержки и масштабирования**.

---


## 🧠 TL;DR: Какие концепции мы используем

| Концепция | Используется в проекте |
|----------|------------------------|
| **Clean Architecture** | ✅ Да |
| **Domain-Driven Design (DDD)** | ✅ Частично |
| **Dependency Injection (DI)** | ✅ Через `Dishka` |
| **Inversion of Control (IoC)** | ✅ Контейнер управляет зависимостями |
| **SOLID** | ✅ Все 5 принципов соблюдены |
| **Use Case / Application Service** | ✅ В `parsing_service.py` |
| **Strategy Pattern** | ✅ Выбор команды (`all_update`, `update_list_id`, `search_request`) |
| **Provider / Factory / Singleton** | ✅ В DI через `AppProvider` |
| **Single Responsibility Principle** | ✅ Каждый файл делает одну задачу |
| **Open/Closed Principle** | ✅ Можно добавлять новые парсеры без изменения кода |
| **Interface Segregation** | ✅ `ParserService` содержит только нужные методы |
| **Dependency Inversion** | ✅ Application зависит от абстракций, а не от реализаций |

---

---

## 🚀 Возможности

- **Расширяемость:** легко добавлять новые парсеры и команды
- **Тестируемость:** полная подмена зависимостей через DI
- **Чистая архитектура:** разделение слоёв (API, Application, Domain, Infrastructure)
- **Поддержка нескольких магазинов:** сейчас поддерживаются `Kuper` и `Ozon`, легко добавить новые

---


## 🔧 Установка и запуск

### 1. Установка зависимостей:

```bash
poetry install
```


### 2. Запуск сервиса:
```bash
poetry run uvicorn src.parser_api.main:app --reload
```

### 3. Открыть документацию: 

http://localhost:8000/docs  

