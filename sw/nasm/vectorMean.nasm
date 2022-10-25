; ------------------------------------
; Calcule a média dos valores de um vetor
; que possui inicio em RAM[5] e tamanho
; defindo em RAM[4],
;
; 1. Salve a soma em RAM[1]
; 2. Salve a média em RAM[0]
; 
; ------------------------------------
; antes       | depois
;             |
; RAM[0]:     | RAM[0]:  2  : média 
; RAM[1]:     | RAM[1]:  8  : soma
; RAM[2]:     | RAM[2]:  
; RAM[3]:     | RAM[3]:  
; RAM[4]:  4  | RAM[4]:  4 
; RAM[5]:  1  | RAM[5]:  1 - 
; RAM[6]:  2  | RAM[6]:  2 | vetor
; RAM[7]:  1  | RAM[7]:  1 |
; RAM[8]:  4  | RAM[8]:  4 -
; ------------------------------------

PREPARANDO:
    leaw $0, %A
    movw $0, (%A) ; ram[0] = 0

    leaw $1, %A
    movw $0, (%A); ram[1] = 0


    leaw $4, %A
    movw (%A), %D
    leaw $6, %A
    movw %D, (%A) ; ram[6] = tamnho do vetor (vai ser usado na media)

    leaw $4, %A
    movw %A, %D
    leaw $2, %A ; ram[2] = comeco -1 do vetor
    movw %D, (%A)

WHILE: ;while geral

    leaw $2, %A
    addw (%A), 1, %D ;
    movw %D, (%A) ;adc 1 em ram[2] pra ter endereco da prox memoria 

    movw %D, %A
    movw (%A), %D
    leaw $1, %A
    addw (%A), %D, %D
    movw %D, (%A) ;peguei o endereco atual da memoria do vetor q trabalhando e somei no geral

MULT:
    leaw $2, %A
    movw (%A), %A
    movw (%A), %D ; sla o valor da ram[5]

    leaw $ENDMULT, %A
    je
    nop

    leaw $2, %A
    movw (%A), %A
    movw (%A), %D ; sla o valor da ram[5]
    leaw $0, %A
    addw (%A), %D, %D
    movw %D, (%A)

    leaw $2, %A
    movw (%A), %A
    subw (%A), $1, %D
    movw %D, (%A)

    leaw $MULT, %A
    jmp
    nop

ENDMULT:

    leaw $4, %A
    movw (%A), %D
    subw %D, 1, %D
    movw %D, (%A) ; subtrai 1 da ram[4] e ve se 0 (ja foi todo tamanho), se n foi continua loop
    leaw $END, %A
    je 
    nop

DIVWHILE: ;div faz de 0 e 6 guardando em 7

    leaw $0, %A
    movw (%A), %D

    leaw $DIVEND, %A 
    jle
    nop

    leaw $6, %A 
    movw (%A), %D 
    leaw $0, %A 
    subw (%A), %D, %D  
    movw %D, (%A) 

    leaw $DIVEND, %A 
    jl
    nop

    leaw $7, %A
    addw $1, (%A), %D 
    movw %D, (%A)

    leaw $DIVWHILE, %A 
    jmp
    nop

DIVEND:
    leaw $7, %A
    movw (%A), %D
    leaw $0, %A
    movw %D, (%A); arrumando cagada da div
END:
    
