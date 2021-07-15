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
    """ 
This is the class for each account thing
use __init__ and pass the name all instances of it are stored
in the global dictionary accounts. Tables are added automatically
You just have to call the methods asociated with this class
add_debit add_credit and create_final table.
Do it in form [Date, Account to debit, Description, Amount]
"""
    def __init__(self,name):
        self.name = name
        self.debit = []
        self.credit = []
        self.table = Table(title=name)

        self.total_debit = 0
        self.total_credit = 0

        self.final_total = 0

        self.balance = 0

        self.table.add_column("Date - Dr")
        self.table.add_column("To -Dr")
        self.table.add_column("Descripton - Dr")
        self.table.add_column("Amount - Dr")
        self.table.add_column("Date - Cr")
        self.table.add_column("To -Cr")
        self.table.add_column("Descripton - Cr")
        self.table.add_column("Amount - Cr")

    def add_debit(self,entry):
        """ Do it in form [Date, Account to credit, Description, Amount"""
        self.total_debit += int(entry[3])
        self.debit.append(entry)
 
    def add_credit(self, entry):
        """ Do it in form [Date, Account to debit, Description, Amount"""
        self.total_credit += int(entry[3])
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
        if self.total_credit > self.total_debit:
            self.table.add_row(" ", " ", "Balance c/d", str(self.total_credit - self.total_debit) ," ", " ", " ", " ", style="red")
            self.table.add_row(" ", " ", "Total", str(self.total_credit), " "," ", "Total", str(self.total_credit), style="red")
            self.final_total = self.total_credit
            self.balance = self.total_credit - self.total_debit
            self.table.add_row(" " , " ", " " , " " , " " , "Balance b/d", str(self.balance), style="red")
        else:
            self.table.add_row(" ", " ", " ", " ", " ", " ", "Balance c/d", str(self.total_debit - self.total_credit) , style="green")
            self.table.add_row(" ", " ", "Total", str(self.total_debit), " "," ", "Total", str(self.total_debit), style="green")
            self.final_total = self.total_debit
            self.balance = self.total_debit - self.total_credit
            self.table.add_row(" " , " "  , "Balance b/d", str(self.balance), " " , " " , " " , " ", style="green")


        console.print(self.table)
        return final_out

          
def parse_string(string):
    out = string.split(":")
    return out

file_name = argv[-1]
accounts = {} 

f = open(file_name, "r")
data = f.readlines()
f.close()

for line in data:
    # Basically this part is ok
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
    # This part is ok too
    accounts[i].create_final_table()
    console.rule(":)")


trial_balance = Table(title="Trial Balance")
trial_balance.add_column("Account")
trial_balance.add_column("Debit", style="green")
trial_balance.add_column("Credit", style="red")

credit_total = 0
debit_total = 0

for i in accounts:
    if accounts[i].total_credit > accounts[i].total_debit:
        trial_balance.add_row(accounts[i].name, " " , str(accounts[i].balance))
        credit_total += accounts[i].balance
    else:
        trial_balance.add_row(accounts[i].name, str(accounts[i].balance), " ", style="green")
        debit_total += accounts[i].balance

trial_balance.add_row("total", str(debit_total), str(credit_total))

console.print(trial_balance)
