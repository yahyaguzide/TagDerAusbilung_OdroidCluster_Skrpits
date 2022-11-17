import requests
import random
import threading
import sys
from msvcrt import getch, kbhit
# from multiprocessing import cpu_count
from time import sleep

MAXTHREADS = 2  # cpu_count()/2  # Get max amount of threads we can safely create
BASEURL = ["http://mc1-", "-", ":5000/blink?values=", "."]
COLOR = [255, 0, 0]
timing_event = threading.Event()
exit_event = threading.Event()


class Droplet:
    def __init__(self, stack, node, led, color, baseURL):
        self.stack = stack
        self.node = node
        self.led = led
        self.baseURL = baseURL
        self.removeLastDrop = False
        self.removeDroplet = False

        # If no Color was given use Random RGB
        if (len(color) == 0):
            self.color = [random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255)]
        else:
            self.color = color

    def movedroplet(self):
        if (not self.removeDroplet and self.node > 3):
            self.removeDroplet = True
        # Remove last drop, this makes it possible to simulate a sliding effect
        if (self.removeLastDrop):
            requests.get(self.baseURL[0]+str(self.stack)+self.baseURL[1]+str(self.node-1) +
                         self.baseURL[2]+str(self.led)+self.baseURL[3]+"0.0.0"
                         )
            # NOTE: DEBUG INFO
            # print("Removing last Droplet:\n" +
            #      self.baseURL[0]+str(self.stack)+self.baseURL[1]+str(self.node-1) +
            #      self.baseURL[2]+str(self.led)+self.baseURL[3]+"0.0.0"
            #      )
            # DEBUG END
        if (not self.removeDroplet):
            # Draw next drop

            requests.get(self.baseURL[0]+str(self.stack)+self.baseURL[1]+str(self.node) +
                         self.baseURL[2]+str(self.led)+self.baseURL[3] +
                         self.baseURL[3].join(map(str, self.color))
                         )
            # NOTE: DEBUG INFO
            # print("Created Droplet:\n" +
            #      self.baseURL[0]+str(self.stack)+self.baseURL[1]+str(self.node) +
            #      self.baseURL[2]+str(self.led)+self.baseURL[3] +
            #      self.baseURL[3].join(map(str, self.color))
            #      )
            # DEBUG END
        self.node += 1  # Increment Node
        if (not self.removeLastDrop and self.node > 1):
            self.removeLastDrop = True


def rainOnStack(nth_stack, led, color, baseURL, maxDrops, randRange):
    droplet_list = []
    # for l_index in led:
    #    droplet_list.append(Droplet(nth_stack, 0, l_index, color, baseURL))

    while not exit_event.is_set():
        # Create new droplet if random int over certain number and list lenght under maxDrops
        if (len(droplet_list) < maxDrops):
            if (0 == random.randint(0, randRange)):
                droplet_list.append(
                    Droplet(nth_stack, 0, random.choice(led), color, baseURL))

        if (timing_event.wait()):
            for droplet in droplet_list:
                if (droplet.removeDroplet):
                    droplet_list.remove(droplet)
                    # NOTE: DEBUG INFO
                    # print("\nDroplet on stack "+str(droplet.stack) +
                    #      " at "+str(droplet.node)+" removed\n")
                    # DEBUG END
                    continue
                droplet.movedroplet()
                sleep(0.2)


if __name__ == "__main__":
    stackNumber = sys.argv[1]
    color = [sys.argv[2], sys.argv[3], sys.argv[4]]

    print(color)

    threads = []
    for nth_thread in range(MAXTHREADS):
        threads.append(threading.Thread(target=rainOnStack,
                                        args=(stackNumber, [1, 2], color, BASEURL, 2, 2), daemon=True))

    for t in threads:
        t.start()

    while True:
        # Stop Daemons
        if kbhit():
            if (ord(getch()) == 113):
                exit_event.set()
                print(
                    "\n####################################\nStop Singal to daemons send, exiting\n####################################\n")
                sleep(0.5)
                print("\n...Bye!")
                break
        sleep(1)
        timing_event.set()
        timing_event.clear()
