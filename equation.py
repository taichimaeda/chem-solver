import re
from util import *


# todo: this class needs to be split into modules later
class Equation:
    def __init__(self, input_str):
        self.input_str = input_str
        self.reactants = []
        self.products = []
        self.matrix = []

    def parse_string(self):
        """
        Parses user input string to list

        :return: reactant, products
        :rtype: tuple(list<str>, list<str>)
        """
        # detects coefficient in front of compounds
        if re.search(r'\+\s*\d+\w', self.input_str):
            # exception on invalid input
            raise Exception('Coefficient must be 1 in all compounds')

        # converting into list
        # todo: needs to be a more sophisticated way later
        reactants, products, *_ = self.input_str.split('=')
        reactants = reactants.split('+')
        products = products.split('+')
        reactants = list(map(lambda comp: comp.strip(), reactants))
        products = list(map(lambda comp: comp.strip(), products))

        # set to member variable
        self.reactants, self.products = reactants, products
        # todo: delete test
        print('reactants, products:', reactants, products)

    def create_matrix(self):
        """
        Creates matrix designed for solving simultaneous equations

        :return: matrix
        :rtype: list(list<int>)
        """
        reactants, products = self.reactants, self.products

        # find all elements that appear in reaction
        all_elems = set()
        for reactant in reactants:
            elems = re.findall(r'[A-Z][a-z]*[0-9]*', reactant)
            for elem in elems:
                elem = re.sub(r'[0-9]+', '', elem)
                all_elems.add(elem)
        all_elems = list(all_elems)

        # todo: delete test
        print('all_elems:', all_elems)

        # function to get matrix by half: reactants and then products
        def get_matrix_halfline(elem, comps, length):
            matrix_halfline = [0 for _ in range(length)]

            # for each compounds either in reactants or products
            for comp_index, comp in enumerate(comps):
                elem_count = 0
                # if the target element appears
                if comp.find(elem) != -1:
                    # get the subscript number for the element
                    elem_match = re.search(rf'{elem}([0-9]+)', comp)
                    if elem_match:
                        elem_count += int(elem_match.group(1))
                    else:
                        elem_count += 1
                # add them as a coefficient in matrix
                matrix_halfline[comp_index] += elem_count

            return matrix_halfline

        # set matrix using the above function
        matrix = []
        for elem in all_elems:
            matrix_line = get_matrix_halfline(elem, reactants, len(reactants))
            # each line of matrix stands for LHS of an equation whose sum is zero, so revert the sign for products
            matrix_line.extend(map(lambda x: -x, get_matrix_halfline(elem, products, len(products))))
            matrix.append(matrix_line)

        # set to member variable
        self.matrix = matrix
        # todo: delete test
        print('matrix: ', matrix)

    def gauss_eleiminte(self):
        """
        Converts the matrix to a unit matrix by gauss elimination

        :return: unit_matrix
        :rtype: list(list<int>)
        """
        matrix = self.matrix
        matrix_height = len(matrix)
        # note the matrix is extended so its width is 1 greater than its height
        matrix_width = matrix_height + 1

        # forward elimination
        # find pivot for each line
        for i in range(matrix_height):

            # todo: delete test
            print('')
            print('-------- current row:', i)
            for line in matrix:
                print(line)

            # find the pivot if the current one is zero
            if matrix[i][i] == 0:
                temp = [matrix[j][i] for j in range(matrix_height)]
                temp = list(map(lambda x: abs(x), temp))
                pivot_index = temp.index(max(temp))
                # swap lines
                matrix[i], matrix[pivot_index] = matrix[pivot_index], matrix[i]

            # todo: delete test
            print('------- after swapping:')
            for line in matrix:
                print(line)

            # for each line (go down from pivot with j)
            for j in range(i + 1, matrix_height):
                # avoid zero division error just in case
                if not matrix[i][i] == 0 and not matrix[j][i] == 0:
                    # find gcd first in order to get integer solutions
                    # using calc.lcm from util module
                    coeff_lcm = calc.lcm(matrix[j][i], matrix[i][i])
                    coeff_pivot = -(coeff_lcm // matrix[i][i])
                    coeff_target = (coeff_lcm // matrix[j][i])
                    # for each element (go across with k)
                    for k in range(matrix_width):
                        matrix[j][k] = coeff_target * matrix[j][k] + coeff_pivot * matrix[i][k]

        # todo: delete test
        print('')
        print('------- final:')
        for line in matrix:
            print(line)

        # backward elimination
        # from the bottom up to index 0 (excluding end point -1)
        for i in range(matrix_height - 1, -1, -1):

            # todo: delete test
            print('')
            print('-------- current row:', i)
            for line in matrix:
                print(line)

            # for each line (go up from pivot (matrix[i][i]) with j)
            for j in range(i - 1, -1, -1):
                # avoid zero division error just in case
                if not matrix[i][i] == 0 and not matrix[j][i] == 0:
                    coeff_lcm = calc.lcm(matrix[j][i], matrix[i][i])
                    coeff_pivot = -(coeff_lcm // matrix[i][i])
                    coeff_target = (coeff_lcm // matrix[j][i])

                    print('i', i, 'j', j)
                    print('target matrix', matrix[j][i])
                    print('pivot', matrix[i][i])
                    print('coeff_target', coeff_target, 'coeff_pivot', coeff_pivot)
                    # for each element (go across with k)
                    for k in range(matrix_width):
                        matrix[j][k] = coeff_target * matrix[j][k] + coeff_pivot * matrix[i][k]

        # set to member variable
        self.matrix = matrix

        # todo: delete test
        print('')
        print('------- final:')
        for line in matrix:
            print(line)

    def get_answers(self):
        """
        Gets answers

        :return:
        """
        # access members
        matrix = self.matrix
        matrix_height = len(matrix)
        matrix_width = matrix_height + 1
        reactants, products = self.reactants, self.products

        coeff_lcm = calc.lcm(
            *[matrix[i][i] for i in range(matrix_height)]
        )
        coeff_gcd = calc.gcd(
            *[matrix[i][matrix_width - 1] for i in range(matrix_height)]
        )

        answers = []
        for i in range(matrix_height):
            matrix[i][matrix_width - 1] = (matrix[i][matrix_width - 1] // coeff_gcd) * coeff_lcm

            answer = -(matrix[i][matrix_width - 1] // matrix[i][i])
            answers.append(answer)
        # the substituted variable = 1
        answers.append(1)

        # todo: delete test
        print(answers)

        def stringify_output(answers):
            output_str = ''
            for i in range(len(reactants)):
                output_str += f"{answers[i]}{reactants[i]} + "

            # remove the last ' + ' bit
            output_str = re.sub(r'\s\+\s$', '', output_str)
            output_str += '= '

            for i in range(len(products)):
                output_str += f"{answers[len(reactants) + i]}{products[i]} + "
            # remove the last ' + ' bit

            output_str = re.sub(r'\s\+\s$', '', output_str)

            return output_str

        return stringify_output(answers)
