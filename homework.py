from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return self.MESSAGE.format(**asdict(self))
        # or another variant w/o **asdict
        # return self.MESSAGE.format(training_type=self.training_type,
        #                            duration=self.duration,
        #                            distance=self.distance,
        #                            speed=self.speed,
        #                            calories=self.calories)


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: int
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: float
    LEN_STEP: ClassVar[float] = 1.38
    SHIFT: ClassVar[float] = 1.1
    MULT: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories: float = ((self.get_mean_speed() + self.SHIFT) * self.MULT
                           * self.weight * self.duration)
        return calories


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight / self.M_IN_KM
                           * self.duration * self.MIN_IN_H)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: int
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[str] = 100

    def get_spent_calories(self) -> float:
        calories: float = (self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                           + (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                           / (self.height / self.CM_IN_M)
                           * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                           * self.weight) * (self.duration * self.MIN_IN_H)
        return calories


def read_package(workout_type: str, data: tuple) -> Training:
    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    try:
        training_type[workout_type]
        training = training_type[workout_type](*data)
        return training

    except KeyError:
        print('В исходных данных определен некорректный тип тренировки',
              workout_type)


def main(training: Training) -> str:
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


packages = [
    ('SWM', [720, 1, 80, 25, 40]),
    ('RUN', [15000, 1, 75]),
    ('WLK', [9000, 1, 75, 180]),
]

if __name__ == '__main__':
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training:
            main(training)
