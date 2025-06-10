import matplotlib.pyplot as plt
import numpy as np

area1 = 0.6
area2 = 193

radius1 = (area1 / np.pi) ** 0.5
radius2 = (area2 / np.pi) ** 0.5

theta1 = np.linspace(0, 2 * radius1 * np.pi, 100)
theta2 = np.linspace(0, 2 * radius2 * np.pi, 100)

x1 = radius1 * np.cos(theta1)
y1 = radius1 * np.sin(theta1)

x2 = radius2 * np.cos(theta2)
y2 = radius2 * np.sin(theta2)

fig, axes = plt.subplots(1, 2, figsize = (10, 5))

axes[0].plot(x1, y1)
axes[0].set_title('Value 1')

axes[1].plot(x2, y2)
axes[1].set_title('Value 2')

plt.tight_layout()

plt.savefig('circle.png', dpi = 300)

