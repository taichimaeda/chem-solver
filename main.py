from equation import Equation


def main():
    equation = Equation('Si2Cl4 + H2O = SiO2 + HCl + H2O')

    equation.parse_string()
    equation.create_matrix()


if __name__ == '__main__':
    main()