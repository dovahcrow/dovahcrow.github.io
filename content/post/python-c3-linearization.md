---
categories:
    - post
    - python
tags:
    - linearization
date: 2016-04-09T17:35:01+08:00
title: Python C3 Linearization
summary: >
  This article describes the linearization algorithm used in python's `super` function call.
---

本文讲解了python的方法搜索优先级, `super`函数的调用以及python的线性化算法`C3`.
<!--more-->

昨天在搞python多继承的时候遇到一个问题抽象化如下:

```python
class A:
    def foo(self):
        print("A")
class B:
    def foo(self):
        print("B")
        super().foo()
class C(B,A):
    def foo(self):
        print("C")
        super().foo()
```

调用`C().foo()`会输出:

```python
C
B
A
```

其中第一行输出`C`很好理解, 第二行`类B的foo`输出`B`以后调用了`super`的`foo方法`。但是如果`B的foo`:

1. 调用了`B`的`super`, 则因为`B`并没有父类, 所以`super().foo()`的调用应该会失败，抛出`AttributeError`错误。
2. 调用了`self`的`super`, 由于此时`self`的类型是`C`, 那么又会去调用`B`的`foo`形成无限递归调用.

然而事实上并没有发生以上两种情况。`B`的`super`竟然调用了`A`的`foo`.

其实个人觉得这里的`super`有些误导人, `super`并不一定是去寻找父类, 它的意思是: 沿着方法搜索序列(`mro`)往上搜索一格。
要理解`mro`, 首先需要知道什么是`linearization`.

`linearization`一般出现在具有多继承的语言中, 比如scala, python等.
因为多继承必然会带来方法冲突等问题从而导致方法搜索失败, 所以必须规定一个方法搜索顺序防止冲突, 线性的从最底部叶
子类开始向上搜索方法直到找到或失败. 这就要求把一棵继承树变化成一个一维的线性结构.

在python中线性化的算法是一种叫做`C3`的算法. 来自论文[A Monotonic Superclass Linearization for Dylan](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.19.3910).

它的描述如下(来自wikipedia):

> 对于以下的类型:
> ```
class O
class A extends O
class B extends O
class C extends O
class D extends O
class E extends O
class K1 extends A, B, C
class K2 extends D, B, E
class K3 extends D, A
class Z extends K1, K2, K3
```
> 他们的线性化(即方法搜索顺序)是:
> ```
L(O)  := [O]                                                // the linearization of O is trivially the singleton list [O], because O has no parents
 
L(A)  := [A] + merge(L(O), [O])                             // the linearization of A is A plus the merge of its parents' linearizations with the list of parents...
       = [A] + merge([O], [O])
       = [A, O]                                             // ...which simply prepends A to its single parent's linearization

L(B)  := [B, O]                                             // linearizations of B, C, D and E are computed similar to that of A
L(C)  := [C, O]
L(D)  := [D, O]
L(E)  := [E, O]
 
L(K1) := [K1] + merge(L(A), L(B), L(C), [A, B, C])          // first, find the linearizations of K1's parents, L(A), L(B), and L(C), and merge them with the parent list [A, B, C]
       = [K1] + merge([A, O], [B, O], [C, O], [A, B, C])    // class A is a good candidate for the first merge step, because it only appears as the head of the first and last lists
       = [K1, A] + merge([O], [B, O], [C, O], [B, C])       // class O is not a good candidate for the next merge step, because it also appears in the tails of list 2 and 3, but...
       = [K1, A, B] + merge([O], [O], [C, O], [C])          // ...class B qualified, and so does class C; class O still appears in the tail of list 3
       = [K1, A, B, C] + merge([O], [O], [O])               // finally, class O is a valid candidate, which also exhausts all remaining lists
       = [K1, A, B, C, O]

L(K2) := [K2] + merge(L(D), L(B), L(E), [D, B, E])
       = [K2] + merge([D, O], [B, O], [E, O], [D, B, E])    // select D
       = [K2, D] + merge([O], [B, O], [E, O], [B, E])       // fail O, select B
       = [K2, D, B] + merge([O], [O], [E, O], [E])          // fail O, select E
       = [K2, D, B, E] + merge([O], [O], [O])               // select O
       = [K2, D, B, E, O]

L(K3) := [K3] + merge(L(D), L(A), [D, A])
       = [K3] + merge([D, O], [A, O], [D, A])               // select D
       = [K3, D] + merge([O], [A, O], [A])                  // fail O, select A
       = [K3, D, A] + merge([O], [O])                       // select O
       = [K3, D, A, O]

L(Z)  := [Z] + merge(L(K1), L(K2), L(K3), [K1, K2, K3])
       = [Z] + merge([K1, A, B, C, O], [K2, D, B, E, O], [K3, D, A, O], [K1, K2, K3])    // select K1
       = [Z, K1] + merge([A, B, C, O], [K2, D, B, E, O], [K3, D, A, O], [K2, K3])        // fail A, select K2
       = [Z, K1, K2] + merge([A, B, C, O], [D, B, E, O], [K3, D, A, O], [K3])            // fail A, fail D, select K3
       = [Z, K1, K2, K3] + merge([A, B, C, O], [D, B, E, O], [D, A, O])                  // fail A, select D
       = [Z, K1, K2, K3, D] + merge([A, B, C, O], [B, E, O], [A, O])                     // select A
       = [Z, K1, K2, K3, D, A] + merge([B, C, O], [B, E, O], [O])                        // select B
       = [Z, K1, K2, K3, D, A, B] + merge([C, O], [E, O], [O])                           // select C
       = [Z, K1, K2, K3, D, A, B, C] + merge([O], [E, O], [O])                           // fail O, select E
       = [Z, K1, K2, K3, D, A, B, C, E] + merge([O], [O], [O])                           // select O
       = [Z, K1, K2, K3, D, A, B, C, E, O]                                               // done
```

比如要调用`Z().foo()`, 然而`D`和`A`都定义了`foo`这个方法, 则根据`Z`的线性化`L(Z) := [Z, K1, K2, K3, D, A, B, C, E, O]`, 第一个搜索到的`foo`应该来自`D`。

这样的话就完美解释了上文第一个例子中为什么`B`的`super().foo()`调用了`A`的`foo`:

`super()`其实是`super(__class__, self)`的简写, 它的作用是在`self`的线性化上排除掉自己以及自己之前的类型.

比如`B`中的`super()`其实是`super(__class__, self)`就是`super(B, self)`. 其中`self`为`C`.

比如因为`C`线性化为`L(C) := [C, B, A]`, `C`中调用`super`, 在线性化结果上排除自己以及之前的类型，则产生搜索顺序`[B, A]`, 所以`C`中`super().foo()`调用的结果是调用了`B`的`foo`.

而在`B`中调用`super()`排除自己`B`以及之前的类型`C`, 产生搜索顺序`[A]`, 所以`B`中`super().foo()`调用的结果是调用了`A`的`foo`.

这个线性化结果可以通过python的类的`mro`方法进行查看。
```python
C.mro() == [C, B, A]
```
