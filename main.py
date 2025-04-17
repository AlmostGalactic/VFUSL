from VFUSL import Interpreter

def run_vf_file(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        interpreter = Interpreter()
        result = interpreter.execute(code)
        if result:
            print(f"Stack dump: {result}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    #except Exception as e:
        #print(f"Error: {e}")


if __name__ == "__main__":
    file_path = input("Enter the path to the VFUSL file (.vf): ")
    run_vf_file(file_path)