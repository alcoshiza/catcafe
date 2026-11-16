import random
from typing import List, Type
from interfaces import IEvent
from models import CafeState

class CatAccidentEvent(IEvent):
    @property
    def title(self) -> str:
        return "🐱 ФОРС-МАЖОР: Зламана кавоварка"

    @property
    def description(self) -> str:
        return "Кіт Барсік скочив на стіл і зламав сенсор кавоварки! Що будете робити?"

    @property
    def options(self) -> List[str]:
        return [
            "Викликати термінового майстра (-600 грн)",
            "Спробувати полагодити власноруч (шанс 50/50)",
            "Працювати без машини (-15 репутації)"
        ]

    def execute(self, state: CafeState, choice_index: int) -> str:
        if choice_index == 0:
            state.budget.withdraw(600)
            return "Майстер все полагодив! Кафе знову працює (-600 грн)."
        elif choice_index == 1:
            if random.random() > 0.5:
                return "Успіх! Вам вдалося полагодити деталь власноруч без витрат."
            else:
                state.budget.withdraw(900)
                state.reputation.modify(-5)
                return "Стало тільки гірше! Довелося платити за термінову деталь 900 грн та втрачено 5 репутації."
        else:
            state.reputation.modify(-15)
            return "Кава готується повільніше, клієнти незадоволені (-15 репутації)."


class InfluencerEvent(IEvent):
    @property
    def title(self) -> str:
        return "⭐ ПОДІЯ: Популярний блогер"

    @property
    def description(self) -> str:
        return "До кафе завітав популярний блогер із котиком! Які ваші дії?"

    @property
    def options(self) -> List[str]:
        return [
            "Пригостити за рахунок закладу (-150 грн)",
            "Взяти повну оплату"
        ]

    def execute(self, state: CafeState, choice_index: int) -> str:
        if choice_index == 0:
            state.budget.withdraw(150)
            state.reputation.modify(15)
            return "Блогер зробив чудовий відгук у соцмережах! (+15 репутації)."
        else:
            return "Блогер розрахувався, але нічого не опублікував."


class SpoiledMilkEvent(IEvent):
    @property
    def title(self) -> str:
        return "🥛 ФОРС-МАЖОР: Кисле молоко"

    @property
    def description(self) -> str:
        return "Зранку виявили партію зіпсованого молока."

    @property
    def options(self) -> List[str]:
        return ["Купити свіже молоко (-200 грн)"]

    def execute(self, state: CafeState, choice_index: int) -> str:
        state.budget.withdraw(200)
        return "Довелося терміново докупити свіже молоко в магазині (-200 грн)."


class QuietDayEvent(IEvent):
    @property
    def title(self) -> str:
        return "🐾 Спокійний ранок"

    @property
    def description(self) -> str:
        return "Ранок спокійний, котики мирно сплять на диванах."

    @property
    def options(self) -> List[str]:
        return ["Продовжити день"]

    def execute(self, state: CafeState, choice_index: int) -> str:
        return "День починається в гарному настрої."


class CatSickOrInjuredEvent(IEvent):
    """Форс-мажор: кіт підвернув лапу або захворів."""
    @property
    def title(self) -> str:
        return "🩹 ФОРС-МАЖОР: Кіт підвернув лапу або захворів"

    @property
    def description(self) -> str:
        return "Кіт невдало зістрибнув зі шафи, підвернув лапку і жалібно нявчить біля бару!"

    @property
    def options(self) -> List[str]:
        return [
            "Викликати ветеринара додому (-400 грн, +5 ⭐)",
            "Накласти пов'язку та вітаміни (шанс 50/50)",
            "Сподіватися, що саме мине (-20 ⭐)"
        ]

    def execute(self, state: CafeState, choice_index: int) -> str:
        if choice_index == 0:
            state.budget.withdraw(400)
            state.reputation.modify(5)
            return "Лікар наклав еластичний бинт і виписав вітаміни. Кіт швидко одужує (-400 грн, +5 репутації)."
        elif choice_index == 1:
            if random.random() > 0.5:
                state.budget.withdraw(80)
                return "Вдалося самотужки накласти зручну пов'язку, котику вже краще (-80 грн на аптечку)."
            else:
                state.budget.withdraw(700)
                state.reputation.modify(-5)
                return "Лапка розпухла! Довелося терміново везти котика у клініку на рентген (-700 грн, -5 репутації)."
        else:
            state.reputation.modify(-20)
            return "Відвідувачі обурені неуважністю до тварин! Репутація сильно впала (-20 репутації)."


