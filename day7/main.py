import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

Operator = Callable[[int, int], int]


class IExpression(ABC):
    @abstractmethod
    def evaluate(self) -> int:
        pass


@dataclass(frozen=True)
class Constant(IExpression):
    value: int

    def evaluate(self) -> int:
        return self.value


@dataclass(frozen=True)
class Operation(IExpression):
    left: IExpression
    right: IExpression
    operator: Operator

    def evaluate(self) -> int:
        return self.operator(self.left.evaluate(), self.right.evaluate())


@dataclass
class Equation:
    result: int
    inputs: list[int]
    possible_operators: list[Operator]

    @staticmethod
    def from_str(equation_str: str, possible_operators: list[Operator]) -> "Equation":
        raw_result, raw_inputs = equation_str.split(": ")

        return Equation(
            int(raw_result),
            [int(input_str) for input_str in raw_inputs.split(" ")],
            possible_operators,
        )

    def can_be_made_true(self) -> bool:
        expressions: list[IExpression] = [Constant(self.inputs[0])]
        for constant in self.inputs[1:]:
            next_expressions, expressions = expressions, []
            for expression in next_expressions:
                for possible_operator in self.possible_operators:
                    expressions.append(
                        Operation(
                            left=expression,
                            right=Constant(constant),
                            operator=possible_operator,
                        )
                    )

        return any(expression.evaluate() == self.result for expression in expressions)


def concat(left: int, right: int) -> int:
    return int(str(left) + str(right))


def main() -> None:
    input_lines = Path("input/input.txt").read_text("utf-8").strip().split("\n")

    equations = [
        Equation.from_str(equation_str, [operator.add, operator.mul])
        for equation_str in input_lines
    ]
    print(sum(equation.result for equation in equations if equation.can_be_made_true()))

    equations_with_concat = [
        Equation.from_str(equation_str, [operator.add, operator.mul, concat])
        for equation_str in input_lines
    ]
    print(
        sum(
            equation.result
            for equation in equations_with_concat
            if equation.can_be_made_true()
        )
    )


if __name__ == "__main__":
    main()
