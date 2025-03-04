class Drawing:
    def __init__(self, width = 800, height = 600):
        self.colors = np.array([np.ogrid[0.:255.:256j], np.ogrid[0.:255.:256j], np.ogrid[0.:255.:256j]]).T
        self.dimensions = (width, height)
        self.screen = pg.display.set_mode(self.dimensions)

    def draw(self, cells):
        indices = (255*cells).astype(dtype=np.int32)
        surface = pg.surfarray.make_surface(self.colors[indices.T])
        surface = pg.transform.flip(surface, False, True)
        surface = pg.transform.scale(surface, self.dimensions)
        self.screen.blit(surface, (0,0))
        pg.display.update()
