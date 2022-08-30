class Vehicle:
    def __init__(self, depot):
        self.depot = depot
        self.assigned_route = [self.depot, self.depot]

    def assign_route(self, assigned_route):
        self.assigned_route.insert(-1, assigned_route)

    def clear_route(self):
        self.assigned_route = [self.depot, self.depot]