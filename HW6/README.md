# HW6 Serverless pipeline

## Что реализовано

В рамках задания реализован serverless pipeline в Yandex Cloud:

- функция `create_task`
- API Gateway для HTTP-вызова `create_task`
- bucket `hw6-uploads-geraskin` для входных файлов
- bucket `hw6-results-geraskin` для результатов
- функция `inference`
- trigger Object Storage на создание объекта в uploads bucket
- сохранение результата обработки в `results` bucket

## Архитектура

1. Клиент отправляет POST-запрос в API Gateway на `/create_task`.
2. API Gateway вызывает функцию `create_task`.
3. Функция `create_task` генерирует `task_id` и pre-signed URL для загрузки файла в `hw6-uploads-geraskin`.
4. Клиент загружает файл по pre-signed URL.
5. Создание объекта в `hw6-uploads-geraskin` вызывает trigger.
6. Trigger запускает функцию `inference`.
7. Функция `inference` читает входной файл, считает:
   - количество строк
   - количество слов
   - количество символов
8. Результат сохраняется в `hw6-results-geraskin` в виде JSON.

## Структура проекта

- `create_task/index.py` — функция генерации `task_id` и pre-signed upload URL
- `create_task/requirements.txt` — зависимости функции `create_task`
- `inference/index.py` — функция обработки загруженного файла
- `inference/requirements.txt` — зависимости функции `inference`
- `api-gateway.yaml` — конфигурация API Gateway

## Используемые ресурсы

- API Gateway
- Cloud Functions
- Object Storage
- Object Storage Trigger
- Service Account

## Как проверить

### 1. Вызов create_task через API Gateway

```powershell
$response = Invoke-WebRequest -Uri "https://d5dp0pp5uiikfr3sv3ru.iwzqm34r.apigw.yandexcloud.net/create_task" -Method Post
$data = $response.Content | ConvertFrom-Json
$data
```

###  2. Загрузка файла по pre-signed URL

```powershell
Set-Content -Path .\final_test.txt -Value "final hw6 pipeline test"
Invoke-WebRequest -Uri $data.upload_url -Method Put -InFile ".\final_test.txt"
```

### 3. Проверка результата

После загрузки файла в bucket `hw6-uploads-geraskin` автоматически вызывается функция `inference`, а результат появляется в bucket `hw6-results-geraskin` в виде JSON-файла:

```json
{
  "task_id": "<task_id>",
  "source_object": "tasks/<task_id>.txt",
  "lines": 1,
  "words": 4,
  "chars": 23
}
```

## API Gateway

URL:

https://d5dp0pp5uiikfr3sv3ru.iwzqm34r.apigw.yandexcloud.net

Endpoint:

POST /create_task

## Примечание по безопасности

Секретные данные (`access_key`, `secret_key`) не хранятся в репозитории и задаются через переменные окружения в Cloud Functions.