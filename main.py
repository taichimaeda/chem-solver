from equation import Equation


def main():
    text1 = 'CH4 + O2 = CO2 + H2O'
    text2 = 'NaCl + SO2 + H2O + O2 = Na2SO4 + HCl'
    equation = Equation(input())

    equation.parse_string()
    equation.create_matrix()

    equation.gauss_eleiminte()

    print(equation.get_answers())


if __name__ == '__main__':
    main()