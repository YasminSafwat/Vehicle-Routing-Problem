from Vehicle import Vehicle


class Depot:
    def __init__(self, idd,  x, y, no_of_vehicles):
        self.id = idd
        self.vehicles = [Vehicle(self) for _ in range(no_of_vehicles)]
        self.x_y_coordinates = (x, y)
        self.customers_list = list()

    def assign_customers(self, customer_object):
        self.customers_list.append(customer_object)

    def printing(self):
        return self.id
