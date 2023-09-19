import sys
import random
import re
import os
import pandas as pd

class Test:
    def __init__(self, filename, save=False) -> None:
        self.filename = filename
        self.filename, self.file_extension = os.path.splitext(filename)
        if not save and os.path.exists(self.filename + ".csv"):
            self.parse_csv()
        else:
            self.parse(save)

    def parse(self, save):
        with open(self.filename + self.file_extension, 'r') as f:
            test_cases = []
            for line in f:
                line = line.strip()
                result = re.search(r'\\item\[(.*)\]\{(.*)\}', line)
                if not result:
                    continue
                french, english = result.groups()
                test_cases.append([french, english])
        self.test_cases = pd.DataFrame(test_cases, columns=['french', 'english'])
        if save:
            self.save(self.test_cases, self.filename)
    
    def save(self, test_cases, filename):
        test_cases.to_csv(filename + ".csv")

    def parse_csv(self):
        self.test_cases = pd.read_csv(self.filename + ".csv")

    def generate(self):
        test_case = self.test_cases.sample()
        print(test_case['french'].values[0])
        input("Press Enter to show answer...")
        print(test_case['english'].values[0])


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 laf-test-generator.py <test_file>')
        sys.exit(1)
    filename = sys.argv[1]
    save = len(sys.argv) > 2 and sys.argv[2] == 'save'
    test = Test(filename, save)
    input("Press Enter to continue...")
    while input("Generate another test? (n): ") != 'n':
        test.generate()

if __name__ == '__main__':
    main()