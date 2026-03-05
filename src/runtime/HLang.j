.source HLang.java
.class public HLang
.super java/lang/Object

.method public static <clinit>()V
Label0:
	return
Label1:
.limit stack 0
.limit locals 0
.end method

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is out Ljava/lang/String; from Label0 to Label1
	ldc ""
	astore_1
	iconst_0
	istore_2
Label4:
	iload_2
	iconst_1
	if_icmpgt Label3
	iconst_2
	newarray int
	dup
	iconst_0
	iconst_1
	iastore
	dup
	iconst_1
	iconst_2
	iastore
	iload_2
	iaload
	istore_3
	iconst_0
	istore 4
Label7:
	iload 4
	iconst_1
	if_icmpgt Label6
	iconst_2
	newarray int
	dup
	iconst_0
	iconst_1
	iastore
	dup
	iconst_1
	iconst_2
	iastore
	iload 4
	iaload
	istore 5
	iload_3
	iload 5
	iadd
	iconst_3
	if_icmpne Label9
	iconst_1
	goto Label10
Label9:
	iconst_0
Label10:
	ifle Label8
	goto Label5
Label8:
	aload_1
	iload_3
	invokestatic io/int2str(I)Ljava/lang/String;
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String;
	iload 5
	invokestatic io/int2str(I)Ljava/lang/String;
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String;
	astore_1
Label5:
	iload 4
	iconst_1
	iadd
	istore 4
	goto Label7
Label6:
Label2:
	iload_2
	iconst_1
	iadd
	istore_2
	goto Label4
Label3:
	aload_1
	invokestatic io/print(Ljava/lang/String;)V
	return
Label1:
.limit stack 15
.limit locals 6
.end method

.method public <init>()V
.var 0 is this LHLang; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
Label1:
.limit stack 1
.limit locals 1
.end method
