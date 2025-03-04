N = 512
M = int(np.ceil((16*N)/9))
# Gaussian spot centered in the middle
radius = 36
y, x = np.ogrid[-N//2:N//2, -M//2:M//2]
cells = np.exp(-0.5 * (x*x + y*y) / (radius*radius))

