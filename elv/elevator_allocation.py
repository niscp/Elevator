from collections import defaultdict


LIFT_SPEED = 1
LIFT_CAPACITY = 10
LIFT_POSIITON = 1

class Elevator:
    def __init__(self, id):
        self.id = id
        self.capacity = LIFT_CAPACITY
        self.speed = LIFT_SPEED
        self.pos = LIFT_POSIITON
        self.upwards = True
        self.passengers = []

    def empty(self):
        return len(self.passengers) == 0

    def update(self, waiting_pass):
        msg_list = []
        boarding = 0
        for p in waiting_pass:
            for p2 in self.passengers:
                if p.name == p2.name:
                    p2.end = p.end
                    waiting_pass.remove(p)

        for p in self.passengers:
            if p.end == self.pos:
                k = 'passenger %s left by %s at Floor %s\n' % (p.name,self.id,self.pos)
                msg_list.append(k)
                boarding += 1
                self.passengers.remove(p)

        for p in waiting_pass:
            if p.start == self.pos and len(self.passengers) < self.capacity:
                self.passengers.append(p)
                boarding += 1
                k = 'passenger %s allocated to %s\n' % (p.name,self.id)
                msg_list.append(k)
                waiting_pass.remove(p)

        if self.upwards:
            alldown = self.passengers and all(e.end < self.pos for e in self.passengers)
            allbelow = self.empty() and waiting_pass and all(p.start < self.pos for p in waiting_pass)
            if alldown or allbelow:
                self.upwards = False
        else:
            allup = self.passengers and all(e.end > self.pos for e in self.passengers)
            allabove = self.empty() and waiting_pass and all(p.start > self.pos for p in waiting_pass)
            if allup or allabove:
                self.upwards = True

        if self.upwards:
            self.pos += self.speed
        else:
            self.pos -= self.speed if self.pos != 0 else 0
        return msg_list,boarding


class Passenger:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.pos = self.start


elevators = []
for i in range(10):
    elevators.append(Elevator("ELEVATOR #"+str(i)))

def start_work(input_data):
    passengers = defaultdict(list)
    for line in input_data:
        name, t, start, end = line[0], int(line[1]), int(line[2]), int(line[3])
        print name,t,start,end
        if start == end:
            continue
        passengers[t].append(Passenger(name, start, end))

    waiting_pass = []

    t = 0
    trace_list = []
    total_boarding_time = 0
    while True:
        waiting_pass.extend(passengers[t])

        for elevator in elevators:
            n,boarding = elevator.update(waiting_pass)
            total_boarding_time += boarding
            trace_list.extend(n)
        if not waiting_pass and all(e.empty() for e in elevators):
            break

        t += 1
    actual_time = (t-1) + total_boarding_time

    return actual_time,trace_list
