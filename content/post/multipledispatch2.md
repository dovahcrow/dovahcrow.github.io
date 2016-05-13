---
author:
  description: The fortune teller
  email: doomsplayer@gmail.com
  github: https://github.com/doomsplayer
  name: Wu Young
  website: http://wooya.me
categories:
- post
- python
tags:
- subtype
- type system
date: 2016-05-13T18:41:28+08:00
title: multipledispatch2
---

本文讲述了笔者的multipledispatch2库的一些技术细节.
<!--more-->

由于是从静态语言切换成的python使用者, 笔者对python的动态类型非常不适应. 因此几乎每个地方都会使用multipledispatch给保护一下.

然后用久了感觉有几个不方便:

  1. `multipledispatch`不支持函数参数的类型签名. `python 3.5`加入了`typing`库, 表示`def foo(bar: int, baz: str) -> list`这种写法是官方提倡的, 然而multipledispatch却不支持这种写法.
  2. `multipledispatch`不支持一个类型是多个类型的子类型的写法, 比如我想表达`A <: B && A <: C`时就无能为力了.

由于给作者提issue以后作者几个月没动静, 因此在`multipledispatch`的基础上, 笔者修改了一些代码, 发布了multipledispatch2.

主要改动是:

  1. 增加了对`type annotation`的支持, 即:
     对于原来的
     
     ```pyhton
     @dispatch(int, str)
     def foo(a, b):
         pass
     ```
     
     现在可以写作:
     
     ```python
     @dispatch
     def foo(a: int, b: str):
         pass
     ```
     
     相对更自然了一点.
     
  2. 增加了对`subtype of multiple types`的支持:
  
     ```python
     class A: pass
     class B: pass
     class C(A, B): pass
     @dispatch
     def foo(a: [A, B]): 
         pass
     ```
     
     那么`foo(C())`的调用是成立的. 当且仅当入参同时是`A`和`B`的子类, 对foo的调用才会成立.
     
     这个对于写库的人来说十分方便, 当你想要使用`trait`来`mixin`的时候, `user`可能会拿你的`trait`混合出很多`subtypes`. 如果你想要提供一些函数来操作这些`subtypes`, 使用原有的`multipledispatch`是不可能的.
     
## 技术细节:
  
  主要问题在于`dispatch order`上. 比如: 对于同一个函数名foo, 它有两种类型:
  
  1. `foo(a: A, b: B): pass`
  2. `foo(a: C, b: B): pass`
  
  其中:
  
  ```python
  class A: pass
  class B: pass
  class C(A): pass
  class D(C): pass
  ```
  
  当你传入参数`(C, B)`的时候, 显然希望调用的是2而不是1, 当传入`(D, B)`的时候, 显然也希望调用2而不是1.只有当传入`(A, B)`时, 才希望调用的是1.
  
  用形象的话来说: 对于入参X, 希望被调用的函数是拥有具体的签名的那个函数.
  
  于是这就要求我们有一个排序方法将foo的所有签名进行排序, 越具体的签名尽可能在前面. 进行签名搜索时, 应该从头开始搜, 并采纳第一个适合的签名.
  
  还是上面那个例子, 如果我们能够产生一个搜索顺序: `[(C, B), (A, B)]`, 那不就符合要求了?
  
  对于排序, 显然需要一个操作符`compare`进行比较. 那么对于签名的`compare`该如何定义呢? 即如何确定签名与签名之间谁大谁小.
  
  在这里我们定义`compare`如下:
  
  ```
  A, B 为 tuple of types
  
  if A.length == b.length then
      A compare B := A <: B (即A是B的子类型)
  ```
  
  而对于`tuple of types`的`<:`定义如下:
  
  ```
  for zip(all a in A, all b in B):
    a <: b
  ```
  即A中每一个类型都是对应位置上B的子类型时, `A<:B`
  
  这样我们定义了类型签名之间的`subtyping`关系. 于是我们使用这个`compare`关系对一个函数的所有签名进行排序, 结果将得到若干个`DAG`(有向无环图).
  
  至于为什么是`DAG`而不是序列, 是因为签名之间并不是良序关系. 两个签名之间可能其实是没有任何大小关系的. 如果签名间没有关系(无法比较), 则他们将产生两个连接片.
  
  接下来我们对`DAG`采取拓扑排序, 那么将得到一个搜索序列. 按照这个序列搜索, 一定能够得到最"确切"的那个签名.
    
### 加入`multiple subtypes`后的变化:
  
  上面的定义很不错, 但是没有考虑一种情况: 在`tuple of types`的`<:`定义中, 我们使用了`a <: b`这个比较. 然而当`multiple subtypes`存在的时候, 如何求`a <: b`呢?
  
  比如,如何证明`C<: [A, B]`当
  
  ```
  class A: pass
  class B: pass
  class C(A, B): pass
  ```
  
  时呢?
  
  甚至是`[C, D] <: [A, B]`当
  
  ```
  class A: pass
  class B: pass
  class C(A): pass
  class D(B): pass
  ```
  
  时呢?
  
  我们拓展一下`subtyping`关系即可:
  
  ```
  对于types a and b
  
  def a <: b as
    if a and b both are type then
        return a <: b
    else if a is type and b is tuple then
      return if a <: all types in b
    else if a is tuple and b is type then
      return if any types in a <: b
    else if a and b both are tuple then
      return for all types in b if any types in a <: types in b
  ```
  
  这样一来, 就完美支持`multiple subtypes`啦.
