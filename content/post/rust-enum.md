---
author:
  description: The fortune teller
  email: doomsplayer@gmail.com
  github: https://github.com/doomsplayer
  image: /images/avatar-64x64.png
  name: Wu Young
  website: http://wooya.me
cardbackground: '#3B4D7D'
categories:
- post
date: 2015-11-04T11:51:39+08:00
title: rust enum
---

本文通过解析`llvm`的`ir`来解析rust `enum`的内存布局。
<!--more-->
rust的enum差不多是C的`enum`和`union`类型的混合体。可以写成

```rust
enum Enum {
    AEnum = 0,
    BEnum = 1,
    CEnum = 2,
}  // 类似C的Enum
```

也可以

```rust
 enum Buk {
    two_int(int,int),
    three_uint(uint,uint,uint),
    lonely_f64(f64),
} // 类似union
```

甚至 

```rust
enum LinkedListNode<T> {
    DataOnly(T),
    DataWithNext(T,Box<LinkedListNode<T>>),
}
```

总之，利用rust的enum，可以任意的构造想要的抽象数据结构。
在另一些语言中，这种数据结构叫做ADT(algebra data type, 代数数据类型)。

===============================================

* 最普通的enum。

有如下结构：

```rust
enum simple {
    A,B,C,D
}
```

在rust编译完以后，完全不会为simple生成任何的数据结构。
`let a = A` 只会被rust编译成 `let a: i8 = 0`。同理，B就是1i8，C就是2i8.

同理

```rust
enum simple {
     A = 1,
     B = 2,
     C = 3,
     D = 4,
}
```
也只是把`let a = 0i8`变成了`let a = 1i8`而已。

match这样一个最简单的enum，rust所做的仅仅只有一个简单的对i8的switch语句。

* union like enum

考虑如下enum：

```rust
enum simple {
     A(i32,i64),
     B(u8),
     C(f32),
}
```

这时，这个enum的llvm内存表示为`{ i8, [7 x i8], [1 x i64] }`，用rust来表示就是`(i8,i8,i8,i8,i8,i8,i8,i8,i64)`

一共8个i8，一个i64.
可能会纳闷：怎么会有那么多i8呢？
原因在于：内存对齐。

首先，enum的标号肯定位于头部，就是第一个i8.因此A还是0，B还是1.
但是和例1不同的是，本例中的enum是带有自定义数据的。所以必须为自定义数据分配空间。
我们来算一下：一共需要1*i8（用于标号）+1*i32（A的第一个域）+1*64（A的第二个域）。B和C我们就不管了，因为它们的大小都小于A，因此我们可以复用A的内存空间。所以这样一个enum至少需要104个bit。但是由于内存对齐的原因，第一个i8要和后面的i64对齐，所以要补上7个i8，因为7*8+8=64嘛。
补完之后我们发现，那个i32也可以被用来补完的7个i8来表示了（4个i8凑一凑就一个i32了嘛）。于是这个enum就是8个i8+1个i64组成了。

现在来看看当它们分别是A，B，C时的情况。
当enum是A的时候，它的结构会转换成{i8, i32, 
i64}.第一个用于标号，是0.第二个是A的第一个域，i32，i64是第二个域。用于内存对齐的i8被llvm自动藏起来了。完整的表示是{i8, 
[3 x i8], i32, i64}，中间3个i8会隐藏掉。
当enum是B的时候，结构就变成了{i8,i8}后面的一大堆东西统统不要。所以如果一个enum要是被这样构造了，每一个B都会浪费大量的空间（空间使用率16/128=12.5%）。对于单片机编程来说要尽量避免这种情况。
当enum是C的时候，结构是{i8,float},[3xi8]同A，会隐藏起来。后面浪费了一个i64.利用率50%，也挺低。

* 1和2混搭

如下enum：

```rust
enum simple {
     A(i32,i64),
     B(u8),
     C(f32),
     D,
     E
}
```
具体情况和union enum差不多。后面两个D和E变成{i8}罢了。

*  泛型enum

```rust
 enum simple<T> {
      Data(T),
     Nil
}
let a = simple::Data::<int>(1);
let b = simple::Nil::<uint>;
```
泛型其实只是生成了两份代码，一个叫`%"enum.main::simple<[int]>" = type { i8, [7 x i8], [1 x i64] }`， 
另一个叫`%"enum.main::simple<[uint]>" = type { i8, [7 x i8], [1 x i64] }`，其它无任何差别。

*  struct variant 

```rust
enum simple {
     duck {a: int, b: int},
     Nil
}
let a = simple::duck{a:4,b:3};
```

和普通的enum一样，只是给duck里面的两个i64起个名字罢了。在ir层面没有任何区别。

* #[repr(C)]

rust还支持把enum的内存表示变为C风格的。

```rust
#[repr(C)]
enum simple {
     a(int),
     b,c
}
```

这儿的区别在于，头部的标号和内存对齐，全部从i8变成了i32，即C的int。`{i32, [1 x i32], i64}`
