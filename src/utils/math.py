def clamp(value, minval, maxval):
	if value > maxval:
		return maxval
	if value < minval:
		return minval
	return value
