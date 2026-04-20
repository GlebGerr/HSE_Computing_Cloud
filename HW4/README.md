# HW4 Kubernetes deployment

## Состав манифестов

В проекте используются следующие Kubernetes-манифесты:

- `k8s/secrets.yaml` - application secrets
- `k8s/postgres.yaml` - PostgreSQL StatefulSet + headless Service
- `k8s/redis.yaml` - Redis Deployment + Service
- `k8s/deployment.yaml` - web Deployment
- `k8s/service.yaml` - ClusterIP Service для web-приложения
- `k8s/ingress.yaml` - Ingress для доступа к приложению
- `k8s/job.yaml` - Job для запуска миграций

## Что реализовано

В рамках задания подготовлены:

- `Deployment` для web-приложения
- `Service` типа `ClusterIP`
- `Ingress`
- `Secret` для application secrets
- `docker-registry secret` для доступа к Container Registry
- `Job` для выполнения миграций
- `PostgreSQL` в виде `StatefulSet`
- `Redis` как отдельный сервис

## Порядок применения манифестов

Сначала необходимо создать secret для доступа к Yandex Container Registry:

```bash
kubectl create secret docker-registry regcred \
  --docker-server=cr.yandex \
  --docker-username=oauth \
  --docker-password=<OAUTH_TOKEN>
```

Потом применяются основные манифесты:

```bash
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/job.yaml
```

## Проверка ресурсов

После применения манифестов можно проверить состояние ресурсов следующими командами:

```bash
kubectl get pods
kubectl get svc
kubectl get ingress
kubectl get jobs
kubectl get statefulsets
```

## Назначение компонентов

### Web application

Web-приложение разворачивается через Deployment и использует образ из Container Registry.

### PostgreSQL

База данных разворачивается в виде StatefulSet, чтобы обеспечить стабильное имя и постоянное хранилище.

### Redis

Redis используется как отдельный сервис внутри кластера.

### Job

Job используется для выполнения миграций Django перед началом работы приложения.

### Ingress

Ingress используется для маршрутизации внешнего HTTP-трафика к ClusterIP Service.