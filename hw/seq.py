#!/usr/bin/env python3

from myhdl import *
from .components import *


@block
def ram(dout, din, addr, we, clk, rst, width, depth):
    loads = [Signal(bool(0)) for i in range(depth)]
    outputs = [Signal(modbv(0)[width:]) for i in range(depth)]
    registersList = [None for i in range(depth)]

    @always_comb
    def comb():
        pass

    return instances()


@block
def pc(increment, load, i, output, width, clk, rst):
    regIn = Signal(modbv(0)[width:])
    regOut = Signal(modbv(0)[width:])
    regLoad = Signal(bool(0))
    incOut = Signal(modbv(0)[width:])
    mux1_out,mux2_out = [Signal(modbv(0)[width:]) for _ in range(2)]
    
    
    incre_1 = inc(regOut,incOut)
    mx1 = mux2way(mux1_out, False, incOut, increment)
    mx2 = mux2way(mux2_out, mux1_out, i, load)
    mx3 = mux2way(regIn, mux2_out, False, rst)
    reg1 = registerN(regIn,regLoad,regOut,width,clk,rst)

    @always_comb
    def comb():
        regLoad.next = rst or increment or load
        output.next = regOut

    return instances()


@block
def registerN(i, load, output, width, clk, rst):
    binaryDigitList = [None for n in range(width)]
    output_n = [Signal(bool(0)) for n in range(width)]

    for y in range(width):
        binaryDigitList[i] = binaryDigit(i[y],load,output_n[i],clk,rst)

    @always_comb
    def comb():
        for n in range(width):
            output.next[n] = output_n[n]

    return instances()

@block
def register8(i, load, output, clk, rst):
    binaryDigitList = [None for n in range(8)]
    output_n = [Signal(bool(0)) for n in range(8)]

    for j in range(8):
        binaryDigitList[j] = binaryDigit(i(j),load,output_n[j],clk,rst)

    @always_comb
    def comb():
        for p in range(8):
            output.next[p] = output_n[p]
    return instances()

@block
def binaryDigit(i, load, output, clk, rst):
    q, d, clear, presset = [Signal(bool(0)) for i in range(4)]

    mux = mux2way(q, d, i, load)
    theDff = dff(d, q, clear, presset, clk, rst)

    @always_comb
    def comb():
        output.next = d

    return instances()


@block
def dff(q, d, clear, presset, clk, rst):
    @always_seq(clk.posedge, reset=rst)
    def logic():
        if clear:
            q.next = 0
        elif presset:
            q.next = 1
        else:
            q.next = d

    return instances()
