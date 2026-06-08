"""Continue smoke test file for Jarvis local integration."""


def bubble_sort(values):
    for i in range(len(values)):
        for j in range(len(values) - 1):
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
    return values


def render_workout(plan):
    return " -> ".join(plan)


if __name__ == "__main__":
    print(bubble_sort([5, 3, 4, 1, 2]))
    print(render_workout(["warmup", "strength", "metcon"]))
