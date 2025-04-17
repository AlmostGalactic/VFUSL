# VFUSL
Very Full Stack Language

It is where every operation is added to the stack (Very original, I know >:D)

## How To Use
It is very simple, every thing you type is added to the stack. Then, during runtime it goes through the stack and runs it.

### Strings
Strings are made like | text |
```py
|Hello, World!|
```

### Code Blocks
Code blocks are made using [ ]

Code blocks will be very useful later on
```py
[ VFUSL CODE HERE ]
```

### Commands
There are many stack commands to actually make the program do programming language things!

Here are some:

1. print -- Prints the top value on the stack with a newline
   - EXAMPLE: ``` |Hello, World!| print ```
2. write -- Same thing as print but without a newline
   - EXAMPLE: ``` |Hello, | write |World!| write  ```
3. exec -- executes a code block. VERY USEFUL FEATURE
   - EXAMPLE: ``` [ 123 print ] exec ``` NOTE: Code blocks will not run unless called by exec.
4. +, -, *, /, % -- Kinda self explanatory. Uses reverse polish notation
5. ==, !=, <, <=, >, >= -- Also self explanatory.
   - EXAMPLE: ``` 2 1 > print ``` This would be true and would add it to the stack and print it
6. <--? -- If statement. More complex
   - EXAMPLE: ``` 1 2 > [ |True| print ] [ |False| print] <--? ``` If the top of the stack is true, it executes the first code block, else, it executes the second
7. create --  Creates a function. After you call the functions name, use exec after it to run the codeblock added to the stack.
   - EXAMPLE: ``` [ |Hello, World!| ] hello create ```  ``` hello exec ``` It will create a function with the name hello, and then it will execute it.
8. @in, @ord, @chr -- Python functions. @in gets input, @ord turns top stack char into ascii val, @chr turns top stack value fro ascii to char
9. whl -- A while loop. If the condition is true, it runs the code block. (Condition must be in code block)
    - EXAMPLE: ``` [ 2 1 > ] [ |FOREVER| ] whl `` this would check if 2 is more than 1, and since it is, it runs the code block next to whl.
10. : -- Duplicates the top item on the stack.

## Examples
Truth Machine
```py
@in
0 ==
[
    # Do nothing
]
[
    [1 1 ==] [ 1 write ] whl
] <--?
```
Cat Program
```py
@in
print
```
Haven't made a calcualtor program yet... Might take too long.
