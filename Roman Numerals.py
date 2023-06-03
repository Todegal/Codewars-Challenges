class RomanNumerals:
	@staticmethod
	def to_roman(val):
		output = ""
		order = ["I", "V", "X", "L", "C", "D", "M"]

		components = []
		i = 3
		while i >= 0:
			components.insert(0, (val // (10 ** i)))
			val -= components[0] * (10 ** i)
			i -= 1

		for j, c in enumerate(components):
			v = j * 2
			if c < 4:
				output += c * order[v]
				continue
			if c == 4:
				output += order[v+1] + order[v]
				continue
			if c == 9:
				output += order[v+2] + order[v]
				continue
			if c >= 5:
				output += order[v] * (c - 5) + order[v+1]
				continue
				
		print(output[::-1])

	@staticmethod
	def from_roman(roman_num):
		symbols = {
			"I" : 1,
			"V" : 5,
			"X" : 10,
			"L" : 50,
			"C" : 100,
			"D" : 500,
			"M" : 1000
		}
		
		lastValue = 0
		total = 0
		for c in roman_num[::-1]:
			value = symbols[c]
			if value < lastValue:
				total -= value
				continue

			total += value
			lastValue = value

		return total
