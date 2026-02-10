# Задание 1. Реализация паттерна Builder для пиццы

print("Задание №1\n---------------------------------")
from typing import List


class Pizza:
    """Продукт - пицца"""

    def __init__(self):
        self.size: str = ""
        self.crust: str = ""
        self.sauce: str = ""
        self.toppings: List[str] = []
        self.extra_cheese: bool = False

    def __str__(self) -> str:
        return (f"Pizza:\n"
                f"  Size: {self.size}\n"
                f"  Crust: {self.crust}\n"
                f"  Sauce: {self.sauce}\n"
                f"  Toppings: {', '.join(self.toppings) if self.toppings else 'None'}\n"
                f"  Extra Cheese: {'Yes' if self.extra_cheese else 'No'}")


class PizzaBuilder:
    """Строитель пиццы"""

    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size: str) -> 'PizzaBuilder':
        self.pizza.size = size
        return self

    def set_crust(self, crust: str) -> 'PizzaBuilder':
        self.pizza.crust = crust
        return self

    def set_sauce(self, sauce: str) -> 'PizzaBuilder':
        self.pizza.sauce = sauce
        return self

    def add_topping(self, topping: str) -> 'PizzaBuilder':
        self.pizza.toppings.append(topping)
        return self

    def add_extra_cheese(self) -> 'PizzaBuilder':
        self.pizza.extra_cheese = True
        return self

    def build(self) -> Pizza:
        if not self.pizza.size or not self.pizza.crust or not self.pizza.sauce:
            raise ValueError("Size, crust, and sauce are required")
        pizza = self.pizza
        self.pizza = Pizza()  # reset builder
        return pizza


class MargheritaBuilder(PizzaBuilder):
    """Строитель для Маргариты"""

    def build(self) -> Pizza:
        self.set_size("Medium")
        self.set_crust("Thin")
        self.set_sauce("Tomato")
        self.add_topping("Mozzarella")
        return super().build()


class PepperoniBuilder(PizzaBuilder):
    """Строитель для Пепперони"""

    def build(self) -> Pizza:
        self.set_size("Large")
        self.set_crust("Thick")
        self.set_sauce("Tomato")
        self.add_topping("Mozzarella")
        self.add_topping("Pepperoni")
        self.add_extra_cheese()
        return super().build()


class PizzaDirector:
    """Директор стандартных пицц"""

    @staticmethod
    def build_margherita() -> Pizza:
        return MargheritaBuilder().build()

    @staticmethod
    def build_pepperoni() -> Pizza:
        return PepperoniBuilder().build()

    @staticmethod
    def build_custom() -> Pizza:
        return PizzaBuilder().set_size("Medium").set_crust("Regular").set_sauce("Tomato").build()


def test_builder_pattern():
    print("=== Тестирование паттерна Builder для пиццы ===\n")

    print("1. Базовое использование PizzaBuilder:")
    pizza1 = (PizzaBuilder()
              .set_size("Large")
              .set_crust("Thin")
              .set_sauce("Pesto")
              .add_topping("Mushrooms")
              .add_topping("Olives")
              .add_extra_cheese()
              .build())
    print(pizza1)
    print()

    print("2. Использование стандартных строителей:")
    print("Маргарита:")
    print(PizzaDirector.build_margherita())
    print()
    print("Пепперони:")
    print(PizzaDirector.build_pepperoni())
    print()

    print("3. Кастомная пицца через директора:")
    print(PizzaDirector.build_custom())
    print()


if __name__ == "__main__":
    test_builder_pattern()

# Задание 2. Приложение приготовления пасты с интерактивом
print("Задание №2\n---------------------------------")
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum


class PastaType(Enum):
    CARBONARA = "Карбонара Deluxe"
    BOLOGNESE = "Болоньезе Special"
    ALFREDO = "Альфредо Supreme"
    MARINARA = "Маринара Gourmet"


