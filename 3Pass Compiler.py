import re

class Compiler(object):
	
	def compile(self, program):
		return self.pass3(self.pass2(self.pass1(program)))
		
	def tokenize(self, program):
		"""Turn a program string into an array of tokens.  Each token
		   is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
		   name or a number (as a string)"""
		token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
		return [int(tok) if tok.isdigit() else tok for tok in token_iter]

	def pass1(self, program):
		"""Returns an un-optimized AST"""
		tokens = self.tokenize(program)
		
		# Find arguments
		# Store arguments in ordered list
		# Reorder tokens to postfix notation 
		# Parse the postfix expression and convert to result using a stack

		# Find arguments
		j = tokens.index("]")
		arguments = tokens[1:j] # Ordered in argument order

		tokens = tokens[j + 1::] # Reduce length of tokens 

		operators = ["+", "-", "*", "/"]
		precedence = lambda x: 1 if x == "+" or x == "-" else 2

		postfix_tokens = [] # Mathematical expression in flipped postfix order
		operator_stack = []
		for token in tokens:
			if token in operators:
				while len(operator_stack) > 0 and operator_stack[-1] != "(" and precedence(operator_stack[-1]) >= precedence(token):
					postfix_tokens.append(operator_stack.pop())
					
				operator_stack.append(token)
			elif token == ")":
				o = operator_stack.pop()
				while o != "(":
					postfix_tokens.append(o)
					o = operator_stack.pop()
			elif token == "(":
				operator_stack.append(token)
			else:
				postfix_tokens.append(token)

		postfix_tokens.extend(operator_stack[::-1])

		# Process each item in the postfix expression

		stack = []
		for token in postfix_tokens:
			v = {}
			if type(token) == int:
				v = { "op": "imm", "n": token }
			elif token in arguments:
				v = { "op": "arg", "n": arguments.index(token) }
			else:
				b = stack.pop()
				a = stack.pop()
				v = { "op": token, "a": a, "b": b }

			stack.append(v)
		
		return stack[0]
		
	def pass2(self, ast):
		"""Returns an AST with constant expressions reduced"""

		# Go through each level of the dict
		# If there is an operator with two immediate values beneath it
		# Combine them
		# See if that's good enough?

		if ast["op"] == "imm" or ast["op"] == "arg":
			return ast

		ast["a"] = self.pass2(ast["a"])
		ast["b"] = self.pass2(ast["b"])

		if ast["a"]["op"] == "imm" and ast["b"]["op"] == "imm":
			ast["n"] = eval(str(ast["a"]["n"]) + ast["op"] + str(ast["b"]["n"]))
			ast["op"] = "imm"

			del ast["a"]
			del ast["b"]

		return ast

	def pass3(self, ast, depth = 0):
		"""Returns assembly instructions"""

		# If immmediate load it and push to stack
		if ast["op"] == "imm":
			return [f"IM {ast['n']}", "PU"]
		
		# Similarly for arguments
		if ast["op"] == "arg":
			return [f"AR {ast['n']}", "PU"]

		# Otherwise it's an operator
		# So recursively find the sub expressions and add them to the start of the result
		assembly = []
		assembly = self.pass3(ast["a"], depth + 1) + self.pass3(ast["b"], depth + 1)

		# Pop from the stack and evaluate
		assembly += ["PO", "SW", "PO"]

		if ast["op"] == "+": assembly += ["AD"]
		if ast["op"] == "-": assembly += ["SU"]
		if ast["op"] == "*": assembly += ["MU"]
		if ast["op"] == "/": assembly += ["DI"]

		# Push it back to the stack if we're not on the first level, otherwise leave it in R0
		if depth != 0:
			assembly += ["PU"]

		return assembly

def simulate(asm, argv):
    r0, r1 = None, None
    stack = []
    for ins in asm:
        if ins[:2] == 'IM' or ins[:2] == 'AR':
            ins, n = ins[:2], int(ins[2:])
        if ins == 'IM':   r0 = n
        elif ins == 'AR': r0 = argv[n]
        elif ins == 'SW': r0, r1 = r1, r0
        elif ins == 'PU': stack.append(r0)
        elif ins == 'PO': r0 = stack.pop()
        elif ins == 'AD': r0 += r1
        elif ins == 'SU': r0 -= r1
        elif ins == 'MU': r0 *= r1
        elif ins == 'DI': r0 /= r1
    return r0

if __name__ == "__main__":
	c = Compiler()
	code = c.pass3(c.pass2(c.pass1("[a b] a * b")))
	print(simulate(code, [2, 2]))