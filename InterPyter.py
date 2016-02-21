#!/usr/bin/env python3
#

import sys
import numpy as np

from Scanner import Scanner
class InterPyter():
    def __init__(self, input_ = ''):
        #{--------------------------------------------------------------}
        #{ python class defaults }
        self.scanner = Scanner()
        self.scanner.ScanLine(input_)
        #{--------------------------------------------------------------}
        #{ Constant Declarations }
        self.verbous = False
        self.verbous = True
        #{--------------------------------------------------------------}
        #{ Variable Declarations }
        #{ Lookahead Character }
        self.nextToken = ''
        self.nextValue = ''
        #{--------------------------------------------------------------}
        #{ Initialize the Variable Area }
        self.Table = {}
        #{--------------------------------------------------------------}
        #{ Initialize }
        if input_ != '':
            self.GetNext()
    #{--------------------------------------------------------------}
    #{ Read New Character From Input Stream }
    def GetNext(self):
        try:
            self.nextToken, self.nextValue = self.scanner.nextGenerator.__next__()
        except StopIteration:
            self.nextToken, self.nextValue = 'EndSym', 'End'
        if self.verbous: print('GetNext: nextValue = {0}'.format(self.nextValue))
        return
            
   #{--------------------------------------------------------------}
    #{ Report an Error }
    def Error(self, string):
        if self.verbous: print('Error: Look = {0}'.format(self.nextValue))
        string = ''.join(['Error: ', string, '.'])
        print(string)
        return
    #{--------------------------------------------------------------}
    #{ Report Error and Halt }
    def Abort(self, string):
        if self.verbous: print('Abort: Look = {0}'.format(self.nextValue))
        self.Error(string)
        sys.exit()
        return
    #{--------------------------------------------------------------}
    #{ Report What Was Expected }
    def Expected(self, string):
        if self.verbous: print('Expected: Look = {0}'.format(self.nextValue))
        string = '{0} Expected'.format(string)
        self.Abort(string)
        return
    #{--------------------------------------------------------------}
    #{ Match a Specific Input Character }
    def Match(self, string):
        if self.verbous: print('Match: Look = {0}'.format(self.nextValue))
        if self.nextValue == string: 
            self.GetNext()
        else: 
            string = ' {0} '.format(string)
            self.Expected(string)
        return
    #{--------------------------------------------------------------}
    #{ Get an Identifier }
    def GetName(self):
        if self.verbous: print('GetName: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        if self.nextToken != 'Ident':
            self.Expected('Identifyer')
        GetName = self.nextValue
        self.GetNext()
        return GetName
    #{--------------------------------------------------------------}
    #{ Get a Number }
    def GetNum(self):
        if self.verbous: print('GetNum: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        GetNumString = ''
        if self.nextToken != 'Number':
            self.Expected('Number')
        GetNumString = self.nextValue
        self.GetNext()
        return float(GetNumString)
    #{---------------------------------------------------------------}
    #{--------------------------------------------------------------}
    def IsAddop(self, char):
        if self.verbous: print('IsAddop: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        return char in ['+', '-']
    #{---------------------------------------------------------------}
    #{ Parse and Translate an Expression }
    #
    # <expression> ::= <term> [<addop> <term>]*
    #
    def Expression(self):
        if self.verbous: print('Expression: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        Value = self.Term()
        while self.IsAddop(self.nextValue):
            if self.nextValue == '+':
                self.Match('+')
                Value = Value + self.Term()
            elif self.nextValue == '-':
                self.Match('-')
                Value = Value - self.Term()
        return Value
    #{--------------------------------------------------------------}
    #{---------------------------------------------------------------}
    #{ Parse and Translate a Math Term }
    #
    # <term> ::= <factor> [ <mulop> <factor> ]*
    #
    def Term(self):
        if self.verbous: print('Term: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        Value = self.SignedFactor()
        while self.nextValue in ['*', '/', '**']:
            if self.nextValue == '*':
                self.Match('*')
                Value = Value * self.Factor()
            elif self.nextValue == '/':
                self.Match('/')
                Value = Value / self.Factor()
            elif self.nextValue == '**':
                self.Match('**')
                Value = Value**self.Factor()
        return Value
    #{---------------------------------------------------------------}
    #{ Parse and Translate the First Math Factor }
    #
    # <signed factor> ::= [<addop>] <factor>
    #
    def SignedFactor(self):
        if self.verbous: print('SignedFactor: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        if self.nextValue == '+':
            self.GetNext()
        if self.nextValue == '-':
            self.GetNext()
            if self.nextToken == 'Number':
                Value = -1 * self.GetNum()
            else:
                Value = -1 * self.Factor()
        else:
            Value = self.Factor()
        return Value
    #{--------------------------------------------------------------}
    #{---------------------------------------------------------------}
    #{ Parse and Translate an Identifier }
    def Ident(self):
        if self.verbous: print('Ident: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        Name = self.GetName()
        if self.nextValue == '(':
            self.Match('(')
            Ident = self.Expression()
            self.Match(')')
            if Name.lower() == 'cos':
                Ident = np.cos(Ident)
            elif Name.lower() == 'sin':
                Ident = np.sin(Ident)
            elif Name.lower() == 'tan':
                Ident = np.tan(Ident)
            else:
                self.Abort('unknown function call: {0}'.format(Name))
              
        else:
            Ident = self.Table[ Name ]
        
        if self.verbous: print('Ident = {0}'.format(Ident))
        return Ident
    #{---------------------------------------------------------------}
    #{ Parse and Translate a Math Factor }
    #
    # <factor> ::= <number> | (<expression>) | <variable>
    #
    def Factor(self):
        if self.verbous: print('Factor: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        if self.nextValue == '(':
            self.Match('(')
            Factor = self.Expression()
            self.Match(')')
        elif self.nextToken == 'Ident':
            Factor = self.Ident()
            #Factor = self.Table[ self.GetName() ]
        else:
            Factor = self.GetNum()
        return Factor
    #{---------------------------------------------------------------}
    #{--------------------------------------------------------------}
    #{ Parse and Translate an Assignment Statement }
    #
    # <assignment> ::= <ident> = <expression>
    #
    def Assignment(self):
        if self.verbous: print('Assignment: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        Name = self.GetName()
        self.Match('=')
        result = self.Expression()
        self.Table[Name] = result
        #print ('{0} = {1}'.format(Name, result))
        return
    #{--------------------------------------------------------------}
    #{--------------------------------------------------------------}
    #{ Recognize and Skip Over a Newline }
    def NewLine(self):
        if self.verbous: print('NewLine: Look = {0}'.format(self.nextValue))
        if self.nextValue == self.CR:
            self.GetNext()
        if self.nextValue == self.LF:
            self.GetNext()
        return
    #{--------------------------------------------------------------}
    #{--------------------------------------------------------------}
    #{ Lexical Scanner }
    def evalLine(self, Line):
        self.scanner.ScanLine(Line)
        self.GetNext()
        if self.verbous: print('evalLine: nextValue = {0}'.format(self.nextValue), end='\t')
        if self.verbous: print('nextToken = {0}'.format(self.nextToken))
        
        if '=' in self.scanner.ValueList:
            self.Assignment()
        else:
            print (self.Expression())
            
        return
    #{---------------------------------------------------------------}

#{ Main Program }
if __name__ == '__main__':
    interPyter = InterPyter()
    exit = False
    while not exit:
        name = input(">>> ") 
        if name == 'exit()':
            exit = True
        else:
            interPyter.evalLine(name)
    sys.exit()
#{--------------------------------------------------------------}
