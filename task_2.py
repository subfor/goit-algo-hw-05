def binary_search_upper_bound(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        if arr[mid] < x:
            low = mid + 1
        else:
            upper_bound = arr[mid]
            high = mid - 1

    return (iterations, upper_bound)


def main():
    arr = [1.1, 2.2, 3.3, 4.4, 5.5]
    x = 3

    iterations, upper = binary_search_upper_bound(arr, x)

    print(f"Ітерацій: {iterations}")
    print(f"Верхня межа: {upper}")


if __name__ == "__main__":
    main()
