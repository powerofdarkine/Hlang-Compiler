"""
Code Generator for HLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from ast import Sub
from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.class_name = "HLang"
        self.emit = Emitter(self.class_name + ".j")
        self.resfunc=[]
        self.cons=[]
        self.inconst=False
        self.curfunc=None
    def visit_program(self, node: "Program", o: Any = None):
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))
        self.resfunc=node.func_decls
        self.cons=node.const_decls
        list_const=[Symbol(x.name,self.visit(x.value,Access(Frame("",""),[],False,True))[1],CName(self.class_name)) for x in node.const_decls]
        
        for x in list_const:
            self.emit.print_out(self.emit.emit_attribute(x.name,x.type,True))
        self.inconst=True
        self.generate_method(
        FuncDecl("<clinit>", [], VoidType(), [Assignment(IdLValue(item.name), item.value) for item in node.const_decls]),
        SubBody(Frame("<clinit>", VoidType()), list_const),
        
    )   
        self.inconst=False
        global_env = reduce(
            lambda acc, cur: self.visit(cur, acc),
            node.func_decls,
            SubBody(None, IO_SYMBOL_LIST),
        )
        
        self.generate_method(
            FuncDecl("<init>", [], VoidType(), []),
            SubBody(Frame("<init>", VoidType()), []),
        )
        self.emit.emit_epilog()

    def generate_method(self, node: "FuncDecl", o: SubBody = None):
        frame = o.frame

        is_init = node.name == "<init>"
        is_main = node.name == "main"

        param_types = list(map(lambda x: x.param_type, node.params))
        if is_main:
            param_types = [ArrayType(StringType(), 0)]
        return_type = node.return_type

        self.emit.print_out(
            self.emit.emit_method(
                node.name, FunctionType(param_types, return_type), not is_init
            )
        )

        frame.enter_scope(True)

        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        # Generate code for parameters
        if is_init:
            this_idx = frame.get_new_index()

            self.emit.print_out(
                self.emit.emit_var(
                    this_idx, "this", ClassType(self.class_name), from_label, to_label
                )
            )
        elif is_main:
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", ArrayType(StringType(), 0), from_label, to_label
                )
            )
        else:
            o = reduce(lambda acc, cur: self.visit(cur, acc), node.params, o)

        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # Generate code for body

        if is_init:
            self.emit.print_out(
                self.emit.emit_read_var(
                    "this", ClassType(self.class_name), this_idx, frame
                )
            )
            self.emit.print_out(self.emit.emit_invoke_special(frame))

        o = reduce(lambda acc, cur: self.visit(cur, acc), node.body, o)

        if type(return_type) is VoidType:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(to_label, frame))

        self.emit.print_out(self.emit.emit_end_method(frame))

        frame.exit_scope()

    def visit_const_decl(self, node: "ConstDecl", o: Any = None):
        # if node.type_annotation:
        #     # typ1=node.type_annotation
        #     code,typ=self.visit(node.value,o)
        # else:
        #     code,typ=self.visit(node.value,o)
        # # idx=o.frame.get_new_index()
        # self.emit.print_out(code)
        # self.emit.emit_write_var(node.name,typ,idx,o.frame)
        # o.sym.append(Symbol(node.name,typ,Index(idx)))
        # return SubBody(o.frame,o.sym)
        # frame = Frame(node.name, node.return_type)
        # idx = o.frame.get_new_index()
        # self.emit.print_out(
        #     self.emit.emit_var(
        #         idx,
        #         node.name,
        #         node.type_annotation,
        #         o.frame.get_start_label(),
        #         o.frame.get_end_label(),
        #     )
        # )
        # if isinstance(node.value,ArrayLiteral):
        #     pass
        # else:
        #     code=self.emit.emit_put_static(f{self.c},)
        # if node.value is not None:
        #     self.visit(
        #         Assignment(IdLValue(node.name), node.value),
        #         SubBody(
        #             o.frame,
        #             [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
        #         ),
        #     )
        # return SubBody(
        #     o.frame,
        #     [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
        # )
        pass
    def visit_func_decl(self, node: "FuncDecl", o: SubBody = None):
        frame = Frame(node.name, node.return_type)
        self.curfunc=Symbol(f'{node.name}',FunctionType([x.param_type for x in node.params],node.return_type),CName(self.class_name))
        self.resfunc=self.resfunc[1:]
        self.generate_method(node, SubBody(frame, o.sym))
        param_types = list(map(lambda x: x.param_type, node.params))
        return SubBody(
            None,
            [
                Symbol(
                    node.name,
                    FunctionType(param_types, node.return_type),
                    CName(self.class_name),
                )
            ]
            + o.sym,
        )

    def visit_param(self, node: "Param", o: Any = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.param_type,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        return SubBody(
            o.frame,
            [Symbol(node.name, node.param_type, Index(idx))] + o.sym,
        )

    # Type system

    def visit_int_type(self, node: "IntType", o: Any = None):
        return self.emit.get_jvm_type(node),IntType()

    def visit_float_type(self, node: "FloatType", o: Any = None):
        return self.emit.get_jvm_type(node),FloatType()

    def visit_bool_type(self, node: "BoolType", o: Any = None):
        return self.emit.get_jvm_type(node),BoolType()

    def visit_string_type(self, node: "StringType", o: Any = None):
        return  self.emit.get_jvm_type(node),StringType()

    def visit_void_type(self, node: "VoidType", o: Any = None):
        return self.emit.get_jvm_type(node),VoidType()

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        return self.emit.get_jvm_type(node),node

    # Statements

    def visit_var_decl(self, node: "VarDecl", o: SubBody = None):

        idx = o.frame.get_new_index()
       
        if node.type_annotation:
            self.emit.print_out(
                self.emit.emit_var(
                    idx,
                    node.name,
                    node.type_annotation,
                    o.frame.get_start_label(),
                    o.frame.get_end_label(),
                )
            )
        

            if node.value is not None:
                self.visit(
                    Assignment(IdLValue(node.name), node.value),
                    SubBody(
                        o.frame,
                        [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
                    ),
                )
            return SubBody(
                o.frame,
                [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
            )
        else:
            self.emit.print_out(
                self.emit.emit_var(
                    idx,
                    node.name,
                    self.visit(node.value,Access(o.frame,o.sym))[1],
                    o.frame.get_start_label(),
                    o.frame.get_end_label(),
                )
            )
        

            if node.value is not None:
                self.visit(
                    Assignment(IdLValue(node.name), node.value),
                    SubBody(
                        o.frame,
                        [Symbol(node.name, self.visit(node.value,Access(o.frame,o.sym))[1], Index(idx))] + o.sym,
                    ),
                )
            return SubBody(
                o.frame,
                [Symbol(node.name, self.visit(node.value,Access(o.frame,o.sym))[1], Index(idx))] + o.sym,)

    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        def filterout(node):
            return node if isinstance(node, (IdLValue, Identifier)) else filterout(node.array)
        if type(node.lvalue) is ArrayAccessLValue:
            code,typ=self.visit(node.lvalue,Access(o.frame,o.sym,True,True))
            self.emit.print_out(code)
            rc, rt = self.visit(node.value, Access(o.frame, o.sym,False,True))
            self.emit.print_out(rc)
            if type(rt) is ArrayType and not (type(node.value) == ArrayLiteral):
                self.emit.print_out(f"\tinvokevirtual {self.emit.get_jvm_type(rt)}/clone()Ljava/lang/Object;\n")
                self.emit.print_out(f"\tcheckcast {self.emit.get_jvm_type(rt)}\n")
            temp=filterout(node.lvalue)
            
            sym = next(filter(lambda x: x.name == temp.name, o.sym), False)    
            self.emit.print_out(self.emit.emit_astore(rt,o.frame))
           
            return o
        else:
            rc, rt = self.visit(node.value, Access(o.frame, o.sym,False))
            self.emit.print_out(rc)
            
            if type(rt) is ArrayType and not (type(node.value) == ArrayLiteral):
                self.emit.print_out(f"\tinvokevirtual {self.emit.get_jvm_type(rt)}/clone()Ljava/lang/Object;\n")
                self.emit.print_out(f"\tcheckcast {self.emit.get_jvm_type(rt)}\n")
            lc, lt = self.visit(node.lvalue, Access(o.frame, o.sym,True))
            self.emit.print_out(lc)
        return o

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        el=[o.frame.get_new_label() for x in node.elif_branches]
        if node.else_stmt!=[] and node.else_stmt!= None:
            falselabel=o.frame.get_new_label()
        endlabel=o.frame.get_new_label()
        boo,typ=self.visit(node.condition,Access(o.frame,o.sym))
        self.emit.print_out(boo)
        if el!=[]:
            self.emit.print_out(self.emit.emit_if_false(el[0],o.frame))
            self.visit(node.then_stmt,o)
            if len (node.then_stmt.statements) != 0 and not isinstance (node.then_stmt.statements[-1],ReturnStmt):
                            self.emit.print_out(self.emit.emit_goto(endlabel,o.frame))
            for x in range(len(node.elif_branches)):
                self.emit.print_out(self.emit.emit_label(el[x],o.frame))
                b,t=self.visit(node.elif_branches[x][0],Access(o.frame,o.sym))
                self.emit.print_out(b)
                if x != len(node.elif_branches)-1:
                    self.emit.print_out(self.emit.emit_if_false(el[x+1],o.frame))
                    self.visit(node.elif_branches[x][1],o)
                    if len (node.elif_branches[x][1].statements) != 0 and not isinstance (node.elif_branches[x][1].statements[-1],ReturnStmt):
                            self.emit.print_out(self.emit.emit_goto(endlabel,o.frame))
                    
                else: 
                    if node.else_stmt!=[] and node.else_stmt!= None:
                        self.emit.print_out(self.emit.emit_if_false(falselabel,o.frame))
                        self.visit(node.elif_branches[x][1],o)
                        if len (node.elif_branches[x][1].statements) != 0 and not isinstance (node.elif_branches[x][1].statements[-1],ReturnStmt):
                            self.emit.print_out(self.emit.emit_goto(endlabel,o.frame))
                        self.emit.print_out(self.emit.emit_label(falselabel,o.frame))
                        self.visit(node.else_stmt,o)
                        
                    else:
                        self.emit.print_out(self.emit.emit_if_false(endlabel,o.frame))
                        self.visit(node.elif_branches[x][1],o)
        else:
            if node.else_stmt!=[] and node.else_stmt!= None:
                self.emit.print_out(self.emit.emit_if_false(falselabel,o.frame))
                self.visit(node.then_stmt,o)
                if len (node.else_stmt.statements) != 0 and not isinstance (node.else_stmt.statements[-1],ReturnStmt):
                            self.emit.print_out(self.emit.emit_goto(endlabel,o.frame))
                self.emit.print_out(self.emit.emit_label(falselabel,o.frame))
                self.visit(node.else_stmt,o)
                
            else:
                self.emit.print_out(self.emit.emit_if_false(endlabel,o.frame))
                self.visit(node.then_stmt,o)
        self.emit.print_out(self.emit.emit_label(endlabel,o.frame))
        return o

    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        o.frame.enter_loop()
        breaklabel=o.frame.get_break_label()
        continuelabel=o.frame.get_continue_label()
        self.emit.print_out(self.emit.emit_label(continuelabel,o.frame))
        boo,typ=self.visit(node.condition,Access(o.frame,o.sym))
        self.emit.print_out(boo)
        self.emit.print_out(self.emit.emit_if_false(breaklabel,o.frame))
        self.visit(node.body,o)
        self.emit.print_out(self.emit.emit_goto(continuelabel,o.frame))
        self.emit.print_out(self.emit.emit_label(breaklabel,o.frame))
        o.frame.exit_loop()
        return o
    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        def dimension(node:ArrayType,dimen:list):
            return dimension(node.element_type,dimen + [node.size]) if  isinstance(node.element_type,ArrayType) else dimen + [node.size]
        def typearray(node,param):
            return typearray(node.element_type,param) if  isinstance(node.element_type,ArrayType) else self.visit(node.element_type,param)
        tempidx=o.frame.get_new_index()
        self.emit.print_out(self.emit.emit_push_iconst(0,o.frame))
        self.emit.print_out(self.emit.emit_write_var('i',IntType(),tempidx,o.frame))
        o.frame.enter_loop()
        continuel=o.frame.get_continue_label()
        breakl=o.frame.get_break_label()
        forl=o.frame.get_new_label()
        code,typ=self.visit(node.iterable,Access(o.frame,o.sym,False,True))
        forlen=typ.size
        idx=o.frame.get_new_index()
        self.emit.print_out(self.emit.emit_label(forl,o.frame))
        self.emit.print_out(self.emit.emit_read_var('i',IntType(),tempidx,o.frame))
        self.emit.print_out(self.emit.emit_push_iconst(forlen-1,o.frame))
        self.emit.print_out(self.emit.emit_ificmpgt(breakl,o.frame))
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_read_var('i',IntType(),tempidx,o.frame))
        self.emit.print_out(self.emit.emit_aload(typ.element_type,o.frame))
        
        self.emit.print_out(self.emit.emit_write_var(node.variable,typ.element_type,idx,o.frame))
        self.visit(node.body,SubBody(o.frame,[Symbol(node.variable,typ.element_type,Index(idx))]+o.sym))
        
        self.emit.print_out(self.emit.emit_label(continuel,o.frame))
        self.emit.print_out(self.emit.emit_read_var('i',IntType(),tempidx,o.frame))
        self.emit.print_out(self.emit.emit_push_iconst(1,o.frame))
        self.emit.print_out(self.emit.emit_add_op('+',IntType(),o.frame))
        self.emit.print_out(self.emit.emit_write_var('i',IntType(),tempidx,o.frame))
        self.emit.print_out(self.emit.emit_goto(forl,o.frame))
        self.emit.print_out(self.emit.emit_label(breakl,o.frame))
        o.frame.exit_loop()
        return o
        
        
    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        if node.value:
            code,typ=self.visit(node.value,Access(o.frame,o.sym))
            self.emit.print_out(code)
            self.emit.print_out(self.emit.emit_return(typ,o.frame))
        else:
            if o.frame.get_stack_size()==0:
                pass
            else:
                self.emit.print_out(self.emit.emit_pop(o.frame))
            self.emit.print_out(self.emit.emit_return(VoidType(),o.frame))
        return o

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_break_label(),o.frame))
        return o

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_continue_label(),o.frame))
        return o   

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        code, typ = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        return o

    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        temp=o
        for x in node.statements:
            o=self.visit(x,o)
        return temp

    # Left-values

    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        sym = next(
            filter(lambda x: x.name == node.name, o.sym),
            False,
        )
        if type(sym.value) is Index:
            code = self.emit.emit_write_var(
                sym.name, sym.type, sym.value.value, o.frame
            )
        else:
            code=self.emit.emit_put_static(f'{self.class_name}/{sym.name}',sym.type,o.frame)
        return code, sym.type

    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Access = None):
        def typearray(node,param):
            return typearray(node.array,param) if  isinstance(node.array,(ArrayAccess,ArrayAccessLValue)) else self.visit(node.array,param)
        def listintype(node,param,lst: list):
            return listintype(node.array,param,lst + [self.visit(node.index,param)]) if isinstance(node.array,(ArrayAccess,ArrayAccessLValue)) else lst + [self.visit(node.index,param)]
        
        codeGen, arrType = self.visit(node.array, o)
        code_index, index_type = self.visit(node.index, o)
        element_type = arrType.element_type
        retType = arrType.element_type
        return codeGen + code_index , retType
    # Expressions

    def visit_binary_op(self, node: "BinaryOp", o: Access = None):
        

        if node.operator in ['||']:
            label1 = o.frame.get_new_label()
            label2 = o.frame.get_new_label()
            left,_=self.visit(node.left,o)
            code =left+self.emit.emit_if_true(label1,o.frame)
            right,_=self.visit(node.right,o)
            code +=right + self.emit.emit_if_true(label1,o.frame)
            code +=self.emit.emit_push_iconst(0,o.frame)
            code += self.emit.emit_goto(label2,o.frame)
            code+=self.emit.emit_label(label1,o.frame) + self.emit.emit_push_iconst(1,o.frame)
            code+=self.emit.emit_label(label2,o.frame)
            return code, BoolType()
        
        if node.operator in ['&&']:
            label1 = o.frame.get_new_label()
            label2 = o.frame.get_new_label()
            left,_=self.visit(node.left,o)
            code =left+self.emit.emit_if_false(label1,o.frame)
            right,_=self.visit(node.right,o)
            code +=right + self.emit.emit_if_false(label1,o.frame)
            code +=self.emit.emit_push_iconst(1,o.frame)
            code += self.emit.emit_goto(label2,o.frame)
            code+=self.emit.emit_label(label1,o.frame) + self.emit.emit_push_iconst(0,o.frame)
            code+=self.emit.emit_label(label2,o.frame)
            return code, BoolType()

            
        codeLeft, typeLeft = self.visit(node.left, o)
        if node.operator in ['>>']:
            function_name=node.right.name if type(node.right)==Identifier else node.right.function.name
            
            function_symbol: Symbol = next(filter(lambda x: x.name == function_name, o.sym), False)
            if not function_symbol:
                for func in self.resfunc:
                    if func.name==function_name:
                        function_symbol=Symbol(func.name,FunctionType([x.param_type for x in func.params],func.return_type),CName(self.class_name))
                        break
            if type(node.right)==Identifier:
                return codeLeft + self.emit.emit_invoke_static(f'{self.class_name}/{function_name}',function_symbol.type,o.frame),function_symbol.type.return_type
            else:
                codeRight=''
                for arg in node.right.args:
                    codeRight+= self.visit(arg,o)[0]
                return codeLeft + codeRight +  self.emit.emit_invoke_static(f'{self.class_name}/{function_name}',function_symbol.type,o.frame),function_symbol.type.return_type
        if node.operator in ['+'] and type(typeLeft) in [StringType]:
            _, typeRight = self.visit(node.right, Access(Frame("", ""), o.sym))

            if type(typeRight) is IntType:
                node.right = FunctionCall(Identifier("int2str"), [node.right])
            elif type(typeRight) is FloatType:
                node.right= FunctionCall(Identifier("float2str"),[node.right]) 
            elif type(typeRight) is FloatType:
                node.right= FunctionCall(Identifier("float2str"),[node.right]) 
            elif type(typeRight) is BoolType:
                node.right =FunctionCall(Identifier("bool2str"),[node.right])
            right,_=self.visit(node.right,o)
            
            # param=reduce(lambda x,y: x + self.emit.get_jvm_type(y),node.right.args,'')
            return codeLeft + right + self.emit.emit_invoke_virtual('java/lang/String/concat',FunctionType([StringType()],StringType()),o.frame),StringType()
            ## TODO java/lang/String/concat
        codeRight, typeRight = self.visit(node.right, o)
        if node.operator in ['+', '-'] and type(typeLeft) in [FloatType, IntType]:
            typeReturn = IntType() if type(typeLeft) is IntType and type(typeRight) is IntType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntType:
                    codeLeft += self.emit.emit_i2f(o.frame)
                if type(typeRight) is IntType:
                    codeRight += self.emit.emit_i2f(o.frame)
            return codeLeft + codeRight + self.emit.emit_add_op(node.operator, typeReturn, o.frame), typeReturn
        elif node.operator in ['*', '/']:
            typeReturn = IntType() if type(typeLeft) is IntType and type(typeRight) is IntType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntType:
                    codeLeft += self.emit.emit_i2f(o.frame)
                if type(typeRight) is IntType:
                    codeRight += self.emit.emit_i2f(o.frame)
                return codeLeft + codeRight + self.emit.emit_mul_op(node.operator, typeReturn, o.frame), typeReturn
            else:
                if node.operator in ['*']:
                    return codeLeft + codeRight + self.emit.emit_mul_op(node.operator, typeReturn, o.frame), typeReturn
                else: return codeLeft + codeRight + self.emit.emit_div(o.frame), typeReturn
            
        if node.operator in ['%']:
            return codeLeft +codeRight  + self.emit.emit_mod(o.frame),IntType()
        if node.operator in ['==', '!=', '<', '>', '>=', '<='] and type(typeLeft) in [FloatType, IntType]:
            typeReturn = IntType() if type(typeLeft) is IntType and type(typeRight) is IntType else FloatType()
            if type(typeReturn) is FloatType:
                if type(typeLeft) is IntType:
                    codeLeft += self.emit.emit_i2f(o.frame)
                if type(typeRight) is IntType:
                    codeRight += self.emit.emit_i2f(o.frame)
            return codeLeft + codeRight + self.emit.emit_re_op(node.operator,typeReturn,o.frame), BoolType()

        if node.operator in ['==', '!='] and type(typeLeft) in [BoolType] : 
            return codeLeft + codeRight + self.emit.emit_re_op(node.operator,IntType(), o.frame), BoolType()
        if node.operator in ['==', '!='] and type(typeLeft) in [StringType]:
            truelabel,falselabel,endlabel=o.frame.get_new_label(),o.frame.get_new_label(),o.frame.get_new_label()
            if node.operator == '==':
                return codeLeft + codeRight + self.emit.emit_invoke_virtual('java/lang/String/compareTo',FunctionType([StringType()],IntType()),o.frame) + self.emit.emit_push_iconst(0,o.frame) + self.emit.emit_rel_op('==',IntType(),truelabel,falselabel,o.frame) + self.emit.emit_label(truelabel,o.frame) + self.emit.emit_push_iconst(1,o.frame)+ self.emit.emit_goto(endlabel,o.frame) + self.emit.emit_label(falselabel,o.frame) + self.emit.emit_push_iconst(0,o.frame)+ self.emit.emit_label(endlabel,o.frame),BoolType()
            else:
                return codeLeft + codeRight + self.emit.emit_invoke_virtual('java/lang/String/compareTo',FunctionType([StringType()],IntType()),o.frame) ,BoolType()
            ## TODO java/lang/String/compareTo
        
              
        
    def visit_unary_op(self, node: "UnaryOp", o: Any = None):
        if node.operator == '!':
            code,typ=self.visit(node.operand,o)
            return code + self.emit.emit_not(IntType(),o.frame),BoolType()
        code, type_return = self.visit(node.operand, o)
        return (code if node.operator == '+' else code + self.emit.emit_neg_op(type_return , o.frame)), type_return 

    def visit_function_call(self, node: "FunctionCall", o: Access = None):
        function_name = node.function.name
        if function_name == 'len':
            code,typ=self.visit(node.args[0],o)
            code+=self.emit.emitARRAYLENGTH()   
            # code+=self.emit.emit_invoke_static('io/int2str',FunctionType([IntType()],StringType()),o.frame)
           
            return code,IntType()
        function_symbol: Symbol = next(filter(lambda x: x.name == function_name, o.sym), False)
        if not function_symbol:
            
            for func in self.resfunc:
                if func.name==function_name:
                    function_symbol=Symbol(func.name,FunctionType([x.param_type for x in func.params],func.return_type),CName(self.class_name))
    
                    break
            if not function_symbol:
                function_symbol=self.curfunc
        
        class_name = function_symbol.value.value
        argument_codes = []
        for argument in node.args:
            ac, at = self.visit(argument, Access(o.frame, o.sym))
            
            argument_codes += [ac]
        return (
            "".join(argument_codes)
            + self.emit.emit_invoke_static(
                class_name + "/" + function_name, function_symbol.type, o.frame
            ),
            function_symbol.type.return_type
        )

    def visit_array_access(self, node: "ArrayAccess", o: Access = None) -> tuple[str, Type]:
        codeGen, arrType = self.visit(node.array, o)
        code_index, index_type = self.visit(node.index, o)
        element_type = arrType.element_type

    # Choose the right load instruction
        if not o.is_left and o.is_first:
            if isinstance(element_type, IntType):
                
                aload_code = self.emit.emit_aload(IntType(),o.frame)
            elif isinstance(element_type, FloatType):
                aload_code = self.emit.emit_aload(FloatType(),o.frame)
            elif isinstance(element_type, BoolType):
                aload_code = self.emit.emit_aload(BoolType(),o.frame)
            elif isinstance(element_type, StringType):
                aload_code = self.emit.emit_aload(StringType(),o.frame)
            elif isinstance(element_type, ClassType) or isinstance(element_type, ArrayType):
                aload_code = self.emit.emit_aload(element_type,o.frame)
        elif  o.is_left and  o.is_first:
            if isinstance(element_type, IntType):
                
                aload_code = self.emit.emit_aload(IntType(),o.frame)
            elif isinstance(element_type, FloatType):
                aload_code = self.emit.emit_aload(FloatType(),o.frame)
            elif isinstance(element_type, BoolType):
                aload_code = self.emit.emit_aload(BoolType(),o.frame)
            elif isinstance(element_type, StringType):
                aload_code = self.emit.emit_aload(StringType(),o.frame)
            elif isinstance(element_type, ClassType) or isinstance(element_type, ArrayType):
                aload_code = self.emit.emit_aload(element_type,o.frame)
        elif not o.is_left and not o.is_first:
            if isinstance(element_type, IntType):
                
                aload_code = self.emit.emit_aload(IntType(),o.frame)
            elif isinstance(element_type, FloatType):
                aload_code = self.emit.emit_aload(FloatType(),o.frame)
            elif isinstance(element_type, BoolType):
                aload_code = self.emit.emit_aload(BoolType(),o.frame)
            elif isinstance(element_type, StringType):
                aload_code = self.emit.emit_aload(StringType(),o.frame)
            elif isinstance(element_type, ClassType) or isinstance(element_type, ArrayType):
                aload_code = self.emit.emit_aload(element_type,o.frame)
        else:
            if isinstance(element_type, IntType):
                aload_code = self.emit.emit_astore(IntType(),o.frame)
            elif isinstance(element_type, FloatType):
                aload_code = self.emit.emit_astore(FloatType(),o.frame)
            elif isinstance(element_type, BoolType):
                aload_code = self.emit.emit_astore(BoolType(),o.frame)
            elif isinstance(element_type, StringType):
                aload_code = self.emit.emit_astore(StringType(),o.frame)
            elif isinstance(element_type, ClassType) or isinstance(element_type, ArrayType):
                aload_code = self.emit.emit_astore(element_type,o.frame)
        retType = arrType.element_type
        
        return codeGen + code_index + aload_code, retType
        
    def visit_array_literal(self, node: "ArrayLiteral", o: Access = None) -> tuple[str, Type]:
        frame = o.frame
        arrlen=len(node.elements)
        if arrlen==0:
            pass
        else:
            _,type_element_array=self.visit(node.elements[0],o)
        
        if type(type_element_array)==IntType or type(type_element_array)==BoolType :
            codeGen = self.emit.emit_push_const(str(arrlen),IntType(),o.frame)
        else :
            codeGen = self.emit.emit_push_const(str(arrlen),StringType(),o.frame)
        if not type(type_element_array) is ArrayType:
           
            codeGen+=self.emit.emit_new_array(type_element_array,frame)
        else:
            codeGen += self.emit.emit_anew_array(type_element_array  , frame)
        
        for idx, item in enumerate(node.elements):
            codeGen +=self.emit.emit_dup(o.frame)
            # codeGen+=self.emit.emit_read_var('array',ArrayType(type_element_array, len(node.elements)) ,o.frame.get_max_index(),o.frame)
            codeGen+=self.emit.emit_push_iconst(idx,o.frame)
            if type(item)==Identifier:
                sym = next(filter(lambda x: x.name == item.name, o.sym), False)
                if sym:
                    typ=sym.type
                    codeGen+=self.emit.emit_read_var(sym.name,sym.type,sym.value.value,o.frame)
            else:
                    code,typ=self.visit(item,o)
                    
                    codeGen+=code
            
            codeGen+=self.emit.emit_astore(typ,o.frame)        
        return codeGen, ArrayType(type_element_array, len(node.elements))  

    def visit_identifier(self, node: "Identifier", o: Access = None) -> tuple[str, Type]:
        sym = next(filter(lambda x: x.name == node.name, o.sym), False)
        if not sym:
            sym = next(filter(lambda x: x.name == node.name, self.cons), False)
            
            _,typ=self.visit(sym.value,(o))
            if o.is_left and not o.is_first :
                code=self.emit.emit_write_var(sym.name,sym.type,sym.value.value,o.frame)
            elif o.is_left and o.is_first:
                code=self.emit.emit_get_static(f'{self.class_name}/{sym.name}',typ,o.frame)
            else:
                code=self.emit.emit_get_static(f'{self.class_name}/{sym.name}',typ,o.frame)
            return code, typ
        if o.is_left and not o.is_first :
            code=self.emit.emit_write_var(sym.name,sym.type,sym.value.value,o.frame)
        elif o.is_left and o.is_first:
            code=self.emit.emit_read_var(sym.name,sym.type,sym.value.value,o.frame)
        else:
            
            if self.inconst:
                code=self.emit.emit_get_static(f'{self.class_name}/{sym.name}',sym.type,o.frame)
            else:
                code=self.emit.emit_read_var(sym.name,sym.type,sym.value.value,o.frame)
        return code, sym.type

    # Literals

    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None) -> tuple[str, Type]:
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Access = None) -> tuple[str, Type]:
        return self.emit.emit_push_fconst(str(node.value),o.frame), FloatType()


    def visit_boolean_literal(self, node: "BooleanLiteral", o: Access = None) -> tuple[str, Type]:
       
        return self.emit.emit_push_iconst(1 if node.value else 0,o.frame), BoolType()
    def visit_string_literal(self, node: "StringLiteral", o: Access = None) -> tuple[str, Type]:
        return  self.emit.emit_push_const('"' + node.value + '"', StringType(), o.frame), StringType()