class Pasta(ABC):
    def __init__(self):
        self._type: str = ""
        self._sauce: str = ""
        self._filling: str = ""
        self._additives: List[str] = []
        self._pasta_type: str = "спагетти"

    @abstractmethod
    def get_type(self) -> str:
        pass

    @abstractmethod
    def get_sauce(self) -> str:
        pass

    @abstractmethod
    def get_filling(self) -> str:
        pass

    @abstractmethod
    def get_additives(self) -> List[str]:
        pass

    def set_pasta_type(self, pasta_type: str) -> None:
        self._pasta_type = pasta_type

    def get_pasta_type(self) -> str:
        return self._pasta_type

    def __str__(self) -> str:
        return (f"Паста: {self.get_type()}\n"
                f"Тип макарон: {self.get_pasta_type()}\n"
                f"Соус: {self.get_sauce()}\n"
                f"Начинка: {self.get_filling()}\n"
                f"Добавки: {', '.join(self.get_additives()) if self.get_additives() else 'нет'}\n"
                f"---")

    def to_dict(self) -> Dict[str, Any]:
        return {'type': self.get_type(), 'pasta_type': self.get_pasta_type(), 'sauce': self.get_sauce(),
                'filling': self.get_filling(), 'additives': self.get_additives()}


class CarbonaraPasta(Pasta):
    def get_type(self) -> str:
        return "Карбонара Deluxe"

    def get_sauce(self) -> str:
        return "Сливочно-яичный соус с панчеттой"

    def get_filling(self) -> str:
        return "Панчетта, яйца, пармезан"

    def get_additives(self) -> List[str]:
        return ["Перец", "Соль", "Оливковое масло"]


class BolognesePasta(Pasta):
    def get_type(self) -> str:
        return "Болоньезе Special"

    def get_sauce(self) -> str:
        return "Томатный соус с мясным рагу"

    def get_filling(self) -> str:
        return "Говядина, свинина, овощи"

    def get_additives(self) -> List[str]:
        return ["Базилик", "Чеснок", "Лук", "Морковь", "Сельдерей"]


class AlfredoPasta(Pasta):
    def get_type(self) -> str:
        return "Альфредо Supreme"

    def get_sauce(self) -> str:
        return "Сливочный соус с сыром пармезан"

    def get_filling(self) -> str:
        return "Курица, грибы, шпинат"

    def get_additives(self) -> List[str]:
        return ["Пармезан", "Сливочное масло", "Чеснок", "Петрушка"]


class MarinaraPasta(Pasta):
    def get_type(self) -> str:
        return "Маринара Gourmet"

    def get_sauce(self) -> str:
        return "Томатный соус с морскими травами"

    def get_filling(self) -> str:
        return "Креветки, мидии, кальмары"

    def get_additives(self) -> List[str]:
        return ["Чеснок", "Базилик", "Орегано", "Белое вино"]


class PastaFactory(ABC):
    @abstractmethod
    def create_pasta(self) -> Pasta:
        pass

    def prepare_pasta(self) -> Pasta:
        pasta = self.create_pasta()
        print(f"Готовим {pasta.get_type()}...")
        return pasta


class CarbonaraFactory(PastaFactory):
    def create_pasta(self) -> Pasta:
        return CarbonaraPasta()


class BologneseFactory(PastaFactory):
    def create_pasta(self) -> Pasta:
        return BolognesePasta()


class AlfredoFactory(PastaFactory):
    def create_pasta(self) -> Pasta:
        return AlfredoPasta()


class MarinaraFactory(PastaFactory):
    def create_pasta(self) -> Pasta:
        return MarinaraPasta()


class PastaBuilder:
    def __init__(self):
        self.pasta = None
        self.reset()

    def reset(self) -> None:
        self.pasta = CustomPasta()

    def set_type(self, pasta_type: str) -> 'PastaBuilder':
        self.pasta._type = pasta_type
        return self

    def set_sauce(self, sauce: str) -> 'PastaBuilder':
        self.pasta._sauce = sauce
        return self

    def set_filling(self, filling: str) -> 'PastaBuilder':
        self.pasta._filling = filling
        return self

    def set_pasta_type(self, pasta_type: str) -> 'PastaBuilder':
        self.pasta.set_pasta_type(pasta_type)
        return self

    def add_additive(self, additive: str) -> 'PastaBuilder':
        self.pasta._additives.append(additive)
        return self

    def build(self) -> Pasta:
        pasta = self.pasta
        self.reset()
        return pasta


class CustomPasta(Pasta):
    def get_type(self) -> str:
        return self._type or "Кастомная паста"

    def get_sauce(self) -> str:
        return self._sauce or "Без соуса"

    def get_filling(self) -> str:
        return self._filling or "Без начинки"

    def get_additives(self) -> List[str]:
        return self._additives


