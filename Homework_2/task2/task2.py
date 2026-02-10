# Задание 2. Есть класс, предоставляющий доступ к набору чисел. Источником этого набора чисел
# является некоторый файл. С определенной периодичностью данные в файле меняются
# (надо реализовать механизм обновления). Приложение должно получать доступ к этим данным и
# выполнять набор операций над ними (сумма, максимум, минимум и т.д.). При каждой попытке доступа
# к этому набору необходимо вносить запись в лог-файл. При реализации используйте паттерн Proxy
# (для логгирования) и другие необходимые паттерны.

print("Задание №2 — Паттерн Proxy (доступ к числам)")
print("-" * 50)

from abc import ABC, abstractmethod
from typing import List
import os
import time
from datetime import datetime
from pathlib import Path
from threading import Lock


# ======================================================
# Интерфейс источника данных
# ======================================================
class NumbersSource(ABC):
    @abstractmethod
    def get_numbers(self) -> List[int]:
        pass

    @abstractmethod
    def reload(self) -> None:
        pass


# ======================================================
# Реальный источник данных (чтение из файла)
# ======================================================
class FileNumbersSource(NumbersSource):
    def __init__(self, filename: str):
        self.filename = filename
        self._numbers: List[int] = []
        self._last_modified = 0.0
        self.reload()

    def reload(self) -> None:
        if not os.path.exists(self.filename):
            self._numbers = []
            return

        self._last_modified = os.path.getmtime(self.filename)
        self._numbers.clear()

        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.isdigit() or (line.startswith("-") and line[1:].isdigit()):
                    self._numbers.append(int(line))

    def _check_updates(self):
        if os.path.exists(self.filename):
            current_time = os.path.getmtime(self.filename)
            if current_time > self._last_modified:
                print("📂 Обнаружены изменения файла, обновляем данные...")
                self.reload()

    def get_numbers(self) -> List[int]:
        self._check_updates()
        return self._numbers.copy()


# ======================================================
# Singleton Logger
# ======================================================
class AccessLogger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.log_file = "numbers_access.log"
                Path(cls._instance.log_file).touch(exist_ok=True)
            return cls._instance

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"[{timestamp}] {message}"
        print(record)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(record + "\n")


# ======================================================
# Proxy для логирования
# ======================================================
class LoggingNumbersProxy(NumbersSource):
    def __init__(self, real_source: NumbersSource):
        self._real_source = real_source
        self._logger = AccessLogger()

    def get_numbers(self) -> List[int]:
        self._logger.log("Запрос доступа к набору чисел")
        numbers = self._real_source.get_numbers()
        self._logger.log(f"Получено чисел: {len(numbers)}")
        return numbers

    def reload(self) -> None:
        self._logger.log("Принудительное обновление данных")
        self._real_source.reload()


# ======================================================
# Facade — операции над числами
# ======================================================
class NumbersService:
    def __init__(self, source: NumbersSource):
        self.source = source

    def total(self) -> int:
        return sum(self.source.get_numbers())

    def maximum(self) -> int:
        nums = self.source.get_numbers()
        return max(nums) if nums else 0

    def minimum(self) -> int:
        nums = self.source.get_numbers()
        return min(nums) if nums else 0

    def average(self) -> float:
        nums = self.source.get_numbers()
        return sum(nums) / len(nums) if nums else 0.0

    def count(self) -> int:
        return len(self.source.get_numbers())


# ======================================================
# Демонстрация работы
# ======================================================
def create_test_file(filename: str, values: List[int]):
    with open(filename, "w", encoding="utf-8") as f:
        for v in values:
            f.write(f"{v}\n")
    print(f"✅ Файл {filename} создан / обновлён")


def demo():
    filename = "numbers_data.txt"

    create_test_file(filename, [3, 7, 15, 20, 42])

    real_source = FileNumbersSource(filename)
    proxy_source = LoggingNumbersProxy(real_source)
    service = NumbersService(proxy_source)

    print("\n📊 Первый доступ:")
    print("Сумма:", service.total())
    print("Максимум:", service.maximum())
    print("Минимум:", service.minimum())
    print("Среднее:", service.average())
    print("Количество:", service.count())

    print("\n⏳ Ждём обновление файла...")
    time.sleep(2)

    create_test_file(filename, [5, 10, 25, 50])

    print("\n📊 Второй доступ (после обновления):")
    print("Сумма:", service.total())
    print("Максимум:", service.maximum())
    print("Минимум:", service.minimum())
    print("Среднее:", service.average())
    print("Количество:", service.count())

    print(f"\n📝 Лог записан в файл: {AccessLogger().log_file}")


if __name__ == "__main__":
    demo()