class CafeRobberyEvent(IEvent):
    """Форс-мажор: кафе пограбували."""
    @property
    def title(self) -> str:
        return "🚨 ФОРС-МАЖОР: Кафе пограбували!"

    @property
    def description(self) -> str:
        return "Вночі хтось заліз через кватирку! Вкрали гроші з сейфу та мішок кавових зерен!"

    @property
    def options(self) -> List[str]:
        return [
            "Викликати поліцію та сигналізацію (-500 грн, +5 ⭐)",
            "Змиритися із втратою частини каси (-350 грн)",
            "Кіт Тузік на варті (-100 грн на сосиски, +10 ⭐)"
        ]

    def execute(self, state: CafeState, choice_index: int) -> str:
        if choice_index == 0:
            state.budget.withdraw(500)
            state.reputation.modify(5)
            return "Поліція оперативно зафіксувала злом, а нова сигналізація захистить кафе (-500 грн, +5 репутації)."
        elif choice_index == 1:
            state.budget.withdraw(350)
            return "Грабіжники забрали 350 грн з каси розмінної готівки (-350 грн)."
        else:
            state.budget.withdraw(100)
            state.reputation.modify(10)
            return "Кіт Тузік одягнув значок шерифа і тепер грізно пильнує вікно! Відвідувачі у захваті (+10 репутації, -100 грн)."


class CatKidnappedEvent(IEvent):
    """Форс-мажор: кота викрали."""
    @property
    def title(self) -> str:
        return "🕵️ ФОРС-МАЖОР: Кота викрали!"

    @property
    def description(self) -> str:
        return "Хтось із відвідувачів тихцем виніс у рюкзаку кота Кулька! На камерах видно підозрілого незнайомця."

    @property
    def options(self) -> List[str]:
        return [
            "Оголосити винагороду в Instagram (-300 грн, +20 ⭐)",
            "Піти на пошуки районами самостійно (шанс 50/50)",
            "Викупити Кулька за ласощі у сусіда (-150 грн)"
        ]

    def execute(self, state: CafeState, choice_index: int) -> str:
        if choice_index == 0:
            state.budget.withdraw(300)
            state.reputation.modify(20)
            return "Пост у соцмережах став вірусним! Кулька повернули за годину, а підписники валом пішли до кафе (+20 репутації, -300 грн)."
        elif choice_index == 1:
            if random.random() > 0.5:
                state.reputation.modify(10)
                return "Ви знайшли викрадача у парку та вмовили повернути кота без бійки! (+10 репутації)."
            else:
                state.budget.withdraw(250)
                state.reputation.modify(-5)
                return "Пошуки затяглися, довелося витратитися на друк листівок та таксі (-250 грн, -5 репутації)."
        else:
            state.budget.withdraw(150)
            return "Викрадачем виявився підліток-сусід. Він віддав Кулька за упаковку елітного котячого паштету (-150 грн)."


