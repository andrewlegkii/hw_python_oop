class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration_hours: float,
                 distance_km: float,
                 speed_kmh: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.distance = distance_km
        self.speed = speed_kmh
        self.calories = calories
        self.duration = duration_hours

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
                 duration_hours: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration_hours
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM
        

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration
        

    def get_spent_calories(self) -> float:
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CF_RUN_1 = 18
    CF_RUN_2 = 20
    minutes = 60

    def get_spent_calories(self) -> float:
        cal = self.CF_RUN_1 * self.get_mean_speed() - self.CF_RUN_2
        calories = cal * self.weight / self.M_IN_KM * self.duration * self.minutes
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    DEGREE_WALK_1 = 0.035
    DEGREE_WALK_2 = 2
    DEGREE_WALK_3 = 0.029
    minutes = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_1 = self.DEGREE_WALK_1 * self.weight
        calories_2 = self.get_mean_speed()**2 // self.height
        calories_3 = calories_2 * self.DEGREE_WALK_3 * self.weight
        calories = (calories_1 + calories_3) * self.duration * self.minutes
        return calories


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
        return self.length_pool * self.count_pool


    def get_spent_calories(self) -> float:
        calories_1 = self.get_mean_speed() + self.CF_SW_1
        calories = calories_1 * self.CF_SW_2 * self.weight
        return calories


def read_package(workout_type: str, int) -> Training:
    type_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_dict[workout_type](*data)


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