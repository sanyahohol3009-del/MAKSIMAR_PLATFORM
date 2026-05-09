# Test Runner Parallel Hardening Acceptance v1

## Статус

Принято.

Цель: обычный full auto parallel должен проходить с active pytest_monitor и xdist.

## Проблема

pytest_monitor при параллельном запуске xdist создавал duplicate TEST_SESSIONS.SESSION_H в SQLite.

Ошибка:

- sqlite3.IntegrityError: UNIQUE constraint failed: TEST_SESSIONS.SESSION_H

Это была ошибка test-runner infrastructure, не ошибка application logic.

## Решение

В conftest.py добавлен локальный test-runtime patch:

- pytest_monitor остаётся включённым;
- xdist остаётся включённым;
- full auto parallel остаётся включённым;
- duplicate TEST_SESSIONS.SESSION_H обрабатывается как идемпотентная повторная регистрация session;
- остальные sqlite ошибки не глушатся.

## Проверки

- hardening smoke: 2 passed
- full auto parallel with monitor active: 1902 passed

## Правило

Не использовать `-p no:monitor` как постоянный обход.

Full auto parallel должен работать в обычном режиме.
