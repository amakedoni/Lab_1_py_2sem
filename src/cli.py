import json
import sys
from pathlib import Path
from typing import Iterator
from .models import Task
from .sources import FileTaskSource, GeneratorTaskSource, ApiStubTaskSource, validate_source
from .loader import TaskLoader


def _print_tasks(tasks: list[Task]) -> None:
    if not tasks:
        print("  [пусто — задач не найдено]")
        return
    for task in tasks:
        print(f"  [{task.id}] {task.payload}")


def _source_from_file() -> FileTaskSource:
    path_str = input("  Путь к JSON-файлу: ").strip()
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    return FileTaskSource(path)


def _source_from_generator() -> GeneratorTaskSource:
    raw = input("  Введи JSON-массив задач (например [{'id':1,'payload':'test'}]): ").strip()
    data: list[dict] = json.loads(raw)

    def gen() -> Iterator[dict]:
        yield from data

    return GeneratorTaskSource(gen())


def _source_from_api() -> ApiStubTaskSource:
    raw = input("  Введи JSON-массив задач для API-заглушки: ").strip()
    data: list[dict] = json.loads(raw)
    return ApiStubTaskSource(data)


SOURCES = {
    "1": ("📄 Из файла (JSON)", _source_from_file),
    "2": ("⚙️  Генератор (ввод JSON)", _source_from_generator),
    "3": ("🌐 API-заглушка (ввод JSON)", _source_from_api),
}


def interactive_loop() -> None:
    print("\n╔══════════════════════════════════╗")
    print("║   Task Processing Platform CLI   ║")
    print("╚══════════════════════════════════╝")

    while True:
        print("\n┌─ МЕНЮ ───────────────────────────")
        for key, (label, _) in SOURCES.items():
            print(f"│  {key}. {label}")
        print("│  q. Выход")
        print("└──────────────────────────────────")

        choice = input("Выбери источник: ").strip().lower()

        if choice == "q":
            print("Пока! 👋")
            break

        if choice not in SOURCES:
            print("❌ Неверный выбор, попробуй снова.")
            continue

        label, factory = SOURCES[choice]
        print(f"\n▶ Выбрано: {label}")

        try:
            source = factory()
            validate_source(source)  # runtime-проверка контракта
            loader = TaskLoader(source)
            tasks = loader.load_all()
            print(f"\n✅ Загружено задач: {len(tasks)}")
            _print_tasks(tasks)
        except TypeError as e:
            print(f"❌ Ошибка контракта: {e}")
        except FileNotFoundError as e:
            print(f"❌ {e}")
        except json.JSONDecodeError:
            print("❌ Невалидный JSON, попробуй снова.")
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")
