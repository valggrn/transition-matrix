from modules.transtition_matrix import TransitionMatrix 
from modules.file import File
import sys

def main():
    if len(sys.argv) < 3:
        print("python main.py 'path to text file' 'length of prefix'")
        sys.exit(1)

    data = File.get_data_from_file(sys.argv[1])
    splitedData = File.split_data(data)
    
    markov = TransitionMatrix(splitedData, int(sys.argv[2]))

    print(" ".join(markov.generate_text_by_matrix()))

if __name__ == "__main__":
    main()