class PastaMenu:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._menu = {
                PastaType.CARBONARA: CarbonaraFactory(),
                PastaType.BOLOGNESE: BologneseFactory(),
                PastaType.ALFREDO: AlfredoFactory(),
                PastaType.MARINARA: MarinaraFactory()
            }
        return cls._instance

    def get_factory(self, pasta_type: PastaType) -> PastaFactory:
        return self._menu[pasta_type]

    def get_available_types(self) -> List[PastaType]:
        return list(self._menu.keys())


class PastaCookingApp:
    def __init__(self):
        self.menu = PastaMenu()
        self.builder = PastaBuilder()

    def show_menu(self) -> None:
        print("🍝 МЕНЮ ПАСТЫ 🍝")
        print("=" * 30)
        for i, pasta_type in enumerate(self.menu.get_available_types(), 1):
            print(f"{i}. {pasta_type.value}")
        print("5. Создать кастомную пасту")
        print("=" * 30)

    def cook_standard_pasta(self, choice: int) -> Pasta:
        types = self.menu.get_available_types()
        if 1 <= choice <= len(types):
            factory = self.menu.get_factory(types[choice - 1])
            return factory.prepare_pasta()
        else:
            raise ValueError("Неверный выбор")

    def cook_custom_pasta(self) -> Pasta:
        print("\nСоздание кастомной пасты:")
        pasta_types = ["спагетти", "феттучини", "пенне", "фарфалле", "равиоли"]
        for i, pt in enumerate(pasta_types, 1):
            print(f"{i}. {pt}")
        choice = int(input("Ваш выбор: "))
        pasta_type = pasta_types[choice - 1] if 1 <= choice <= len(pasta_types) else "спагетти"
        type_name = input("\nВведите тип пасты: ") or "Кастомная паста"
        sauce = input("Введите соус: ") or "Стандартный соус"
        filling = input("Введите начинку: ") or "Стандартная начинка"
        additives = [x.strip() for x in input("Добавки через запятую: ").split(",") if x.strip()]
        custom = (
            self.builder.set_type(type_name).set_sauce(sauce).set_filling(filling).set_pasta_type(pasta_type).build())
        for add in additives:
            custom._additives.append(add)
        print("Кастомная паста создана!")
        return custom

    def run(self) -> None:
        print("Добро пожаловать в приложение для приготовления пасты!")
        while True:
            print("\n" + "=" * 40)
            self.show_menu()
            try:
                choice = int(input("\nВыберите вариант (0 для выхода): "))
                if choice == 0:
                    print("До свидания! Приятного аппетита! 🍝")
                    break
                elif 1 <= choice <= 4:
                    pasta = self.cook_standard_pasta(choice)
                    print("\nВаша паста готова!")
                    print(pasta)
                elif choice == 5:
                    pasta = self.cook_custom_pasta()
                    print("\nВаша кастомная паста готова!")
                    print(pasta)
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("Введите число.")
            except Exception as e:
                print(f"Произошла ошибка: {e}")


def demonstrate_pasta_patterns():
    print("=== Демонстрация паттернов проектирования ===\n")
    factories = [CarbonaraFactory(), BologneseFactory(), AlfredoFactory()]
    print("1. Factory Method:")
    for f in factories:
        p = f.create_pasta()
        print(f"Фабрика создала: {p.get_type()}")
        print(f"Соус: {p.get_sauce()}")
        print(f"Начинка: {p.get_filling()}")
        print(f"Добавки: {', '.join(p.get_additives())}")
        print()
    print("2. Builder Pattern:")
    builder = PastaBuilder()
    custom = (builder.set_type("Экспериментальная паста").set_sauce("Соус Аль Кьянто").set_filling(
        "Грибы, сыр, курица").set_pasta_type("пенне").add_additive("Трюфельное масло").add_additive(
        "Пармезан").add_additive("Базилик").build())
    print(custom)
    print("3. Singleton Pattern:")
    menu1 = PastaMenu()
    menu2 = PastaMenu()
    print(f"menu1 is menu2: {menu1 is menu2}")
    print(f"Доступные типы: {[t.value for t in menu1.get_available_types()]}")
    print()


