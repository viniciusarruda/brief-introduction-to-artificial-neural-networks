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

	data = np.array([[0., 0., 1., 1.], [0., 1., 0., 1.]])
	print 'Input data:\n{}'.format(data)

	# First neuron of hidden layer
	threshold = 1.
	weights = np.array([[.6],[.6]])
	neuron = MP_Neuron(weights, np.array([[0.]]), threshold)
	output_first_neuron = neuron.classify(data) 

	# Second neuron of hidden layer
	threshold = .5
	weights = np.array([[1.1],[1.1]])
	neuron = MP_Neuron(weights, np.array([[0.]]), threshold)
	output_second_neuron = neuron.classify(data) 

	# Unique neuron of output layer
	threshold = .5
	weights = np.array([[-1.],[1.]])
	neuron = MP_Neuron(weights, np.array([[0.]]), threshold)
	# changes the data (i.e. maps the initial data to another space)
	data = np.array([output_first_neuron, output_second_neuron])
	print '\nOutput classfied:\n{}'.format(neuron.classify(data))

	## plot
	x = np.linspace(-0.3,1.2,100)
	y = ((- weights[0][0] * x) + threshold) / weights[1][0]
	plt.figure()
	plt.title("Note: (0,1) and (1,0) were mapped overlapping to (0,1).")
	plt.plot(x, y, 'k')
	plt.scatter(data[0][0], data[1][0], c='r', s=100)
	plt.scatter(data[0][1], data[1][1], c='g', s=100)
	plt.scatter(data[0][2], data[1][2], c='g', s=100)
	plt.scatter(data[0][3], data[1][3], c='r', s=100)
	plt.show()


if __name__ == '__main__':
	main()


