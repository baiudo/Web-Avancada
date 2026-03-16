import threading
import time
import random

semaphoro = threading.Semaphore(0)

class MySemaphoro():
    def __init__(self):
        self.item = None

    def produtor(self):
        time.sleep(10)
        self.item = random.randint(0, 1000)
        print("Item produzido: %s " % self.item)
        print("Produtor notificando: produzido item numero %s " % self.item )
        print("Chamando release() para avisar que o item esta disponivel")
        semaphoro.release()

    def consumidor(self):
        print("Tentando consumir item...")
        print("Chamando acquire() e aguardando liberacao do produtor")
        semaphoro.acquire()
        print("Consumidor notificando: cosumido item %s " % self.item)
        semaphoro.release()
        print('\n')


if __name__ == "__main__":
    obj = MySemaphoro()

    for i in range(0, 5):
        t1 = threading.Thread(target=obj.produtor)
        t2 = threading.Thread(target=obj.consumidor)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    print("Programa encerrado!")