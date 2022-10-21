; Arquivo: LCDQuadrado.nasm
; Curso: Elementos de Sistemas
; Criado por: Rafael Corsi
; Data: 28/3/2018
;
; Desenhe uma linha no LCD

PREPARANDO:
    leaw $18, %A
    movw %A, %D
    leaw $0, %A
    movw %D, (%A); ram[0] = 18

    leaw $16384, %A
    movw %A, %D
    leaw $1, %A
    movw %D, (%A); ram[1] = 16384
    
WHILE:
    leaw $1, %A
    movw (%A), %D
    leaw %D, %A
    movw $0, %D
    notw %D
    movw %D, (%A)

    leaw $0, %A
    movw (%A), %D
    subw 1,%D,%D
    movw %D, (%A)

    leaw $END, %A
    je
    nop

    leaw $1, %A
    movw (%A), %D
    assw 1, %D, %D
    movw %D, (%A)

    leaw $WHILE, %A
    jmp
    nop

END:

