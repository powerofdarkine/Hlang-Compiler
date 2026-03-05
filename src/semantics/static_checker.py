from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ConstDecl, FuncDecl, Param, VarDecl, Assignment, 
    IfStmt, WhileStmt, ForStmt, ReturnStmt, BreakStmt, ContinueStmt, 
    ExprStmt, BlockStmt, IntType, FloatType, BoolType, StringType, 
    VoidType, ArrayType, IdLValue, ArrayAccessLValue, BinaryOp, UnaryOp, 
    FunctionCall, ArrayAccess, Identifier, IntegerLiteral, FloatLiteral, 
    BooleanLiteral, StringLiteral, ArrayLiteral, Type
)
from .static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)

# Import marker classes with different names to avoid conflict  
from .static_error import Identifier as IdentifierMarker, Function as FunctionMarker

class FunctionType(Type):
    def __init__(self, param_types: List[Type], return_type: Type):
        super().__init__()
        self.param_types = param_types
        self.return_type = return_type
        self.func=0
        
    def accept(self, visitor):
        return visitor.visit_function_type(self)

    def __str__(self):
        params_str = ', '.join(str(t) for t in self.param_types) if self.param_types else ""
        params_part = f"({params_str})" if params_str else "()"
        return f"FunctionType{params_part} -> {self.return_type}"
    
class Symbol:
    def __init__(self, name: str, typ: 'Type'):
        self.name = name  
        self.typ = typ
        self.const=False   
        self.param=0
        

    def __str__(self):
        return f"Symbol(name={self.name}, type={self.typ})"
    
    @staticmethod
    def str(params: List[List['Symbol']]) -> str:
        return "[" + ", ".join("[" + ", ".join(str(sym) for sym in scope) + "]" for scope in params) + "]"
    