if __name__ == "__main__":
    demonstrate_pasta_patterns()
    app = PastaCookingApp()
    app.run()
print()

# Задание 3. Реализация паттерна Prototype с наследником и кастомной клонировкой
print("Задание №3\n---------------------------------")
from abc import ABC, abstractmethod
from typing import List, Dict
import copy
import json


# Абстрактный класс Prototype
class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def deep_clone(self):
        pass


# Класс Person, реализующий Prototype
class Person(Prototype):
    def __init__(self, name: str, age: int, hobbies: List[str] = None, contacts: Dict[str, str] = None):
        self.name = name
        self.age = age
        self.hobbies = hobbies or []
        self.contacts = contacts or {}

    def clone(self):
        """Поверхностное копирование"""
        return copy.copy(self)

    def deep_clone(self):
        """Глубокое копирование"""
        return copy.deepcopy(self)

    def custom_clone(self, **kwargs):
        """Клонирование с изменением атрибутов"""
        cloned = self.deep_clone()
        for key, value in kwargs.items():
            if hasattr(cloned, key):
                setattr(cloned, key, value)
        return cloned

    def add_hobby(self, hobby: str):
        self.hobbies.append(hobby)

    def add_contact(self, key: str, value: str):
        self.contacts[key] = value

    def __str__(self):
        return f"Person(name='{self.name}', age={self.age}, hobbies={self.hobbies}, contacts={self.contacts})"


# Наследник Employee с дополнительными атрибутами
class Employee(Person):
    def __init__(self, name: str, age: int, position: str, salary: float, hobbies: List[str] = None,
                 contacts: Dict[str, str] = None):
        super().__init__(name, age, hobbies, contacts)
        self.position = position
        self.salary = salary
        self.skills: List[str] = []

    def add_skill(self, skill: str):
        self.skills.append(skill)

    def __str__(self):
        base = super().__str__()[7:-1]  # убираем "Person(" и ")"
        return f"Employee({base}, position='{self.position}', salary={self.salary}, skills={self.skills})"


# Функция демонстрации Prototype
def demonstrate_prototype():
    print("=== Демонстрация Prototype ===\n")

    # Создаём оригинальный объект Person
    original_person = Person(
        name="Мария Петрова",
        age=29,
        hobbies=["плавание", "шахматы"],
        contacts={"email": "maria@example.com", "phone": "+79112223344"}
    )
    print("Оригинал Person:")
    print(original_person)
    print()

    # Поверхностное копирование
    shallow = original_person.clone()
    shallow.name = "Шаллоу Мария"
    shallow.hobbies.append("велоспорт")
    print("Поверхностный клон:")
    print(shallow)
    print("Оригинал после shallow clone:")
    print(original_person)
    print()

    # Глубокое копирование
    deep = original_person.deep_clone()
    deep.name = "Дип Мария"
    deep.hobbies.append("йога")
    deep.contacts["email"] = "deep_maria@example.com"
    print("Глубокий клон:")
    print(deep)
    print("Оригинал после deep clone:")
    print(original_person)
    print()

    # Кастомное клонирование
    custom = original_person.custom_clone(name="Александра", age=35)
    custom.add_hobby("рисование")
    custom.add_contact("linkedin", "linkedin.com/alexandra")
    print("Кастомный клон:")
    print(custom)
    print()

    # Демонстрация наследника Employee
    employee = Employee(
        name="Игорь Смирнов",
        age=32,
        position="Разработчик",
        salary=120000,
        hobbies=["программирование", "шахматы"],
        contacts={"email": "igor@example.com"}
    )
    employee.add_skill("Python")
    employee.add_skill("Django")

    employee_clone = employee.deep_clone()
    employee_clone.salary = 150000
    employee_clone.add_skill("JavaScript")

    print("Оригинальный Employee:")
    print(employee)
    print("Клон Employee с изменениями:")
    print(employee_clone)
    print()

    # Сериализация в JSON
    person_json = json.dumps(original_person.__dict__, ensure_ascii=False)
    employee_json = json.dumps(employee.__dict__, ensure_ascii=False)
    print("JSON оригинального Person:", person_json)
    print("JSON оригинального Employee:", employee_json)
    print()


if __name__ == "__main__":
    demonstrate_prototype()
