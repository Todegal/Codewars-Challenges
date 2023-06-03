import shlex

class Interpreter:
	def __init__(self):
		self.program = []
		self.pc = [0]
		self.cmp = 0
		self.output = []
		self.ended = False
		self.registers = {}
		self.ins = {}

		self.ins["mov"] = self.__ins_mov
		self.ins["inc"] = self.__ins_inc
		self.ins["dec"] = self.__ins_dec
		self.ins["add"] = self.__ins_add
		self.ins["sub"] = self.__ins_sub
		self.ins["mul"] = self.__ins_mul
		self.ins["div"] = self.__ins_div
		
		self.ins["jmp"] = self.__ins_jmp
		self.ins["cmp"] = self.__ins_cmp
		self.ins["jne"] = self.__ins_jne
		self.ins["je"] = self.__ins_je
		self.ins["jge"] = self.__ins_jge
		self.ins["jg"] = self.__ins_jg
		self.ins["jle"] = self.__ins_jle
		self.ins["jl"] = self.__ins_jl
		
		self.ins["call"] = self.__ins_call
		self.ins["ret"] = self.__ins_ret
		self.ins["msg"] = self.__ins_msg
		self.ins["end"] = self.__ins_end
	
	def get_value(self, value):
		if value in self.registers:
			return self.registers[value]
		else:
			return int(value)
	
	def sanitize_program(self, program):
		for line in program.splitlines():
			line = line.split(";")[0].strip()
			if len(line) == 0:
				continue

			line = shlex.split(line)
			line = [l.rstrip(",") for l in line]
			self.program.append(line)			
	
	def run(self, program):
		self.sanitize_program(program)
		while self.pc[0] < len(self.program) and not self.ended:
			ins = self.program[self.pc[0]][0]
			args = self.program[self.pc[0]][1:]
			
			if ins in self.ins:
				self.ins[ins](*args)
			
			self.pc[0] += 1
			
		if self.ended:
			return self.output

		return -1

	def __ins_mov(self, x, y):
		self.registers[x] = self.get_value(y)
		
	def __ins_inc(self, x):
		self.registers[x] += 1
		
	def __ins_dec(self, x):
		self.registers[x] -= 1

	def __ins_add(self, x, y):
		self.registers[x] += self.get_value(y)

	def __ins_sub(self, x, y):
		self.registers[x] -= self.get_value(y)

	def __ins_mul(self, x, y):
		self.registers[x] *= self.get_value(y)

	def __ins_div(self, x, y):
		self.registers[x] //= self.get_value(y)
	
	def __ins_call(self, lbl):
		for i, c in enumerate(self.program):
			if c[0] == lbl + ":":
				self.pc.insert(0, i)

	def jump(self, lbl):
		for i, c in enumerate(self.program):
			if c[0] == lbl + ":":
				self.pc[0] = i

	def __ins_jmp(self, lbl):
		self.jump(lbl)

	def __ins_cmp(self, x, y):
		self.cmp = self.get_value(x) - self.get_value(y)

	def __ins_jne(self, lbl):
		if self.cmp != 0:
			self.jump(lbl)

	def __ins_je(self, lbl):
		if self.cmp == 0:
			self.jump(lbl)

	def __ins_jge(self, lbl):
		if self.cmp >= 0:
			self.jump(lbl)

	def __ins_jg(self, lbl):
		if self.cmp > 0:
			self.jump(lbl)

	def __ins_jle(self, lbl):
		if self.cmp <= 0:
			self.jump(lbl)

	def __ins_jl(self, lbl):
		if self.cmp < 0:
			self.jump(lbl)
	
	def __ins_ret(self):
		self.pc.pop(0)

	def __ins_msg(self, *args):
		v = []
		for x in args:
			if x in self.registers:
				v += [str(int(self.registers[x]))]
			else:
				v += [x]
		self.output = "".join(v)

	def __ins_end(self):
		self.ended = True

def assembler_interpreter(program):
	return Interpreter().run(program)

if __name__ == "__main__":
	print(assembler_interpreter('''
call  func1
call  print
end

func1:
    call  func2
    ret

func2:
    ret

print:
    msg 'This program should return -1'
'''))