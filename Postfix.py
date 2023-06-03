from imaplib import IMAP4_stream
from lib2to3.pytree import convert
import re

def convert_to_postfix(expression: str) -> list:
    tokens = re.findall("(\w*[\.]?\w+|[\(\)\+\*\-\/])", expression)
    operators = ["/", "*", "+", "-"]

    stack = []
    output = []
    for token in tokens:
        if token.isnumeric():
            output.append(token)
        elif token in operators:
            if len(stack) == 0:
                stack.append(token)
            elif stack[-1] not in operators:
                stack.append(token)
            elif operators.index(token) < operators.index(stack[-1]):
                stack.append(token)
            elif operators.index(token) >= operators.index(stack[-1]):
                output.append(stack.pop())
                stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while True:
                t = stack.pop()
                if t != "(":
                    output.append(t)
                else:
                    break

    output.extend(stack[::-1])
    print(output)
    return output
        
def execute_postfix(postfix_tokens: list):
    stack = []
    for token in postfix_tokens:
        if token.isdigit():
            stack.append(int(token))
        elif len(re.findall("(\-?\d+\.\d+\b)", token)) > 0:
            stack.append(float(token))
        elif token == "*":
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
        elif token == "+":
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
        elif token == "-":
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif token == "/":
            a = stack.pop()
            b = stack.pop()
            stack.append(b / a)

    return stack[0]

if __name__ == "__main__":
    while True:
        print(execute_postfix(convert_to_postfix(input("- "))))