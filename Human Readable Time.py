from doctest import OutputChecker


def format_duration(seconds):
	if seconds == 0: return "now"
	output = ""
	years = seconds // (60 * 60 * 24 * 365)
	days = seconds // (60 * 60 * 24) - (years * 365)
	hours = seconds // (60 * 60) - (years * 365 * 24) - (days * 24)
	minutes = seconds // 60  - (years * 365 * 24 * 60) - (days * 24 * 60) - (hours * 60)	
	seconds = seconds  - (years * 365 * 24 * 60 * 60) - (days * 24 * 60 * 60) - (hours * 60 * 60) - (minutes * 60)

	plural = lambda s: ("s" if s > 1 else "")

	if years > 0:
		output += f"{years} year" + plural(years)
	if days > 0:
		if len(output):
			output += ", "
		output += f"{days} day" + plural(days)
	if hours > 0:
		if len(output):
			output += ", "
		output += f"{hours} hour" + plural(hours)
	if minutes > 0:
		if len(output):
			if seconds:
				output += ", "
			else:
				output += " and "
		output += f"{minutes} minute" + plural(minutes)
	if seconds > 0:
		if len(output):
			output += " and "
		output += f"{seconds} second" + plural(seconds)

	return output