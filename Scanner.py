#!/usr/bin/env python3
#

import sys

class Scanner():
    def __init__(self, input_ = ''):
        #{--------------------------------------------------------------}
        #{ python class defaults }
        self.input_ = input_
        self.LookGenerator = self.SetLook()
        self.nextGenerator = self.SetNext()
        #{--------------------------------------------------------------}
        #{ Constant Declarations }
        self.TAB = '\t'
        self.LF  = '\n'
        self.CR  = '\r'
        self.verbous = False
        #self.verbous = True
        #{--------------------------------------------------------------}
        #{ Variable Declarations }
        #{ Lookahead Character }
        self.Look = ''
        self.Token = ''
        self.Value = ''
        self.TokenList = []
        self.ValueList = []
        #{--------------------------------------------------------------}
        #{ Type Declarations }
        self.KWlist = ['IF', 'ELSE', 'ENDIF', 'END']
        self.SymType = dict(enumerate( ['IfSym', 'ElseSym', 'EndifSym', 'EndSym', 'Ident', 'Number', 'Operator']))
        #{--------------------------------------------------------------}
        #{ Initialize }
        if self.input_ != '':
            self.GetChar()
    #{--------------------------------------------------------------}
    #{ Read New Character From Input Stream }
    def SetLook(self):
        if self.verbous: print('SetLook: Look = {0}'.format(self.Look))
        for char in self.input_:
            yield char

    #{--------------------------------------------------------------}
    #{ Read New Character From Input Stream }
    def SetNext(self):
        for Token, Value in zip(self.TokenList, self.ValueList):
            yield Token, Value 
    #{--------------------------------------------------------------}
    #{ Read New Character From Input Stream }
    def GetChar(self):
        try:
            self.Look = self.LookGenerator.__next__()
        except StopIteration:
            self.Look = ''
        if self.verbous: print('GetChar: Look = {0}'.format(self.Look))
        return
   #{--------------------------------------------------------------}
    #{ Report an Error }
    def Error(self, string):
        if self.verbous: print('Syntax Error: Look = {0}'.format(self.Look))
        string = ''.join(['Syntax Error: ', string, '.'])
        print(string)
        return
    #{--------------------------------------------------------------}
    #{ Report Error and Halt }
    def Abort(self, string):
        if self.verbous: print('Abort: Look = {0}'.format(self.Look))
        self.Error(string)
        sys.exit()
        return
    #{--------------------------------------------------------------}
    #{ Report What Was Expected }
    def Expected(self, string):
        if self.verbous: print('Expected: Look = {0}'.format(self.Look))
        string = '{0} Expected'.format(string)
        self.Abort(string)
        return
    #{--------------------------------------------------------------}
    #{ Recognize an Alpha Character }
    def IsAlpha(self, char):
        return char.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not char == '' # return bool
    #{--------------------------------------------------------------}
    #{ Recognize a Decimal Digit }
    def IsDigit(self, char):
        return char in '0123456789.' and not char == '' # return bool
    #{--------------------------------------------------------------}
    #{ Get an Identifier }
    def GetName(self):
        self.Value = ''
        if self.verbous: print('GetName: Look = {0}'.format(self.Look))
        if not self.IsAlpha(self.Look):
            self.Expected('Name')
        while self.IsAlNum(self.Look):
            self.Value = self.Value + self.Look
            self.GetChar()
        k = self.Lookup(self.Value)
        if k == None:
            self.Token = 'Ident'
        else:
            self.Token = self.SymType[k]
        return 
    #{--------------------------------------------------------------}
    #{ Get a Number }
    def GetNum(self):
        if self.verbous: print('GetNum: Look = {0}'.format(self.Look))
        GetNumString = ''
        if not self.IsDigit(self.Look):
            self.Expected('Integer')
        while self.IsDigit(self.Look): 
            GetNumString = GetNumString+self.Look
            self.GetChar()
        if self.verbous: print('GetNum: GetNumString = {0}'.format(GetNumString))
        self.Value = GetNumString
        self.Token = 'Number'
        
        return 
    #{--------------------------------------------------------------}
    #{ Lexical Scanner }
    def ScanLine(self, Line):
        self.Look = ''
        self.Token = ''
        self.Value = ''
        self.TokenList = []
        self.ValueList = []
        self.input_ = ''.join(Line.split())
        self.LookGenerator = self.SetLook()
        self.GetChar()
        
        while self.Token != 'EndSym':
            self.Scan()
            
            self.TokenList.append(self.Token)
            self.ValueList.append(self.Value)
        if self.verbous: print(self.TokenList)
        if self.verbous: print(self.ValueList)
        
        self.nextGenerator = self.SetNext()
        return
    #{--------------------------------------------------------------}
    #{ Lexical Scanner }
    def Scan(self):
        if self.verbous: print('Scan: Look = {0}'.format(self.Look))
        if self.Look == '':
            self.Value = 'End'
            self.Token = 'EndSym'
        elif self.IsAlpha(self.Look):
            self.GetName()
        elif self.IsDigit(self.Look):
            self.GetNum()
        elif self.IsOp(self.Look):
            self.GetOp()
        else:
            self.Value = self.Look
            self.Token = 'Operator'
            self.GetChar()
        return
    #{---------------------------------------------------------------}
    #{ Recognize Any Operator }
    def IsOp(self, char):
        return char in ['+', '-', '*', '/', '<', '>', ':', '=']
    #{--------------------------------------------------------------}
    #{ Get an Operator }
    def GetOp(self):
        self.Value = ''
        if not self.IsOp(self.Look):
            self.Expected('Operator')
        while self.IsOp(self.Look):
            self.Value = self.Value + self.Look
            self.GetChar()
            if self.Value == '=':
                if self.Look not in ['<', '>', '=']:
                    self.Token = 'Operator'
                    return
        self.Token = 'Operator'
        
        return
    #{--------------------------------------------------------------}
    def IsAddop(self, char):
        if self.verbous: print('IsAddop: Look = {0}'.format(self.Look))
        return char in ['+', '-']
    #{--------------------------------------------------------------}
    #{ Recognize an Alphanumeric Character }
    def IsAlNum(self, char): 
        return self.IsAlpha(char) or self.IsDigit(char)
    #{--------------------------------------------------------------}
    #{ Skip Over a Comma }
    #def SkipComma(self):
        #if self.Look == ',':
            #self.GetChar()
        #return
    #{--------------------------------------------------------------}
    #{ Table Lookup }
    #{ If the input string matches a table entry, return the entry index. If not, return a zero. }
    def Lookup(self, string):
        if self.verbous: print('Lookup: Look = {0}'.format(self.Look))
        if self.verbous: print('Lookup: string = {0}'.format(string))
        try:
            return self.KWlist.index(string.upper())
        except ValueError:
            return None
    #{--------------------------------------------------------------}



#{ Main Program }
if __name__ == '__main__':
    string  = '''11+2**2+123\t12 3+Aloa''' 
    scanner = Scanner()
    scanner.ScanLine(string)
    scanner.ScanLine('a=        2\t+\r1')
    scanner.ScanLine('a=        2\t+(\r1*3)')
    scanner.ScanLine('-12\t+(\r1*3)')
    scanner.ScanLine('')
        
    sys.exit()
#{--------------------------------------------------------------}
