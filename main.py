from equation import Equation


def main():
    equation = Equation('CH4 + O2 = CO2 + H2O')

    equation.parse_string()
    equation.create_matrix()

    equation.gauss_eleiminte()


    print(equation.get_answers())


if __name__ == '__main__':
    main()