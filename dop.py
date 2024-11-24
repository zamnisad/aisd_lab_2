import matplotlib.pyplot as plt
import numpy as np
import os


class Color:
    Reset = '\033[0m'
    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'


class Errors:
    def __init__(self):
        pass

    @staticmethod
    def empty_data():
        return f"{Color.Red}Error: Cannot search for empty data in the tree!{Color.Reset}"

    @staticmethod
    def not_search(data):
        return f"{Color.Red}Error: Data not found in the tree! Data: {data} is not in the tree!{Color.Reset}"

    @staticmethod
    def equals_elements(data):
        return f"{Color.Red}Error: Duplicate element detected! Data: {data} cannot be added to the tree!{Color.Reset}"


def plot_graphs(name_out, name_in):
    sizes = []
    heights = []
    with open(name_in, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) == 2:
                size_str, height_str = parts

                size = int(size_str.split(":")[1].strip())
                height = int(height_str.split(":")[1].strip())

                sizes.append(size)
                heights.append(height)

    print(name_out)

    sizes = np.array(sizes)
    heights = np.array(heights)

    # Рассчитываем логарифмическую функцию log2(n)
    log2_values = np.log2(sizes)

    # Создаём директорию "Graphs", если она не существует
    if not os.path.exists("Graphs"):
        os.makedirs("Graphs")

    for i in range(2):
        # Строим график
        plt.figure(figsize=(10, 6))
        if i:
            if name_out == "BST":
                plt.plot(sizes, 2.3 * log2_values, linestyle="--", color="r", label=r"$\log_2(n)$",
                         alpha=0.5)
            elif name_out == "RB":
                plt.plot(sizes, 1.6 * log2_values, linestyle="--", color="r", label=r"$\log_2(n)$",
                         alpha=0.5)
            else:
                plt.plot(sizes, log2_values, linestyle="--", color="r", label=r"$\log_2(n)$",
                         alpha=0.5)

        # Основной график
        plt.plot(sizes, heights, marker="", linestyle="-", color="b", label="Height/Size")

        if i:
            plt.title(f"Height/Size and log2(n) in {name_out} tree")
            plt.ylabel("Heights / log2(n)", fontsize=14)
        else:
            plt.title(f"Height/Size in {name_out} tree")
            plt.ylabel("Heights", fontsize=14)
        plt.xlabel("Sizes", fontsize=14)

        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend(fontsize=12)

        # Сохраняем график в файл
        plt.savefig(os.path.join("Graphs", name_out + f"_{i}.jpg"))
        plt.close()


for filename in os.listdir("TXT"):
    full_path = os.path.join("TXT", filename)

    plot_graphs(filename.replace(".txt", ""), full_path)
