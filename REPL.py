from VFUSL import Interpreter

def REPL():
    interpreter = Interpreter()
    while True:
        try:
            command = input("VFUSL> ")
            if command.lower() in ['exit', 'quit']:
                break
            interpreter.execute(command)
        #except Exception as e:
            #print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

#interpreter = Interpreter()
#print(interpreter.tokenize('[ |Hello, World!| [ |Hi2| ] 123 ]'))
REPL()