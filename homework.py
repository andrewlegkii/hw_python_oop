from turtle import distance


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:

        self.training_type = training_type
        self.distance = distance
        """КМ"""
        self.speed = speed
        """КМ/Ч"""
        self.calories = calories
        self.duration = duration
        """Часы"""

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

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
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories()
                                   )
        return info_message


class Running(Training):
    """Тренировка: бег."""
    CF_RUN_1 = 18
    CF_RUN_2 = 20
    time_1 = 60

    def get_spent_calories(self) -> float:
        cal = self.CF_RUN_1 * self.get_mean_speed() - self.CF_RUN_2
        return cal * self.weight / self.M_IN_KM * self.duration * self.time_1


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF1 = 0.035
    COEFF2 = 2
    COEFF3 = 0.029
    time_2 = 60
    TRAINING_TYPE = 'WLK'

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
                * self.time_2))


class Swimming(Training):
    """Тренировка: плавание."""
    CF_SW_1 = 1.1
    CF_SW_2 = 2
    LEN_STEP = 1.38

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
        distance_1 = self.length_pool * self.count_pool
        self.distance_1 = distance_1 / super().M_IN_KM / self.duration 


    def get_spent_calories(self) -> float:
        calories = (self.get_mean_speed() + self.CF_SW_1) * self.CF_SW_2 * self.weight
        return calories


def read_package(workout_type: str, int) -> Training:
    type_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_dict[workout_type](*int)


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
        if training is None:
            print('Неожиданный тип тренировки')
        else:
            main(training)