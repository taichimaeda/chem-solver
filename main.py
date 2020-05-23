from equation import Equation


def main():
    equation = Equation('Si2Cl4 + H2O = SiO2 + HCl + H2O')

    #equation.parse_string()
    #equation.create_matrix()
    matrix = [
        [4, 0, 0, -1, 0],
        [2, 0, -1, 0, 0],
        [0, 1, -2, 0, -1],
        [0, 2, 0, -1, -2]
    ]

    matrix2 = [
        [2, 1, 3, 6],
        [1, 3, 2, 1],
        [3, -2, -1, 7]
    ]
    print('init')
    for line in matrix2:
        print(line)


    equation.gauss_eleiminte(matrix2)

    #print(equation.get_answers())


if __name__ == '__main__':
    main()