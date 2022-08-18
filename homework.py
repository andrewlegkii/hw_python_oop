class InfoMessage:
    """Информационное сообщение о тренировке. Пояснения: speed=КМ/Ч;
     distance=КМ; duration=Часы"""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:

        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: int = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        raise NotImplementedError("Для работы всех наследников")

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CF_RUN_1: int = 18
    CF_RUN_2: int = 20
    MINS_IN_HOUR: int = 60

    def get_spent_calories(self) -> float:
        cal = self.CF_RUN_1 * self.get_mean_speed() - self.CF_RUN_2
        return (cal * self.weight / self.M_IN_KM * self.duration 
        * self.MINS_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF1: float = 0.035
    COEFF2: int = 2
    COEFF3: float = 0.029
    MINS_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF3 * self.weight) * (self.duration
                * self.MINS_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    CF_SW_1: float = 1.1
    CF_SW_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        total_distance = self.length_pool * self.count_pool
        return total_distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> int:
        men_speed_with_coef = self.get_mean_speed() + self.CF_SW_1
        return men_speed_with_coef * self.CF_SW_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    type_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    data: list[int]
    return type_dict[workout_type](*data)


try:
    workout_type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
except KeyError:
    raise KeyError('Неизвестный тип тренировки')


def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)