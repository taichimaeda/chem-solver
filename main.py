from equation import Equation


def main():
    equation = Equation('Si2Cl4 + H2O = SiO2 + HCl + H2O')

    equation.parse_string()
    equation.create_matrix()
    #equation.gauss_eleiminte()

    #print(equation.get_answers())


if __name__ == '__main__':
    main()