class KidDrewMustacheEvent(IEvent):
    """Форс-мажор: маленька дитина намалювала коту вуса."""
    @property
    def title(self) -> str:
        return "🎨 ФОРС-МАЖОР: Дитина намалювала коту вуса!"

    @property
    def description(self) -> str:
        return "Маленький гість дістав незмивний маркер і домалював Барсіку другі вуса та окуляри як у Гаррі Поттера!"

    @property
    def options(self) -> List[str]:
        return [
            "Купити спеціальний делікатний шампунь (-150 грн)",
            "Новий арт-стиль та відео в TikTok (+15 ⭐, +80 грн)",
            "Влаштувати скандал з батьками дитини (-10 ⭐)"
        ]

    def execute(self, state: CafeState, choice_index: int) -> str:
        if choice_index == 0:
            state.budget.withdraw(150)
            return "Котика відмили до блиску, тепер Барсік пахне лавандою (-150 грн)."
        elif choice_index == 1:
            state.budget.add(80)
            state.reputation.modify(15)
            return "Відео з котом-чарівником зібрало мільйон переглядів! Відвідувачі в захваті (+15 репутації, +80 грн чайових)."
        else:
            state.reputation.modify(-10)
            return "Батьки написали гнівний відгук у Google Maps, репутація постраждала (-10 репутації)."


class CatStuckInBoxEvent(IEvent):
    """Курйоз: кіт Скумбрія застряг у коробці."""
    @property
    def title(self) -> str:
        return "📦 КУРЙОЗ: Кіт Скумбрія застряг у коробці"

    @property
    def description(self) -> str:
        return "Кіт Скумбрія спробував втиснутися у крихітну коробку від десертів і тепер бігає як панцирна черепаха!"

    @property
    def options(self) -> List[str]:
        return [
            "Зняти відео 'Кіт-трансформер' (+20 ⭐, +100 грн)",
            "Обережно зняти коробку за допомогою олії (-40 грн)",
            "Виманити шматочком рибки, щоб виліз сам (-60 грн)"
        ]

    def execute(self, state: CafeState, choice_index: int) -> str:
        if choice_index == 0:
            state.budget.add(100)
            state.reputation.modify(20)
            return "Кіт став зіркою інтернету! Гості посміхаються та залишають щедрі чайові (+20 репутації, +100 грн)."
        elif choice_index == 1:
            state.budget.withdraw(40)
            return "Скумбрія звільнена без жодної подряпини (-40 грн на серветки та олію)."
        else:
            state.budget.withdraw(60)
            return "Запах риби зробив магію — кіт миттєво вислизнув із пастки (-60 грн на смаколик)."


class CatDrankEspressoEvent(IEvent):
    """Курйоз: кіт Прікол випив еспресо."""
    @property
    def title(self) -> str:
        return "⚡ КУРЙОЗ: Кіт Прікол випив еспресо!"

    @property
    def description(self) -> str:
        return "Кіт Прікол скочив на бар і злизав пінку подвійного еспресо! Тепер він бігає по стелі на гіпершвидкості!"

    @property
    def options(self) -> List[str]:
        return [
            "Ловити реактивного кота всім залом (+15 ⭐)",
            "Купити заспокійливі ласощі з м'ятою (-120 грн)",
            "Почекати, поки сяде батарейка (-60 грн)"
        ]

    def execute(self, state: CafeState, choice_index: int) -> str:
        if choice_index == 0:
            state.reputation.modify(15)
            return "Справжній квест згуртував усіх клієнтів! Прікола спіймано, всі щасливі (+15 репутації)."
        elif choice_index == 1:
            state.budget.withdraw(120)
            return "М'ятні ласощі подіяли: кіт заснув солодким сном на барній стійці (-120 грн)."
        else:
            state.budget.withdraw(60)
            return "Поки Прікол літав по полицях, він випадково зачепив дизайнерську чашку (-60 грн)."


class EventFactory:
    """Фабрика для генерації подій."""
    def __init__(self):
        self._events: List[Type[IEvent]] = [
            CatAccidentEvent,
            InfluencerEvent,
            SpoiledMilkEvent,
            QuietDayEvent,
            CatSickOrInjuredEvent,
            CafeRobberyEvent,
            CatKidnappedEvent,
            KidDrewMustacheEvent,
            CatStuckInBoxEvent,
            CatDrankEspressoEvent
        ]

    def get_random_event(self) -> IEvent:
        event_cls = random.choice(self._events)
        return event_cls()
