# Computer Architecture

## Project

* [Implement the LS-8 Emulator](ls8/)

## Task List: add this to the first comment of your Pull Request

### Day 1: Get `print8.ls8` running

- [ ] Inventory what is here
- [ ] Implement the `CPU` constructor
- [ ] Add RAM functions `ram_read()` and `ram_write()`
- [ ] Implement the core of `run()`
- [ ] Implement the `HLT` instruction handler
- [ ] Add the `LDI` instruction
- [ ] Add the `PRN` instruction

### Day 2: Add the ability to load files dynamically, get `mult.ls8` running

- [ ] Un-hardcode the machine code
- [ ] Implement the `load()` function to load an `.ls8` file given the filename
      passed in as an argument
- [ ] Implement a Multiply instruction (run `mult.ls8`)

### Day 3: Stack

- [ ] Implement the System Stack and be able to run the `stack.ls8` program

### Day 4: Get `call.ls8` running

- [ ] Implement the CALL and RET instructions
- [ ] Implement Subroutine Calls and be able to run the `call.ls8` program

### Stretch

- [ ] Add the timer interrupt to the LS-8 emulator
- [ ] Add the keyboard interrupt to the LS-8 emulator
- [ ] Write an LS-8 assembly program to draw a curved histogram on the screen


##### Notes
watch number bases and conversions
two videos from day 1
this video about the stack day 3
converting between number types
what is a cpu register

###### Number types
> Decimal - You know it already. Decimal is \
0 1 2 3 4 5 6 7 8 9 \
Base 10

> Binary - two numbers, 0 1. Base 2. Bit

> Hexadecimal - base 16 \
0 1 2 3 4 5 6 7 8 9 A B C D E F \

> Octal - base 8. 0 1 2 3 4 5 6 7. No one uses it.

###### Terminology
byte: 8 bits. aka octet. max val: 255 decimal, FF hex
nibble: 4 bits. rarely used. Max val: 15 decimal, F hex

###### Binary
+----------128s place
|+---------64s place
||+--------32s place
|||+-------16s place
||||+------8s place
|||||+-----4s place
||||||+----2s place
|||||||+---1s place
||||||||
01010110

       0 = 0
       1 = 1
      10 = 2
      11 = 3
     100 = 4

01010110
        0
        64
        0
        16
        0
        4
        2



###### Binary to hex
10100011 split it in half, 4s

1010 0011
            1 + 2 = 3
            2 + 8 = 10 = A
A3 = 10100011


C7

0000 0000
            C = 12 = 8 + 4 = 1100
            7 = 4 + 2 + 1 = 0111
11000111 = C7


###### 