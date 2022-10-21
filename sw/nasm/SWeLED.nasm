; Arquivo: SWeLED.nasm
; Curso: Elementos de Sistemas
; Criado por: Rafael Corsi
; Data: 28/3/2018
;
; Faça os LEDs exibirem                8     4     2   
; LED = 0 0 0 0 0 0 0 ON ON ON ON ON !SW3 !SW2 !SW1 0

leaw $496, %A
movw %A, %D
leaw $0, %A
movw %D, (%A)

SW1:
    leaw $21185, %A
    movw (%A), %D
    leaw $2, %A
    andw %D, %A, %D

    leaw $SW2, %A
    jg
    nop

    leaw $0, %A ; aqui eu somei 2 
    movw (%A), %D
    leaw $2, %A
    addw %D, %A, %D
    leaw $0, %A
    movw %D, (%A)

SW2:
    leaw $21185, %A
    movw (%A), %D
    leaw $4, %A
    andw %D, %A, %D

    leaw $SW3, %A
    jg
    nop

    leaw $0, %A ; aqui eu somei 4
    movw (%A), %D
    leaw $4, %A
    addw %D, %A, %D
    leaw $0, %A
    movw %D, (%A)

SW3:
    leaw $21185, %A
    movw (%A), %D
    leaw $8, %A
    andw %D, %A, %D

    leaw $END, %A
    jg
    nop

    leaw $0, %A ; aqui eu somei 8
    movw (%A), %D
    leaw $8, %A
    addw %D, %A, %D
    leaw $0, %A
    movw %D, (%A)

END:
leaw $0, %A
movw (%A), %D
leaw $21184, %A
movw %D, (%A)






