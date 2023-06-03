from ctypes import ArgumentError
import math

class Blobservation:
	def __init__(self, height: int, width: int = 0):
		if not isinstance(height, int): raise ArgumentError("height must be an integer!")
		if not isinstance(width, int): raise ArgumentError("width must be an integer!")
		if width == 0: width = height

		if not( width <= 50 and height <= 50 ): raise ArgumentError("Dimensions must not exceed 50!")
		if not( width >= 8 and height >= 8 ): raise ArgumentError("Dimensions must not be less than 8!")
		
		self.current_population = [[0] * width for _ in range(height)]
		self.width = width; self.height = height

	def populate(self, start_population: list) -> None:
		if not isinstance(start_population, list): raise ArgumentError("start_population must be a list!")

		blobs = []
		for blob in start_population:
			if type(blob["x"]) != int or type(blob["y"]) != int or type(blob["size"]) != int:
				raise ArgumentError("Invalid properties in populate input!")

			x = blob["x"]
			y = blob["y"]
			size = blob["size"]

			if not( x >= 0 and x < self.height and y >= 0 and y < self.width ): raise ArgumentError("Location must be within room dimensions!")
			if not( size > 0 and size <= 20 ): raise ArgumentError("Size must be between 0 and 20!")

			blobs.append((x, y, size))

		for x, y, size in blobs:
			self.current_population[x][y] += size

	def calculate_angle(self, blob: tuple, target: tuple) -> float:
		dx, dy = target[0] - blob[0], target[1] - blob[1]
		raw_angle = math.atan(-dy / dx) if dx != 0 else math.pi / 2 if dy > 0 else -math.pi / 2
		angle = raw_angle + (0 if dy >= 0 and dx <= 0 else math.pi if dy >= 0 or dx > 0 else 2 * math.pi)
		return angle

	def select_target(self, blob: tuple, potential_targets: list) -> tuple:
		# Find nearest targets
		#	- Find distance to each target
		#	- Stor distance in list
		#	- Go through enumerated targets and lookup distance for comparison
		# If more than one largest size
		# If same size clockwise from top
		#	- Sort list using dot product
		#	- If X is less blob X subtract 1
		#	- Return first element

		distances = []
		for target in potential_targets:
			distances.append(max(abs(blob[0] - target[0]), abs(blob[1] - target[1])))

		min_distance = min(distances)
		potential_targets = [t for i, t in enumerate(potential_targets) if distances[i] == min_distance]

		if len(potential_targets) == 1:
			return potential_targets[0]

		max_size = max(potential_targets, key = lambda x: x[2])[2]
		potential_targets = [t for t in potential_targets if t[2] == max_size]

		if len(potential_targets) == 1:
			return potential_targets[0]

		potential_targets.sort(key = lambda x: self.calculate_angle(blob, x))
		return potential_targets[0]
		
	def move(self, iterations: int = 1) -> None:
		if not type(iterations) == int: raise ArgumentError("iterations must be an integer!")
		if not( iterations >= 1 ): raise ArgumentError("iterations must be a positive integer!")

		# For every iteration:

		#	Find all the blobs
		#	Find smallest blob size
		#	Find all blobs with a larger size
		#	Add small blobs to new generation
		#	For each blob with size:
		#		Find all blobs smaller (potential targets)
		#		Select target:
		#			- Closest
		#			- Largest
		#			- Clockwise (from up^)
		#		Find direction to target:
		#			- Round normalized vector
		#		Move 1 in that direction:
		#			- Add size to square in the new generation

		for i in range(iterations):
			next_generation = [[0] * self.width for _ in range(self.height)]

			blobs = [] # Find all the blobs
			for x, column in enumerate(self.current_population):
				for y, size in enumerate(column):
					if size > 0:
						blobs.append((x, y, size))

			if len(blobs) == 0: return
		
			smallest_blob_size = min(blobs, key = lambda x: x[2])[2] # Find smallest blob size

			small_blobs, big_blobs = [], []
			for blob in blobs:
				(small_blobs, big_blobs)[blob[2] > smallest_blob_size].append(blob)

			for blob in small_blobs: # Add small blobs to next generation
				next_generation[blob[0]][blob[1]] += blob[2]

			for blob in big_blobs:
				potential_targets = [b for b in blobs if b[2] < blob[2]] # Find all blobs smaller

				target = self.select_target(blob, potential_targets)

				d_x = target[0] - blob[0]
				d_y = target[1] - blob[1]

				if d_x != 0: d_x = 1 * (abs(d_x) / d_x)
				if d_y != 0: d_y = 1 * (abs(d_y) / d_y)

				n_x = int(blob[0] + d_x)
				n_y = int(blob[1] + d_y)

				next_generation[n_x][n_y] += blob[2]

			self.current_population = next_generation

	def print_state(self) -> list:
		blobs = []
		for x, column in enumerate(self.current_population):
			for y, size in enumerate(column):
				if size > 0:
					blobs.append([x, y, size])
		return blobs
