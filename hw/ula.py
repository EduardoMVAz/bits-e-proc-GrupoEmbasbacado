#!/usr/bin/env python3

from myhdl import *


@block
def ula(x, y, c, zr, ng, saida, width=16):

    zx_out = Signal(modbv(0)[width:])
    nx_out = Signal(modbv(0)[width:])
    zy_out = Signal(modbv(0)[width:])
    ny_out = Signal(modbv(0)[width:])
    and_out = Signal(modbv(0)[width:])
    add_out = Signal(modbv(0)[width:])
    mux_out = Signal(modbv(0)[width:])
    no_out = Signal(modbv(0)[width:])
    comp_zr_out = Signal(modbv(0)[width:])
    comp_ng_out = Signal(modbv(0)[width:])

    c_zx = c(5)
    c_nx = c(4)
    c_zy = c(3)
    c_ny = c(2)
    c_f = c(1)
    c_no = c(0)

    z1 = zerador(c_zx,x,zx_out)
    z2 = zerador(c_zy,y,zy_out)
    n1 = inversor(c_nx,zx_out,nx_out)
    n2 = inversor(c_ny,zy_out,ny_out)

    a2 = add(ny_out,nx_out,add_out)
    # m = mux2way(mux_out,and_out,add_out,c_f)
    i = inversor(c_no,mux_out, no_out)

    c = comparador(no_out,comp_zr_out,comp_ng_out,width)

    @always_comb
    def comb():


        and_out = ny_out & nx_out
        if int(c_f) == 0:
            mux_out.next = (ny_out & nx_out)
        else:
            mux_out.next = add_out

        saida.next = no_out
        zr.next = comp_zr_out
        ng.next = comp_ng_out
        print(bin(no_out, 16))
        print(bin(comp_zr_out, 1))
        print(bin(comp_ng_out, 1))



    return instances()


# -z faz complemento de dois
# ~z inverte bit a bit
@block
def inversor(z, a, y):
    @always_comb
    def comb():
        if z == 0:
            a.next = y
        else:
            a.next = ~y
    return instances()


@block
def comparador(a, zr, ng, width):
    # width insica o tamanho do vetor a
    @always_comb
    def comb():
        if(a == 0):
            zr.next = 1
        else:
            zr.next = 0

        if (a[0] == 1):
            ng.next = 1
        else:
            ng.next = 0
    return instances()


@block
def zerador(z, a, y):
    @always_comb
    def comb():
        pass

    return instances()


@block
def add(a, b, q):
    @always_comb
    def comb():
        pass

    return instances()


@block
def inc(a, q):
    @always_comb
    def comb():
        pass

    return instances()


# ----------------------------------------------
# Conceito B
# ----------------------------------------------


@block
def halfAdder(a, b, soma, carry):
    s = Signal(bool())
    c = Signal(bool())

    @always_comb
    def comb():
        s = a ^ b
        c = a & b

        soma.next = s
        carry.next = c

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(3)]
    haList = [None for i in range(2)]

    haList[0] = halfAdder(a, b, s[0], s[1])  # 2
    haList[1] = halfAdder(c, s[0], soma, s[2])  # 3

    @always_comb
    def comb():
        carry.next = s[1] | s[2]  # 4

    return instances()


@block
def addcla4(a, b, q):
    @always_comb
    def comb():
        pass

    return instances()


@block
def addcla16(a, b, q):
    @always_comb
    def comb():
        pass

    return instances()


# ----------------------------------------------
# Conceito A
# ----------------------------------------------


@block
def ula_new(x, y, c, zr, ng, sr, sf, bcd, saida, width=16):
    pass


@block
def bcdAdder(x, y, z):
    pass
