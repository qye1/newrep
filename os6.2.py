import time
import keyboard
from threading import Thread
from queue import Queue
def buffer_listener(buffer):
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            buffer.put(event.name)
            if event.name == 'esc':
                break
def buffer_sender(buffer, interval):
    while True:
        time.sleep(interval)
        if not buffer.empty():
            signals = []
            while not buffer.empty():
                signals.append(buffer.get())
            print(f"Передача сигналов: {', '.join(signals)}")

            if 'esc' in signals:
                print("Завершение программы.")
                break
def main():
    buffer = Queue()
    interval = int(input("Введите интервал: "))
    listener_thread = Thread(target=buffer_listener, args=(buffer,), daemon=True)
    listener_thread.start()
    buffer_sender(buffer, interval)
if __name__ == "__main__":
    main()