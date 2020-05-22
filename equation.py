import math
import re


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

        # initialize matrix
        #matrix = [[0 for _ in range(matrix_width)] for _ in range(matrix_height)]

        for elem in all_elems:
            matrix_line = get_matrix_halfline(elem, reactants, len(reactants))
            # each line of matrix stands for LHS of an equation whose sum is zero, so revert the sign for products
            matrix_line.extend(map(lambda x: -x, get_matrix_halfline(elem, products, len(products))))
            matrix.append(matrix_line)

        # set to member variable
        self.matrix = matrix
        # todo: delete test
        print('matrix: ', matrix)

    def gauss_eleiminte(self, matrix):
        """
        Converts the matrix to a unit matrix by gauss elimination

        note chemical equations have indeterminate solutions
        so pivoting and substitute some number to one of the variables (parameters)
        are necessary (in this case substitute 1 to the rightmost variables)

        :return: unit_matrix
        :rtype: list(list<int>)
        """
        # todo: remove arg matrix and comment out below after test is finished
        #matrix = self.matrix
        matrix_height = matrix_width = len(matrix)

        # forward elimination
        # find pivot for each line
        for i in range(matrix_height):
            # find the pivot
            temp = [matrix[j][i] for j in range(matrix_height)]
            pivot_index = temp.index(max(temp))
            # swap lines
            matrix[i], matrix[pivot_index] = matrix[pivot_index], matrix[i]

            # for each line (go down from pivot with j)
            for j in range(i + 1, matrix_height):
                coeff = -(matrix[j][0] / matrix[i][i])
                # for each element (go across with k)
                for k in range(matrix_width):
                    matrix[j][k] += coeff * matrix[i][k]

        # backward elimination (i and j decrements each time)
        for i in range(matrix_height - 1, 0, -1):
            # for each line (go up from pivot with j)
            for j in range(matrix_height - 1, 0, -1):
                coeff = -(matrix[j][matrix_width - 1] / matrix[i][i])
                # for each element (go across with k)
                for k in range(matrix_width):
                    matrix[j][k] += coeff * matrix[i][k]

        # set to member variable
        self.matrix = matrix

        # todo: delete test
        print(matrix)

    def get_answers(self):
        """
        Gets answers

        :return:
        """
        reactants, products = self.reactants, self.products
        reactants_length, products_length = len(reactants), len(products)
        matrix = self.matrix
        matrix_height = matrix_width = len(matrix)

        answers = []
        for i in range(matrix_height):
            answer = matrix[i][0] / matrix[i][i]
            answers.append(answer)

        # stringify
        output_str = ''
        for i in range(reactants_length):
            output_str += f"{answers[i]}{reactants[i]} + "

        # remove the last ' + ' bit
        output_str = re.sub(r'\s\+\s$', '', output_str)
        output_str += '= '

        # todo: this one also needs to be refactored somehow it's ugly
        for i in range(reactants_length, reactants_length + products_length):
            output_str += f"{answers[i]}{products[i]} + "

        # remove the last ' + ' bit
        output_str = re.sub(r'\s\+\s$', '', output_str)
