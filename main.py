# This is a sample Python script.
import csv
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 读取csv至字典
    csvFile = open("./food/category.csv", "r")
    reader = csv.reader(csvFile)

    for item in reader:
        # 忽略第一行
        if reader.line_num == 1:
            continue
        print(item[2])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
