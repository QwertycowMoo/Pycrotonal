import numpy as np


def find_next_step(freq, edo):
    step = np.power(2, 1.0 / edo)
    return freq * step


def find_scale(root, edo, num_octaves=1):
    if root < 0:
        raise ValueError("This is not a valid root")
    scale = [root]
    for i in range(edo * num_octaves):
        # since we are dynamically adding things to scale, we can access indexs of scale
        # that are outside the initialization
        freq = scale[i]
        freq = np.around(find_next_step(freq, edo), 4)
        scale.append(freq)
    return scale