class StaticChecker(ASTVisitor):
    def __init__(self):
        self.loopnum = 0
        self.dimen=0
        self.curr_function: FuncDecl = None
        self.createloop: bool = False
        self.rfunc=[]
        self.inconst=False

    def lookup(self, name, lst, function):
        for x in lst:
            if name==function(x):
                return x
        return None

    def visit(self, node: 'ASTNode', param):
        return node.accept(self, param)
    def check_program(self, node: 'ASTNode'):
        self.visit(node, [])
    def visit_program(self, node: 'Program', param):
        self.rfunc=node.func_decls
        env=reduce(
            lambda x,y: [([self.visit(y,x)] + x[0])]+x[1:], 
            node.const_decls + node.func_decls, 
            [[
                
                Symbol("int2str", FunctionType([IntType()], StringType())),
                Symbol("str2int", FunctionType([StringType()], IntType())),
                Symbol("str2float", FunctionType([StringType()], FloatType())),
                Symbol("float2str", FunctionType([FloatType()], StringType())),
                Symbol("bool2str", FunctionType([BoolType()], StringType())),
                Symbol("print", FunctionType([StringType()], VoidType())),
                Symbol("input", FunctionType([], StringType())),
                
                
            ]]
        ) 
        

        found_main = any(
        isinstance(sym, Symbol) and sym.name == "main" and isinstance(sym.typ, FunctionType) and 
        isinstance(sym.typ.return_type,VoidType) and sym.typ.param_types == []
        for sym in env[0])
        if not found_main:
            raise NoEntryPoint()
    def visit_integer_literal(self, node: 'IntegerLiteral', param): return IntType()
    def visit_float_literal(self, node: 'FloatLiteral', param): return FloatType()
    def visit_boolean_literal(self, node: 'BooleanLiteral', param): return BoolType()
    def visit_string_literal(self, node: 'StringLiteral', param): return StringType()
    def visit_int_type(self, node: 'IntType', param): return node
    def visit_float_type(self, node: 'FloatType', param): return node
    def visit_bool_type(self, node: 'BoolType', param): return node
    def visit_string_type(self, node: 'StringType', param): return node
    def visit_void_type(self, node: 'VoidType', param): return node
    def visit_array_type(self, node: 'ArrayType', param): return node
    
    def visit_const_decl(self, node: 'ConstDecl', param: List[List['Symbol']]):
        def dimension(node:ArrayType,dimen:list):
            return dimension(node.element_type,dimen + [node.size]) if  isinstance(node.element_type,ArrayType) else dimen + [node.size]
        def dimenlit(node:ArrayLiteral,dimen:list):
            return dimenlit(node.elements[0],dimen + [len(node.elements)]) if (node.elements != [] and isinstance(node.elements[0],ArrayLiteral)) else dimen + [len(node.elements)]
        def typearray(node,param):
            return typearray(node.element_type,param) if  isinstance(node.element_type,ArrayType) else self.visit(node.element_type,param)
        if self.lookup(node.name, param[0], lambda x: x.name)!=None:
            raise Redeclared("Constant", node.name)
        self.inconst=True
        if node.type_annotation!=None:
            typ = self.visit(node.type_annotation,param)
            if isinstance(typ,ArrayType) and typ.size==0:
                if isinstance(node.value,ArrayLiteral) and len(node.value.elements)==0:
                    n = Symbol(node.name,typ)
                    n.const=True
                    self.inconst=False
                    return n 
                else:
                    raise TypeMismatchInStatement(node)
            right=self.visit(node.value,param)
            if not isinstance(typ,type(right)):
                raise TypeMismatchInStatement(node)
            if isinstance(typ,ArrayType):
                    if not isinstance(typearray(typ,param),type(typearray(right,param))):
                        raise TypeMismatchInStatement(node)

                    if dimension(typ,[]) != dimenlit(node.value,[]):
                        raise TypeMismatchInStatement(node)
        else:
            typ=self.visit(node.value,param)
            if isinstance(typ,VoidType):
                raise TypeMismatchInExpression(node.value)
            if isinstance(typ,ArrayType)  and typ.size ==0:
                raise TypeCannotBeInferred(node)
                
        n = Symbol(node.name,typ)
        n.const=True
        self.inconst=False
        return n 
    
    def visit_func_decl(self, node: 'FuncDecl', param: List[List['Symbol']]):
        if param!=[]:
            symbol = self.lookup(node.name, param[0], lambda x: x.name)
        if node.name=="main":
            if node.params==[] and isinstance(node.return_type,VoidType):
                param=[[Symbol(node.name,FunctionType([x.param_type for x in node.params],node.return_type))]+param[0]]
            
        if symbol:
            raise Redeclared("Function",symbol.name)
        self.rfunc=self.rfunc[1:]
        self.curr_function=FunctionType([x.param_type for x in node.params],node.return_type)
        table=reduce(lambda x,y: [([out] + x[0]) if isinstance(out:= self.visit(y,x), Symbol) else x[0]]+x[1:], node.params, [[]]+[param[:-1]]+[[Symbol(node.name,FunctionType([x.param_type for x in node.params],node.return_type))]+param[0]]) 
        self.curr_function=node
        reduce(lambda x,y: [([res] + x[0]) if isinstance(res:= self.visit(y,x), Symbol) else x[0]] + x[1:], node.body, table) 
        return Symbol(node.name,FunctionType([x.param_type for x in node.params],node.return_type))
    
    def visit_param(self, node: 'Param', param: List['Symbol']) -> Symbol:
        if self.lookup(node.name, param[0], lambda x: x.name)!=None:
            raise Redeclared("Parameter",node.name)
        
        n= Symbol(node.name,node.param_type)
        n.param=1
        return n
    def visit_var_decl(self, node: 'VarDecl', param: List[List['Symbol']]) -> Symbol:
        def dimension(node:ArrayType,dimen:list):
            return dimension(node.element_type,dimen + [node.size]) if  isinstance(node.element_type,ArrayType) else dimen + [node.size]
        def dimenlit(node:ArrayLiteral,dimen:list):
            return dimenlit(node.elements[0],dimen + [len(node.elements)]) if (node.elements != [] and isinstance(node.elements[0],ArrayLiteral)) else dimen + [len(node.elements)]
        def typearray(node,param):
            return typearray(node.element_type,param) if  isinstance(node.element_type,ArrayType) else self.visit(node.element_type,param)
        if  self.lookup(node.name, param[0], lambda x: x.name)!=None:
            raise Redeclared("Variable",node.name)
        if node.type_annotation!=None:
            typ = self.visit(node.type_annotation,param)
            if isinstance(typ,ArrayType) and typ.size==0:
                if isinstance(node.value,ArrayLiteral) and len(node.value.elements)==0:
                    n = Symbol(node.name,typ)
                    n.const=True
                    self.inconst=False
                    return n 
                else:
                    raise TypeMismatchInStatement(node)
                
            right=self.visit(node.value,param)
            if isinstance(right,VoidType):
                raise TypeMismatchInExpression(node.value)
            if not isinstance(typ,type(right)):
                raise TypeMismatchInStatement(node)
            if isinstance(typ,ArrayType):

                    # if isinstance(right.element_type,VoidType):
                    
                    #         raise TypeMismatchInStatement(node)
                    if not isinstance(typearray(typ,param),type(typearray(right,param))):
                        raise TypeMismatchInStatement(node)
                    # if isinstance(node.value,ArrayLiteral):
                    #     if dimension(typ,[]) != dimenlit(right,[]):
                    #         raise TypeMismatchInStatement(node)
                    # el
                    # if isinstance(node.value,ArrayAccess):
                    if dimension(typ,[]) != dimension(right,[]):
                        
                            raise TypeMismatchInStatement(node)
                        
        else:
            typ=self.visit(node.value,param)
            if isinstance(typ,VoidType):
                raise TypeMismatchInExpression(node.value)
            if isinstance(typ,ArrayType):
                if  typ.size ==0:
                    raise TypeCannotBeInferred(node)
                
        return Symbol(node.name,typ)
    
    def visit_while_stmt(self, node: 'WhileStmt', param: List[List['Symbol']]):
        typ = self.visit(node.condition,param)
        if not isinstance(typ, BoolType):
            raise TypeMismatchInStatement(node)

        self.loopnum += 1
        self.visit(node.body, param)
        self.loopnum -= 1

    
    def visit_for_stmt(self, node: 'ForStmt', param: List[List['Symbol']]):
        typ=self.visit(node.iterable,param)
        if not isinstance(typ,ArrayType):
            raise TypeMismatchInStatement(node)
        self.createloop=True
        self.loopnum+=1
        self.visit(node.body, [[Symbol(node.variable,typ.element_type)]]+param)
        self.loopnum-=1
        
    def visit_continue_stmt(self, node: 'ContinueStmt', param: List[List['Symbol']]):
        if self.loopnum == 0: raise MustInLoop(node)
    
    def visit_break_stmt(self, node: 'BreakStmt', param: List[List['Symbol']]):
        if self.loopnum==0:
            raise MustInLoop(node)
        

   
    
    def visit_assignment(self, node: 'Assignment', param: List[List['Symbol']]):
        def dimension(node:ArrayType,dimen:list):
            return dimension(node.element_type,dimen + [node.size]) if  isinstance(node.element_type,ArrayType) else dimen + [node.size]
        def dimenlit(node:ArrayLiteral,dimen:list):
            return dimenlit(node.elements[0],dimen + [len(node.elements)]) if (node.elements != [] and isinstance(node.elements[0],ArrayLiteral)) else dimen + [len(node.elements)]
        def filterout(node):
            return node if isinstance(node, (IdLValue, Identifier)) else filterout(node.array)
        def constcheck(node,param,i):
            return False if ((node.name in [x.name for x in param[i]]) and self.lookup
                             (node.name,param[i],lambda x: x.name).const) else True
        def typearray(node,param):
            return typearray(node.element_type,param) if  isinstance(node.element_type,ArrayType) else self.visit(node.element_type,param)
        
        for i in range(len(param)):
            l=filterout(node.lvalue)
            if l.name in [x.name for x in param[i]]:
                if self.lookup(l.name,param[i],lambda x: x.name).const==1:
                    raise TypeMismatchInStatement(node)
            #  and not isinstance(node.lvalue,ArrayAccessLValue)
                else:
                    break
            else: 
                continue
        
                
        left=self.visit(node.lvalue, param)
        if isinstance(node.lvalue,IdLValue):
            n=self.lookup(node.lvalue.name, param[0],lambda x: x.name)
            if n==None:
                raise Undeclared(IdentifierMarker,node.lvalue.name)
            if self.lookup(node.lvalue.name, param[0],lambda x: x.name).param==1:
                raise TypeMismatchInStatement(node)
        else:
            temp= filterout(node.lvalue)
            if self.lookup(temp.name, param[0],lambda x: x.name).param==1:
                    raise TypeMismatchInStatement(node)

        right=self.visit(node.value,param)
        if not isinstance(left,type(right)):
            raise TypeMismatchInStatement(node)
        if isinstance(left,ArrayType):
           
            if isinstance(right,ArrayType):
                if isinstance(right.element_type,VoidType):
                    raise TypeMismatchInStatement(node)
            if not isinstance(typearray(left,param),type(typearray(right,param))):
                        raise TypeMismatchInStatement(node)

            if(dimension(left,[])!=dimenlit(node.value,[])):
                raise TypeMismatchInStatement(node)
            
        # value=self.visit(node.value,param)
        # if param[0][0].typ !=

    def visit_block_stmt(self, node: 'BlockStmt', param: List[List['Symbol']]):
        if not self.createloop:
            reduce(lambda x,y: [([out] + x[0]) if isinstance(out:= self.visit(y,x), Symbol) else x[0]]+x[1:], node.statements,  [[]] + param)
        else:
            self.createloop=False 
            reduce(lambda x,y: [([res] +x[0]) if isinstance(res:= self.visit(y,x), Symbol) else x[0]]+ x[1:], node.statements,  param)
            

    def visit_id_lvalue(self, node: 'IdLValue', param: List[List['Symbol']]):
        res= list(filter(lambda x:x!=None,[self.lookup(node.name, y, lambda x: x.name) for y in param]))
        if res!=[] and not isinstance(res[0].typ,FunctionType):
            return res[0].typ
        raise Undeclared(IdentifierMarker(), node.name)

    
    def visit_identifier(self, node: 'Identifier', param: List[List['Symbol']]):  
        
        res= list(filter(lambda x:x!=None,[self.lookup(node.name, y, lambda x: x.name) for y in param]))
        if res!=[] and not isinstance(res[0].typ,FunctionType):
            return res[0].typ
        raise Undeclared(IdentifierMarker(),node.name)
        
    def visit_if_stmt(self, node: 'IfStmt', param: List[List['Symbol']]): 
        if not isinstance(self.visit(node.condition,param),BoolType):
            raise TypeMismatchInStatement(node)
        self.visit(node.then_stmt,param)
        if all( isinstance(self.visit(x,param),BoolType) for x in [y[0] for y in node.elif_branches]):
            list(map(lambda y: self.visit(y,param),[x[1] for x in node.elif_branches]))
        else:
            raise TypeMismatchInStatement(node)
        if node.else_stmt:
            self.visit(node.else_stmt,param)
    def visit_function_call(self, node: 'FunctionCall', param: List[List['Symbol']]):
        
            
        if isinstance(node.function,Identifier):
            if node.function.name=='len':
                if not len(node.args)==1 or not isinstance(self.visit(node.args[0],param),ArrayType):
                    raise TypeMismatchInExpression(node)
                return IntType()
            name=node.function.name
        res= list(filter(lambda x:x!=None and isinstance(x.typ,FunctionType),[x if x.name==name else None for x in  param[-1]]))
        if res !=[]:
            # if not isinstance(res.typ.return_type,VoidType):
            #     raise TypeMismatchInExpression(node)
            lst=list(filter(lambda x: len(x.typ.param_types) == len(node.args),res))
            if lst != []:
                temp= list(map(lambda y: all(y),[list(map(lambda x: isinstance(x[0],type(x[1])),zip([self.visit(x,param) for x in node.args],i.typ.param_types))) for i in res]))
                # ,True)) 
                if True in temp :
                    return res[[i for i, val in enumerate(temp) if val][0]].typ.return_type
                else:
                    raise TypeMismatchInExpression(node)
                    
            raise TypeMismatchInExpression(node)
        if self.inconst:
            raise Undeclared(FunctionMarker,node.function.name)
            
        env=reduce(lambda x,y: [([self.visit(y,x)] + x[0])] + x[1:], self.rfunc, [[]]+param)
        res= list(filter(lambda x:x!=None and isinstance(x.typ,FunctionType),[x if x.name==name else None for x in  env[0]]))
        if res !=[]:
            # if not isinstance(res.typ.return_type,VoidType):
            #     raise TypeMismatchInExpression(node)
            lst=list(filter(lambda x: len(x.typ.param_types) == len(node.args),res))
            if lst != []:
                temp= list(map(lambda y: all(y),[list(map(lambda x: isinstance(x[0],type(x[1])),zip([self.visit(x,param) for x in node.args],i.typ.param_types))) for i in res]))
                # ,True)) 
                if True in temp :
                    return res[[i for i, val in enumerate(temp) if val][0]].typ.return_type
                else:
                    raise TypeMismatchInExpression(node)
                    
            raise TypeMismatchInExpression(node)    
        raise Undeclared(FunctionMarker,node.function.name)
         

 
        

    



    def visit_expr_stmt(self, node: 'ExprStmt', param: List[List['Symbol']]):
        # if isinstance(node.expr,FunctionCall):
        #     if not isinstance(self.visit(node.expr,param),VoidType):  
        #         raise TypeMismatchInStatement(node)
        # self.visit(node.expr,param)
        
        if not isinstance(node.expr,FunctionCall):
            if isinstance(node.expr,BinaryOp) and node.expr.operator==">>":
                left=self.visit(node.expr.left,param)
                if isinstance(node.expr.right,Identifier):
                    if node.expr.right.name== 'len':
                       raise TypeMismatchInStatement(node) 
                    res= list(filter(lambda x:x!=None and isinstance(x.typ,FunctionType),[x if x.name==node.expr.right.name else None for x in  param[-1]]))
                    if res !=[]:
            # if not isinstance(res.typ.return_type,VoidType):
            #     rai   se TypeMismatchInExpression(node)
                        lst=list(filter(lambda x: len(x.typ.param_types) == 1,res))
                        if lst != []:
                            temp= list(map(lambda y: isinstance(y[0],type(y[1])),[(x.typ.param_types[-1],left) for x in lst]))
                            if True in temp :
                                n= lst[[i for i, val in enumerate(temp) if val][0]]
                                n.typ.func+=1
                                if n.typ.func>=len(n.typ.param_types)-1:
                                    n.typ.func=0
                                if not isinstance(n.typ.return_type,VoidType):
                                    raise TypeMismatchInStatement(node)
                                else:
                                    return VoidType()
                            else:
                                raise TypeMismatchInStatement(node)
                    
                        raise TypeMismatchInStatement(node)                
                    raise Undeclared(FunctionMarker,node.expr.right.name)
                    

                    
                if isinstance(node.expr.right,FunctionCall):
                    if isinstance(node.expr.right.function,Identifier):
                        res= list(filter(lambda x:x!=None and isinstance(x.typ,FunctionType),[x if x.name==node.expr.right.function.name else None for x in  param[-1]]))
                        if res !=[]:
                            l=len(node.expr.right.args)
                            b= list(map(lambda y: all(y),[list(map(lambda x: isinstance(x[0],type(x[1])),zip([self.visit(x,param) for x in node.expr.right.args],i.typ.param_types[::-1]))) for i in res]))
                            if True in b:
                                k=[x[1] for x in list(filter(lambda x: x[0],zip(b,res)))]
                            else:
                                raise TypeMismatchInStatement(node)

                # if not isinstance(res.typ.return_type,VoidType):
                #     rai   se TypeMismatchInExpression(node)
                            lst=list(filter(lambda x: len(x.typ.param_types) !=l ,k)) 
                            if lst != []:
                                temp= list(map(lambda y: isinstance(y[0],type(y[1])),[(x.typ.param_types[len(x.typ.param_types)-l-1],left) for x in lst]))
                                
                                if True in temp :
                                    
                                    n= lst[[i for i, val in enumerate(temp) if val][0]]
                    
                                    # n.typ.func+=1
                                    # if n.typ.func==len(n.typ.param_types)-1:
                                    #     n.typ.func=0
                                    if not isinstance(n.typ.return_type,VoidType):
                                        
                                        raise TypeMismatchInStatement(node)
                                    else:
                                        return n.typ.return_type
                                else:
                                    raise TypeMismatchInStatement(node)
                            raise TypeMismatchInStatement(node)                
                        raise Undeclared(FunctionMarker,node.expr.right.function.name)
            else:
                
                if not isinstance(self.visit(node.expr,param),VoidType):
                    raise TypeMismatchInStatement(node)
                return
        if isinstance(node.expr.function,Identifier):
            name=node.expr.function.name
        res= list(filter(lambda x:x!=None and isinstance(x.typ,FunctionType),[x if x.name==name else None for x in  param[-1]]))
        if res !=[]:
            # if not isinstance(res.typ.return_type,VoidType):
            #     raise TypeMismatchInExpression(node)
            lst=list(filter(lambda x: len(x.typ.param_types) == len(node.expr.args),res))
            if lst != []:
                
                temp= list(map(lambda y: all(y),[list(map(lambda x: isinstance(x[0],type(x[1])),zip([self.visit(x,param) for x in node.expr.args],i.typ.param_types))) for i in res]))
                # ,True)) 
                if True in temp :
                    n =res[[i for i, val in enumerate(temp) if val][0]].typ.return_type
                    if not isinstance(n,VoidType):
                        raise TypeMismatchInStatement(node)
                    return n
                else:
                    raise TypeMismatchInStatement(node)
                    
            raise TypeMismatchInStatement(node)      
        env=reduce(
            lambda acc, ele: [([self.visit(ele, acc)] + acc[0])] + acc[1:], 
            self.rfunc, [[]]+param
        )
        res= list(filter(lambda x:x!=None and isinstance(x.typ,FunctionType),[x if x.name==name else None for x in  env[0]]))
        if res !=[]:
            # if not isinstance(res.typ.return_type,VoidType):
            #     raise TypeMismatchInExpression(node)
            lst=list(filter(lambda x: len(x.typ.param_types) == len(node.expr.args),res))
            if lst != []:
                
                temp= list(map(lambda y: all(y),[list(map(lambda x: isinstance(x[0],type(x[1])),zip([self.visit(x,param) for x in node.expr.args],i.typ.param_types))) for i in res]))
                # ,True)) 
                if True in temp :
                    n =res[[i for i, val in enumerate(temp) if val][0]].typ.return_type
                    if not isinstance(n,VoidType):
                        raise TypeMismatchInStatement(node)
                    return n
                else:
                    raise TypeMismatchInStatement(node)
                    
            raise TypeMismatchInStatement(node)          
        raise Undeclared(FunctionMarker,node.expr.function.name)
    
    def visit_return_stmt(self, node: 'ReturnStmt', param: List[List['Symbol']]): 
        if node.value!=None:
            typ = self.visit(node.value,param)
            if not isinstance(typ,type(self.curr_function.return_type)):
                raise TypeMismatchInStatement(node)
            else:
                return typ
        if not isinstance(self.curr_function.return_type,VoidType):
                raise TypeMismatchInStatement(node)    
    def visit_binary_op(self, node: 'BinaryOp', param: List[List['Symbol']]): 
            if node.operator==">>":
                left=self.visit(node.left,param)
                if isinstance(node.right,Identifier):
                    if node.right.name=='len':
                        if not isinstance(self.visit(node.left,param),ArrayType):
                            raise TypeMismatchInExpression(node)
                        return IntType()
                    res= list(filter(lambda x:x!=None and isinstance(x.typ,FunctionType),[x if x.name==node.right.name else None for x in  param[-1]]))
                    if res !=[]:
            # if not isinstance(res.typ.return_type,VoidType):
            #     rai   se TypeMismatchInExpression(node)
                        lst=list(filter(lambda x: len(x.typ.param_types) == 1,res))
                        if lst != []:
                            temp= list(map(lambda y: isinstance(y[0],type(y[1])),[(x.typ.param_types[-1],left) for x in lst]))
                            if True in temp :
                                n= lst[[i for i, val in enumerate(temp) if val][0]]
                                n.typ.func+=1
                                if n.typ.func>=len(n.typ.param_types)-1:
                                    n.typ.func=0
                                # if isinstance(n.typ.return_type,VoidType):
                                #     raise TypeMismatchInExpression(node)
                                # else:
                                return n.typ.return_type
                            else:
                                raise TypeMismatchInExpression(node)
                    
                        raise TypeMismatchInExpression(node)                
                    raise Undeclared(FunctionMarker,node.right.name)
                    

                    
                if isinstance(node.right,FunctionCall):
                    # if node.right.function.name=='len':
                    #     if not len(node.args)==0 or not isinstance(self.visit(node.left,param),ArrayType):
                    #         raise TypeMismatchInExpression(node)
                    #     return IntType()
                    if isinstance(node.right.function,Identifier):
                        res: Optional['Symbol'] = list(filter(lambda x:x!=None and isinstance(x.typ,FunctionType),[x if x.name==node.right.function.name else None for x in  param[-1]]))
                        if res !=[]:
                            l=len(node.right.args)
                            b= list(map(lambda y: all(y),[list(map(lambda x: isinstance(x[0],type(x[1])),zip([self.visit(x,param) for x in node.right.args],i.typ.param_types[::-1]))) for i in res]))
                            if True in b:
                                k=[x[1] for x in list(filter(lambda x: x[0],zip(b,res)))]
                            else:
                                raise TypeMismatchInExpression(node)

                # if not isinstance(res.typ.return_type,VoidType):
                #     rai   se TypeMismatchInExpression(node)
                            lst=list(filter(lambda x: len(x.typ.param_types) !=l ,k))
                            if lst != []:
                                temp= list(map(lambda y: isinstance(y[0],type(y[1])),[(x.typ.param_types[len(x.typ.param_types)-l-1],left) for x in lst]))
                                
                                if True in temp :
                                    
                                    n= lst[[i for i, val in enumerate(temp) if val][0]]
                                    # n.typ.func+=1
                                    # if n.typ.func==len(n.typ.param_types)-1:
                                    #     n.typ.func=0
                                    # if isinstance(n.typ.return_type,VoidType):
                                    #     raise TypeMismatchInExpression(node)
                                    # else:
                                    return n.typ.return_type
                                else:
                                    raise TypeMismatchInExpression(node)
                            raise TypeMismatchInExpression(node)                
                        raise Undeclared(FunctionMarker,node.right.function.name)
                    
            left=self.visit(node.left,param)
            right=self.visit(node.right,param)
            if node.operator in ["+","-","*","/"] : 
                if  isinstance(left,IntType) and isinstance(right,IntType):
                    return IntType()
                elif isinstance(left,FloatType) and isinstance(right,FloatType):
                    return FloatType()
                elif isinstance(left,IntType) and isinstance(right,FloatType):
                    return FloatType()
                elif isinstance(left,FloatType) and isinstance(right,IntType):
                    return FloatType()
                elif (isinstance(left,StringType) and isinstance(right,StringType)) or (isinstance(left,StringType) and not isinstance(right,(VoidType,ArrayType))):
                    if node.operator == "+":
                        return StringType()
                    raise TypeMismatchInExpression(node)
                else:
                    raise TypeMismatchInExpression(node)
            elif node.operator=="%":
                if isinstance(left,IntType) and isinstance(right,IntType):
                    return IntType()

                else:
                    raise TypeMismatchInExpression(node)
                   
            elif node.operator in ["<","<=",">=",">"]:
               
                if  not (isinstance(left,IntType) or isinstance(left,FloatType)):
                        raise TypeMismatchInExpression(node)
                if  not (isinstance(right,IntType) or isinstance(right,FloatType)):
                        raise TypeMismatchInExpression(node)
                    
                return BoolType()
                
                
            elif node.operator in ["==","!="]:
                if isinstance(left,(IntType,FloatType)) and isinstance(right,(IntType,FloatType)):
                    return BoolType()
                if isinstance(left,type(right)):
                    return BoolType()
                raise TypeMismatchInExpression(node)
            else:
                if isinstance(left,BoolType) and isinstance(right,BoolType):
                    return BoolType()
                raise TypeMismatchInExpression(node)


    def visit_unary_op(self, node: 'UnaryOp', param: List[List['Symbol']]): 
            result=self.visit(node.operand,param)
            if node.operator  in ["+","-"]:
                if (isinstance(result,IntType) or isinstance(result,FloatType)):
                    return result
                raise TypeMismatchInExpression(node)
            else:
                if isinstance(result,BoolType):
                    return result
                raise TypeMismatchInExpression(node)
                

    def visit_array_access(self, node: 'ArrayAccess', param: List[List['Symbol']]): 
        def dimension(node:ArrayType,dimen:list):
            return dimension(node.element_type,dimen + [node.size]) if  isinstance(node.element_type,ArrayType) else dimen + [node.size]
        def listintype(node:ArrayAccess,param,lst: list):
            return listintype(node.array,param,lst + [self.visit(node.index,param)]) if isinstance(node.array,ArrayAccess) else lst + [self.visit(node.index,param)]
        def typearray(node:ArrayAccess,param):
            return typearray(node.array,param) if  isinstance(node.array,ArrayAccess) else self.visit(node.array,param)
        def typd(node:ArrayType,param,start,end):
            return typd(node.element_type,param,start+1,end) if start!=end else self.visit(node.element_type,param)
        lst=listintype(node,param,[])
        if not all([isinstance(x,IntType) for x in lst]):
            raise TypeMismatchInExpression(node)
        typ=typearray(node,param)
        if not isinstance(typ,ArrayType):
            raise TypeMismatchInExpression(node)
        else:
            if len(dimension(typ,[])) < len(lst):
                raise TypeMismatchInExpression(node)
        
        return typd(typ,param,1,len(lst))
    def visit_array_literal(self, node: 'ArrayLiteral', param: List[List['Symbol']]): 
        def dimension(node:ArrayType,dimen:list):
            return dimension(node.element_type,dimen + [node.size]) if  isinstance(node.element_type,ArrayType) else dimen + [node.size]
        def validate_list_of_lists(lst):
            if not lst:
                return True  # Empty list is considered valid
    # Get the length of the first sublist
            first_len = len(lst[0])

            for sublist in lst:
                if len(sublist) != first_len:
                    return False  # Length mismatch

            for i in range(first_len):
                 reference = lst[0][i]
            for sublist in lst[1:]:
                if sublist[i] != reference:
                    return False  # Mismatch in corresponding element

            return True
        
        if node.elements==[]:
            return ArrayType(VoidType(),0)
        boo = all(isinstance(self.visit(e, param), type(self.visit(node.elements[0], param))) for e in node.elements)
        if not boo:
            raise TypeMismatchInExpression(node)
        lst=list(map(lambda x: self.visit(x,param),node.elements))
        if lst!=[] and isinstance(lst[0],ArrayType):
            temp=list(map(lambda x: dimension(x,[]),lst))
            if not validate_list_of_lists(temp):
                raise TypeMismatchInExpression(node)
        return ArrayType(self.visit(node.elements[0],param),len(node.elements))
    def visit_array_access_lvalue(self, node: 'ArrayAccessLValue', param: List[List['Symbol']]): 
        def dimension(node:ArrayType,dimen:list):
            return dimension(node.element_type,dimen + [node.size]) if  isinstance(node.element_type,ArrayType) else dimen + [node.size]
        def listintype(node,param,lst: list):
            return listintype(node.array,param,lst + [self.visit(node.index,param)]) if isinstance(node.array,(ArrayAccess,ArrayAccessLValue)) else lst + [self.visit(node.index,param)]
        def typearray(node,param):
            return typearray(node.array,param) if  isinstance(node.array,(ArrayAccess,ArrayAccessLValue)) else self.visit(node.array,param)
        def typd(node:ArrayType,param,start,end):
            return typd(node.element_type,param,start+1,end) if start!=end else self.visit(node.element_type,param)
        lst=listintype(node,param,[])
        if not all([isinstance(x,IntType) for x in lst]):
            raise TypeMismatchInExpression(node)
        typ=typearray(node,param)
        if not isinstance(typ,ArrayType):
            raise TypeMismatchInExpression(node)
        else:
            if len(dimension(typ,[])) < len(lst):
                raise TypeMismatchInExpression(node)
        return typd(typ,param,1,len(lst))


    

    
    