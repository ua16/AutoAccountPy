#!/usr/bin/env python3

from rich import print as rprint
from rich.console import Console
from rich.table import Table


from sys import argv

console = Console()
console.colorsystem = "truecolor"

empty_entry = [" ", " " , " ", " "]

def return_larger(a,b):
    if a==b:
        return a
    if a>b:
        return a
    if b>a:
        return b
    

class Ledger():
    def __init__(self,name):
        self.name = name
        self.debit = []
        self.credit = []
        self.table = Table(title=name)

        self.table.add_column("Date - Dr")
        self.table.add_column("To -Dr")
        self.table.add_column("Descripton - Dr")
        self.table.add_column("Amount - Dr")
        self.table.add_column("Date - Cr")
        self.table.add_column("To -Cr")
        self.table.add_column("Descripton - Cr")
        self.table.add_column("Amount - Cr")

    def add_debit(self,entry):
        self.debit.append(entry)
 
    def add_credit(self, entry):
        self.credit.append(entry)       

    def create_final_table(self):
        max_size = return_larger(len(self.debit), len(self.credit)) 
        final_out = []
        for i in range(0,max_size):
            debit_there = True
            credit_there = True
            try:
               b = self.debit[i]
            except IndexError:
                debit_there = False
            try:
                b = self.credit[i]
            except IndexError:
                credit_there = False
  
            if debit_there == True and credit_there == True:
                final_out.append(self.debit[i] + self.credit[i])
            elif debit_there == True and credit_there == False:
                final_out.append(self.debit[i] + empty_entry)
            elif  credit_there == True and debit_there == False:
                final_out.append(empty_entry + self.credit[i])
        for i in final_out:
            self.table.add_row(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
        console.print(self.table)
        return final_out

          
def parse_string(string):
    out = string.split(":")
    return out

file_name = argv[1]
accounts = {} 

f = open(file_name, "r")
data = f.readlines()
f.close()

for line in data:
    if line.startswith("#"):
        continue
    else:
        current_line = parse_string(line)
        if current_line[1] not in accounts:
            accounts.update({current_line[1]:Ledger(current_line[1])})
        if current_line[2] not in accounts:
            accounts.update({current_line[2]:Ledger(current_line[2])})

        accounts[current_line[1]].add_debit([current_line[0],current_line[2],current_line[4],current_line[3]])
        accounts[current_line[2]].add_credit([current_line[0],current_line[1],current_line[4],current_line[3]])


for i in accounts:
    accounts[i].create_final_table()
    console.rule(":)")
