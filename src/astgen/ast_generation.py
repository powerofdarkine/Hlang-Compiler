"""
AST Generation module for HLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.HLangVisitor import HLangVisitor
from build.HLangParser import HLangParser
from src.utils.nodes import *


class ASTGeneration(HLangVisitor):
    def visitProgram(self, ctx: HLangParser.ProgramContext):
        dec,func1=self.visit(ctx.dec())
        func2=self.visit(ctx.res())
        return Program(dec,func1 + func2)
    def visitArray(self, ctx:HLangParser.ArrayContext):
        if ctx.ele():
            first=self.visit(ctx.ele())
            rest=self.visit(ctx.elelist())
            return ArrayLiteral([first]+rest)
        else:
            return ArrayLiteral([])
    def visitEle(self, ctx:HLangParser.EleContext):
        if ctx.INTLIT():
            return IntegerLiteral(int(ctx.INTLIT().getText()))
        if ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        if ctx.TRUE():
            return BooleanLiteral(True)
        if ctx.FALSE():
            return BooleanLiteral(False)
        if ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        if ctx.array():
            return self.visit(ctx.array())
    def visitElelist(self, ctx:HLangParser.ElelistContext):
        if ctx.getChildCount()==3:
            return [self.visit(ctx.ele())] + self.visit(ctx.elelist())
        else:
            return []
    def visitRes(self, ctx:HLangParser.ResContext):
        if ctx.getChildCount()==2:
            return [self.visit(ctx.func())] + self.visit(ctx.res())
        else:
            return []
    def visitDec(self, ctx:HLangParser.DecContext):
        cons=[self.visit(v) for v in ctx.const()]
        func=[self.visit(v) for v in ctx.funcd()]
        return cons, func
    def visitConst(self, ctx:HLangParser.ConstContext):
        name = ctx.ID().getText()
        opt=self.visit(ctx.opt()) if ctx.opt() else None
        exp=self.visit(ctx.exp())
        return  ConstDecl(name,opt,exp)
    def visitFuncd(self, ctx: HLangParser.FuncdContext):
        if ctx.mtype():
            typ=self.visit(ctx.mtype())
        elif ctx.arr():
            typ=self.visit(ctx.arr())
        else:
            typ=VoidType()
        return FuncDecl(ctx.ID().getText(),self.visit(ctx.para()),typ,self.visit(ctx.body()))
    def visitPara(self, ctx: HLangParser.ParaContext):
        if ctx.getChildCount() == 0:
            return []
        else:
            name = ctx.ID().getText()
            typ = self.visit(ctx.mtype())
            tail = self.visit(ctx.paralst())
            return [Param(name, typ)] + tail

    def visitParalst(self, ctx: HLangParser.ParalstContext):
        if ctx.getChildCount() == 0:
            return []
    
        name = ctx.ID().getText()

    # Determine whether mtype or arr exists
        typ = self.visit(ctx.mtype()) if ctx.mtype() else self.visit(ctx.arr())

        tail = self.visit(ctx.paralst()) if ctx.paralst() else []

        return [Param(name, typ)] + tail


    def visitMtype(self, ctx: HLangParser.MtypeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOL():
            return BoolType()
        elif ctx.STRING():
            return StringType()
    def visitBody(self, ctx: HLangParser.BodyContext):
        return self.visit(ctx.inside())
    def visitInside(self, ctx: HLangParser.InsideContext):
        if ctx.getChildCount()==2:
            return [self.visit(ctx.stat())]+ self.visit(ctx.inside())
        else:
            return []
    def visitStat(self, ctx: HLangParser.StatContext):
        if ctx.var():
            return self.visit(ctx.var())
        elif ctx.assign():
            return self.visit(ctx.assign())
        elif ctx.condition():
            return self.visit(ctx.condition())
        elif ctx.loop():
            return self.visit(ctx.loop())
        elif ctx.body():
            return BlockStmt(self.visit(ctx.body()))
        elif ctx.smallstate():
            return self.visit(ctx.smallstate())
        elif ctx.exp():
            return ExprStmt(self.visit(ctx.exp()))
    def visitVar(self, ctx: HLangParser.VarContext):
        name = ctx.ID().getText()
        opt=self.visit(ctx.opt()) if ctx.opt() else None
        exp=self.visit(ctx.exp())
        return  VarDecl(name,opt,exp)
    def visitAssign(self, ctx: HLangParser.AssignContext):
        id=ctx.ID().getText()
        para=self.visit(ctx.asspara())
        if para == []:
            return Assignment(IdLValue(id),self.visit(ctx.exp()))
        elif len(para)==1:
            return Assignment(ArrayAccessLValue(Identifier(id),para[0]),self.visit(ctx.exp()))
        else:
            return Assignment(ArrayAccessLValue(reduce(lambda x,y: ArrayAccess(x,y) ,para[:-1],Identifier(id)),para[-1]),self.visit(ctx.exp()))
        # return Assignment(IdLValue(id) if para ==[]  ArrayAccessLValue(reduce(lambda x,y: ArrayAccess(x,y) ,para[:-1],Identifier(id)),para[-1]) ,self.visit(ctx.exp()))
    def visitAsspara(self, ctx: HLangParser.AssparaContext):
        if ctx.getChildCount()==0:
            return []
        else:
            return [self.visit(ctx.exp())] + self.visit(ctx.asspara())
        
    def visitCondition(self, ctx: HLangParser.ConditionContext):
        cond=self.visit(ctx.cond())
        return IfStmt(self.visit(ctx.exp()),BlockStmt(self.visit(ctx.body(0))),cond[:-1] if cond!= [[]] else [],BlockStmt(self.visit(ctx.body(1))) if ctx.ELSE() else [])
    def visitCond(self, ctx: HLangParser.CondContext):
        if ctx.getChildCount()==0:
            return [[]]
        else:
            return [(self.visit(ctx.exp()),BlockStmt(self.visit(ctx.body())))] + self.visit(ctx.cond())
    def visitLoop(self, ctx: HLangParser.LoopContext):
        if ctx.WHILE():
            return WhileStmt(self.visit(ctx.exp()),BlockStmt(self.visit(ctx.body())))
        else:
            return ForStmt(ctx.ID().getText(),self.visit(ctx.exp()),BlockStmt(self.visit(ctx.body())))
    def visitSmallstate(self, ctx: HLangParser.SmallstateContext):
        if ctx.RETURN():
            return ReturnStmt(self.visit(ctx.exp()) if ctx.exp() else None)
        if ctx.CONTINUE():
            return ContinueStmt()
        else:
            return BreakStmt()
    def visitExp(self, ctx: HLangParser.ExpContext):
        if ctx.getChildCount()==3:
            return BinaryOp(self.visit(ctx.exp()),ctx.PIPE().getText(),self.visit(ctx.exp0()))
        else:
            return self.visit(ctx.exp0())
    def visitExp0(self, ctx: HLangParser.Exp0Context):
        if ctx.getChildCount()==3:
            return BinaryOp(self.visit(ctx.exp0()),ctx.OR().getText(),self.visit(ctx.exp1()))
        else:
            return self.visit(ctx.exp1())
    def visitExp1(self, ctx: HLangParser.Exp1Context):
        if ctx.getChildCount()==3:
            return BinaryOp(self.visit(ctx.exp1()),ctx.AND(),self.visit(ctx.exp2()))
        else:
            return self.visit(ctx.exp2())
    def visitExp2(self, ctx: HLangParser.Exp1Context):
        if ctx.getChildCount()==1:
            return self.visit(ctx.exp3())
        left=self.visit(ctx.exp2())
        right=self.visit(ctx.exp3())
        if ctx.EQ():
            return BinaryOp(left,ctx.EQ().getText(),right)
        else:
            return BinaryOp(left,ctx.NEQ().getText(),right)
    def visitExp3(self, ctx: HLangParser.Exp1Context):
        if ctx.getChildCount()==1:
            return self.visit(ctx.exp4())
        left=self.visit(ctx.exp3())
        right=self.visit(ctx.exp4())
        if ctx.LT():
            return BinaryOp(left,ctx.LT().getText(),right)
        if ctx.LE():
            return BinaryOp(left,ctx.LE().getText(),right)
        if ctx.GT():
            return BinaryOp(left,ctx.GT().getText(),right)
        else:
            return BinaryOp(left,ctx.GE().getText(),right)
    def visitExp4(self, ctx: HLangParser.Exp1Context):
        if ctx.getChildCount()==1:
            return self.visit(ctx.exp5())
        left=self.visit(ctx.exp4())
        right=self.visit(ctx.exp5())
        if ctx.ADD():
            return BinaryOp(left,ctx.ADD().getText(),right)
        else: 
            return BinaryOp(left,ctx.SUB().getText(),right)
    def visitExp5(self, ctx: HLangParser.Exp1Context):
        if ctx.getChildCount()==1:
            return self.visit(ctx.exp6())
        left=self.visit(ctx.exp5())
        right=self.visit(ctx.exp6())
        if ctx.MUL():
            return BinaryOp(left,ctx.MUL().getText(),right)
        if ctx.DIV():
            return BinaryOp(left,ctx.DIV().getText(),right)
        else:
            return BinaryOp(left,ctx.MOD().getText(),right)
    def visitExp6(self, ctx: HLangParser.Exp7Context):
        if ctx.getChildCount()==1:
            return self.visit(ctx.exp7())
        if ctx.NOT():
            return UnaryOp(ctx.NOT().getText(),self.visit(ctx.exp6()))
        if ctx.SUB():
            return UnaryOp(ctx.SUB().getText(),self.visit(ctx.exp6()))
        else:
            return UnaryOp(ctx.ADD().getText(),self.visit(ctx.exp6()))
    def visitExp7(self, ctx: HLangParser.Exp7Context):
        if ctx.ele():
            return self.visit(ctx.ele())
        else :
            return self.visit(ctx.callable_())      
    def visitCallable(self, ctx: HLangParser.CallableContext):
        fu=self.visit(ctx.fu())
        acc=self.visit(ctx.arracc())
        if ctx.ID():              
            if fu!=[] :
                if acc:
                    return reduce(lambda x,y: ArrayAccess(x,y),acc,FunctionCall(Identifier(ctx.ID().getText()),fu if fu!=[[]] else []))
                return FunctionCall(Identifier(ctx.ID().getText()),fu if fu!=[[]] else [])
            elif acc:
                return reduce(lambda x,y: ArrayAccess(x,y),acc,Identifier(ctx.ID().getText()))
            
            return Identifier(ctx.ID().getText())
        if ctx.INT():
            return FunctionCall(Identifier("int"),fu if fu!=[[]] else [])
        if ctx.FLOAT():
            return FunctionCall(Identifier("float"),fu if fu!=[[]] else [])
        if ctx.array():
            # if ctx.exp():
            #     array=self.visit(ctx.array())
            #     expl=self.visit(ctx.exp())
            #     return reduce(lambda x,y: ArrayAccess(x,y),expl,array)
            # else:
            arracc=self.visit(ctx.arracc())
            if arracc ==[]:
                return self.visit(ctx.array())
            else:
                return reduce(lambda x,y: ArrayAccess(x,y),arracc,self.visit(ctx.array()))
        if ctx.INTLIT():
            return FunctionCall(ctx.INTLIT().getText(),fu if fu!=[[]] else [])
        else:
            if fu!=[]:
                if acc:
                    return reduce(lambda x,y: ArrayAccess(x,y),acc,FunctionCall(self.visit(ctx.exp()),fu))
            elif acc:
                    return reduce(lambda x,y: ArrayAccess(x,y),acc,self.visit(ctx.exp()))

            return self.visit(ctx.exp())
    # def visitPostfix(self, ctx: HLangParser.PostfixContext):
    #     if ctx.getChildCount()==4:
    #         return [self.visit(ctx.exp())] + self.visit(ctx.postfix())
    #     else:
    #         if ctx.exp():
    #             return [self.visit(ctx.exp())] + self.visit(ctx.cm()) +self.visit(ctx.postfix())
    #         else :
    #             return [None]  + self.visit(ctx.postfix())
    def visitFu(self, ctx: HLangParser.FuContext):
        if ctx.getChildCount()!=0:
                return (([self.visit(ctx.exp())] + self.visit(ctx.cm())) if ctx.exp() else [[]] )+ self.visit(ctx.fu())
        else :
                return []
    def visitArracc(self, ctx: HLangParser.ArraccContext):
        if ctx.getChildCount()!=0:
            return [self.visit(ctx.exp())] + self.visit(ctx.arracc())
        else:
            return []
    def visitCm(self, ctx: HLangParser.CmContext):
        if ctx.getChildCount()==0:
            return []
        return [self.visit(ctx.exp())] + self.visit(ctx.cm())
    def visitOpt(self, ctx: HLangParser.OptContext):
        if ctx.mtype():
            return self.visit(ctx.mtype())
        return self.visit(ctx.arr())
    def visitArr(self, ctx: HLangParser.ArrContext):
        return self.visit(ctx.arrs())
    def visitArrs(self, ctx: HLangParser.ArrsContext):
        if ctx.getChildCount()==5:
            return ArrayType(self.visit(ctx.arrs()),int(ctx.INTLIT().getText()))
        else:
            return ArrayType(self.visit(ctx.mtype()),int(ctx.INTLIT().getText()))
    
    
        
    
        
    
        
        
        
            
    


            
  
        
        
                    
        
    
        
