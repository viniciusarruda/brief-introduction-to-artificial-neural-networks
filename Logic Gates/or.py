import matplotlib.pyplot as plt
import numpy as np

class MP_Neuron:

	def __init__(self, weights, bias, threshold):
		self._weights = weights
		self._bias = bias
		self._threshold = threshold

	def classify(self, input):
		tmp = self._weights.transpose().dot(input)
		return np.array([self._activation_function(value) for value in tmp[0]])

	def _activation_function(self, value):
		# heaviside function
		return 1. if value >= self._threshold else 0.


def main():

	threshold = 0.5
	neuron = MP_Neuron(np.array([[1.],[1.]]), np.array([[0.]]), threshold)
	data = np.array([[0., 0., 1., 1.], [0., 1., 0., 1.]])
	print 'Input data:\n{}'.format(data)
	print '\nOutput classfied:\n{}'.format(neuron.classify(data))

	## plot
	x = np.linspace(-0.3,1.2,100)
	y = -x + threshold 
	plt.figure()
	plt.plot(x, y, 'k')
	plt.scatter(data[0][0], data[1][0], c='r', s=100)
	plt.scatter(data[0][1], data[1][1], c='g', s=100)
	plt.scatter(data[0][2], data[1][2], c='g', s=100)
	plt.scatter(data[0][3], data[1][3], c='g', s=100)
	plt.show()


if __name__ == '__main__':
	main()


