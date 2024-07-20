import requests
import re
from collections import Counter
import matplotlib.pyplot as plt
import threading
from queue import Queue


# Функція для завантаження тексту з URL
def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


# Функція Map
def map_function(text, queue):
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    queue.put(word_counts)


# Функція Reduce
def reduce_function(queue):
    final_counts = Counter()
    while not queue.empty():
        word_counts = queue.get()
        final_counts.update(word_counts)
    return final_counts


# Функція для візуалізації результатів
def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()
    plt.show()


def main(url):
    # Завантаження тексту
    text = fetch_text(url)

    # Створення черги для зберігання результатів Map-функцій
    queue = Queue()

    # Розбивка тексту на частини для багатопотокової обробки
    num_threads = 4
    chunk_size = len(text) // num_threads
    threads = []

    for i in range(num_threads):
        chunk = text[i * chunk_size: (i + 1) * chunk_size]
        thread = threading.Thread(target=map_function, args=(chunk, queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Виконання Reduce-функції
    word_counts = reduce_function(queue)

    # Візуалізація результатів
    visualize_top_words(word_counts)


if __name__ == "__main__":
    # URL для аналізу
    url = 'https://www.gutenberg.org/files/1342/1342-0.txt'
    main(url)
