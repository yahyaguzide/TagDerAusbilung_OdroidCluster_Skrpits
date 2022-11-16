import requests
import random
import threading
#from multiprocessing import cpu_count
from time import sleep

maxThreads = 4  # cpu_count()/2  # Get max amount of threads we can safely create
baseURL = ["http://mc1-", "-", ":5000/blink?values=", "."]
event_object = threading.Event()


class Droplet:
    def init(stack, node, led, color, baseURL):
        this.stack = stack
        this.node = node
        this.led = led
        this.baseURL = baseURL
        this.removeLastDrop = False
        this.removeDrop = False

        # If no Color was given use Random RGB
        if (len(color) == 0):
            this.color = [random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255)]
        else:
            this.color = color

    def movedroplet():
        if (not this.removeDrop and this.node > 3):
            this.removeDrop = True
        # Remove last drop, this makes it possible to simulate a sliding effect
        if (removeDrop):
            requests.get(this.baseURL[0]+str(this.stack)+this.baseURL[1]+str(this.node-1) +
                         this.baseURL[2]+str(this.led)+this.baseURL[3]+this.baseURL[3].join(map(str, color)))
        if (not this.removeDrop):
            # Draw next drop
            requests.get(this.baseURL[0]+str(this.stack)+this.baseURL[1]+str(this.node) +
                         this.baseURL[2]+str(this.led)+this.baseURL[3]+this.baseURL[3].join(map(str, color)))
        this.node += 1  # Increment Node
        if (not this.removeLastDrop and this.node > 1):
            this.removeLastDrop = True


def rainOnStack(nth_stack, color):
    droplets = []
    while true:
        if (event_object.wait()):
            for droplet in droplets:
                droplet.movedroplet()


if __name__ == "__main__":
    threads = []
    color = [255, 0, 0]
    for nth_stack in range(maxThreads):
        threads.append(threading.Thread(target=rainOnStack,
                       args=(nth_stack, color), daemon=True))

    while True:
        sleep(0.5)
        event_object.set()
