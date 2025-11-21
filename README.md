# gost-backup-vault

## English

**gost-backup-vault** is a wrapper around popular backup tools (restic, borg, tar) designed to manage encrypted backups using Russian GOST block ciphers (Magma, Kuznyechik). It provides a unified CLI for managing backup policies and a Prometheus exporter for monitoring.

**Key Features:**
- Unified CLI for restic, borg, and tar.
- Additional encryption layer using GOST standards.
- Policy management and validation.
- Prometheus metrics for backup status and health.

---

## Русский

**gost-backup-vault** — это инструмент для организации зашифрованных бэкапов с использованием ГОСТ-криптографии. Он представляет собой обёртку над restic, borg и tar, предоставляя единый интерфейс управления и мониторинга.

### Основные возможности
- **Единый CLI**: Управление бэкапами через restic, borg или tar с помощью одного инструмента.
- **ГОСТ-шифрование**: Дополнительный слой шифрования с использованием алгоритмов "Магма" и "Кузнечик".
- **Мониторинг**: Встроенный Prometheus-экспортер для отслеживания статуса бэкапов.
- **Политики**: Генератор и валидатор политик резервного копирования.

### Для кого
- Компании, работающие с КИИ, гос-контрактами и в финсекторе.
- Интеграторы и DevOps-специалисты, которым нужны понятные «ГОСТ-совместимые» бэкапы.

### Как использовать (минимальный пример)

```bash
pip install gost-backup-vault

# Запуск проверки конфига и dry-run
gost-backup check --config examples/configs/small_office_linux.yaml --dry-run

# Запуск бэкапа
gost-backup backup --config examples/configs/small_office_linux.yaml --job etc-and-home

# Запуск экспортёра метрик
gost-backup metrics-server --config examples/configs/small_office_linux.yaml --listen 0.0.0.0:9105
```

## Профессиональные услуги – run-as-daemon.ru

Проект развивается инженером DevOps/DevSecOps с сайта [run-as-daemon.ru](https://run-as-daemon.ru).

Если вам нужно:
- внедрить бэкап с использованием ГОСТ-криптографии;
- настроить мониторинг бэкапов и регулярные проверки восстановления;
- адаптировать решение под требования КИИ/гос-контрактов,

вы можете заказать консалтинг, внедрение и поддержку.

> [!IMPORTANT]
> **Важно (Юридическая часть)**
> * Проект не является сертифицированным СКЗИ.
> * Использование ГОСТ-алгоритмов через этот инструмент не гарантирует соответствие требованиям регуляторов.
> * Решения о соответствии, сертификации и выборе конкретных СКЗИ принимаются вместе с юристами и специалистами по ИБ.
