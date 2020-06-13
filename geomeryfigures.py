class Parameters:
    def __init__(self, base_param: int):
        self.base_param = base_param
        self.current_figure = None

    def choose_figure(self, figure_type):
        self.current_figure = figure_type

    def area(self):
        return self.current_figure.area(self.base_param)

    def perimeter(self):
        return self.current_figure.perimeter(self.base_param)

    def volume(self):
        return self.current_figure.volume(self.base_param)


class Figure:
    @staticmethod
    def area(base_size):
        return NotImplementedError()

    @staticmethod
    def perimeter(base_size):
        return NotImplementedError()

    @staticmethod
    def volume(base_size):
        return 0


class Circle(Figure):
    @staticmethod
    def area(base_size):
        return round(3.14159*(base_size**2), 2)

    @staticmethod
    def perimeter(base_size):
        return round(6.283185*base_size, 2)


class Triangle(Figure):
    @staticmethod
    def area(base_size):
        return round(0.43301*(base_size**2), 2)

    @staticmethod
    def perimeter(base_size):
        return round(3*base_size, 2)


class Square(Figure):
    @staticmethod
    def area(base_size):
        return round(base_size**2, 2)

    @staticmethod
    def perimeter(base_size):
        return round(4*base_size, 2)


class Pentagon(Figure):
    @staticmethod
    def area(base_size):
        return round(1.7205*(base_size**2), 2)

    @staticmethod
    def perimeter(base_size):
        return round(5*base_size, 2)


class Hexagon(Figure):
    @staticmethod
    def area(base_size):
        return round(2.5981*(base_size**2), 2)

    @staticmethod
    def perimeter(base_size):
        return round(6*base_size, 2)


class Cube(Figure):
    @staticmethod
    def area(base_size):
        return round(6*(base_size**2), 2)

    @staticmethod
    def perimeter(base_size):
        return round(12*base_size, 2)

    @staticmethod
    def volume(base_size):
        return round(base_size**3, 2)


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing

    figure = Parameters(10)

    figure.choose_figure(Circle())
    assert figure.area() == 314.16

    figure.choose_figure(Triangle())
    assert figure.perimeter() == 30

    figure.choose_figure(Square())
    assert figure.area() == 100

    figure.choose_figure(Pentagon())
    assert figure.perimeter() == 50

    figure.choose_figure(Hexagon())
    assert figure.perimeter() == 60

    figure.choose_figure(Cube())
    assert figure.volume() == 1000

    print("Coding complete? Let's try tests!")
