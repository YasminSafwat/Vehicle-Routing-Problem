class Customer:
    def __init__(self, customer_id, x, y):
        self.id = customer_id
        self.x_y_coordinates = (x, y)

    def printing(self):
        return self.id
