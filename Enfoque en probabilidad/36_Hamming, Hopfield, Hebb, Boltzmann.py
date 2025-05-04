import numpy as np
import matplotlib.pyplot as plt

# -------------------------- Red de Hamming --------------------------

def hamming_encode(data):
    G = np.array([[1, 0, 0, 0, 1, 1, 0],
                  [0, 1, 0, 0, 1, 0, 1],
                  [0, 0, 1, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1]])
    encoded = np.dot(data, G) % 2
    return encoded

def hamming_decode(encoded):
    H = np.array([[1, 1, 1, 0, 1, 0, 0],
                  [1, 1, 0, 1, 0, 1, 0],
                  [1, 0, 1, 1, 0, 0, 1]])
    syndrome = np.dot(encoded, H.T) % 2
    if np.sum(syndrome) == 0:
        return encoded[:4]
    error_pos = int("".join(map(str, syndrome[::-1])), 2) - 1
    encoded[error_pos] = 1 - encoded[error_pos]
    return encoded[:4]

# -------------------------- Red de Hopfield --------------------------

class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))

    def train(self, patterns):
        for p in patterns:
            p = np.array(p)
            self.weights += np.outer(p, p)
        np.fill_diagonal(self.weights, 0)

    def predict(self, x):
        prev = np.zeros_like(x)
        while not np.array_equal(prev, x):
            prev = np.copy(x)
            for i in range(self.size):
                x[i] = np.sign(np.dot(self.weights[i], x))
        return x

# -------------------------- Aprendizaje Hebbiano --------------------------

class HebbianLearning:
    def __init__(self, input_size):
        self.weights = np.zeros(input_size)

    def train(self, X, epochs=10, lr=0.1):
        for epoch in range(epochs):
            for x in X:
                self.weights += lr * x * self.weights
            print(f"Epoch {epoch+1}, Pesos: {self.weights}")

    def predict(self, x):
        return np.dot(x, self.weights)

# -------------------------- Red de Boltzmann --------------------------

class BoltzmannMachine:
    def __init__(self, num_visible, num_hidden):
        self.num_visible = num_visible
        self.num_hidden = num_hidden
        self.weights = np.random.randn(num_visible, num_hidden) * 0.1
        self.visible_bias = np.zeros(num_visible)
        self.hidden_bias = np.zeros(num_hidden)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sample_hidden(self, visible):
        h = np.dot(visible, self.weights) + self.hidden_bias
        return self.sigmoid(h)

    def sample_visible(self, hidden):
        v = np.dot(hidden, self.weights.T) + self.visible_bias
        return self.sigmoid(v)

    def train(self, data, epochs=10, learning_rate=0.1):
        for epoch in range(epochs):
            for sample in data:
                hidden = self.sample_hidden(sample)
                visible = self.sample_visible(hidden)
                self.weights += learning_rate * np.outer(sample - visible, hidden)
            print(f"Epoch {epoch+1} completed.")

# -------------------------- Ejemplo de uso --------------------------

# 1. Red de Hamming
message = np.array([1, 0, 1, 1])  # Mensaje original
encoded_message = hamming_encode(message)  # Codificar
encoded_message[2] = 1 - encoded_message[2]  # Introducir error
decoded_message = hamming_decode(encoded_message)  # Decodificar y corregir
print(f"Mensaje codificado: {encoded_message}")
print(f"Mensaje decodificado: {decoded_message}")

# 2. Red de Hopfield
patterns = [np.array([1, 1, 1, -1]), np.array([-1, -1, -1, 1])]
hopfield = HopfieldNetwork(4)
hopfield.train(patterns)
noisy_input = np.array([1, 1, 1, 1])
recovered_pattern = hopfield.predict(noisy_input)
print(f"Patrón recuperado por Hopfield: {recovered_pattern}")

# 3. Aprendizaje Hebbiano
hebbian_input = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
hebbian_net = HebbianLearning(input_size=2)
hebbian_net.train(hebbian_input)

# 4. Red de Boltzmann
boltzmann_data = np.array([[1, 0, 1], [0, 1, 0], [1, 1, 0]])
boltzmann = BoltzmannMachine(3, 2)
boltzmann.train(boltzmann_data)
