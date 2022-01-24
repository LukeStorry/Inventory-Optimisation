import simpy


def create_generator(environment, whys):
    while True:
        whys += 'Y'
        print(environment.now)
        yield environment.timeout(1)


environment = simpy.Environment()
whys = []
environment.process(create_generator(environment, whys))
environment.run(until=5)
print(whys)
environment.run(until=10)
print(whys)
