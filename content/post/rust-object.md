---
categories:
- post
- rust
tags:
- OO
- generic
date: 2015-11-04T11:49:25+08:00
title: rust object
summary: >
  This article simply introduced the mechanism of dynamic dispatch in rust.  
---

rust有非常强大的类型系统。今天我们来说说rust的泛型。
<!--more-->

rust有两种泛型：

1. 基于`static 
dispatch`的泛型，类似于C++的模板。在编译期进行代码特化（monomorphization），为每一种类型生成一份代码。好处是执行效率高，但是会带来额外的冗余代码，使二进制文件变大（bloat）。

2. 基于`dynamic 
dispatch`的泛型，类似于java和go的`interface`。在运行期查找虚表（vtable）来选择执行的方法。好处是使用灵活，但是性能肯定比static dispatch来的差。本篇着重介绍这一种泛型。

<hr/>

* Trait Object

 rust的`dynamic dispatch`实现都是基于一种叫做`trait object`的类型来实现的。先看一个例子：

```rust
    trait Object {
        fn dood(&self) -> int {
            1i
        }
    }
    impl Object for int {}
    impl Object for uint {}
    fn main() {
        fn gimme_an_object(i: &Object) {
            println!("{}", i.dood());
        }
        gimme_an_object(&2i);  // OUTPUT: 1
        gimme_an_object(&3u);  // OUTPUT: 1
    }
```

`gimme_an_object`函数这里发生了什么？
可以看到，`gimme_an_object`需要传入一个&Object类型的参数。就是说，`gimme_an_object`函数的参数i是一个实现了Object这个trait的引用类型。所以我们无论喂给它了一个&int或一个&uint，它都能完成调用。因为之前的两个`impl`已经为`uint`类型和`int`类型实现了`Object`这个`trait`。
在这一点上，rust的trait和go的interface很相似。我们只需要传入一个接口，函数就能完成工作，为不用管传入的参数到底是什么类型。
但是这里有一个细节需要注意：为什么要写`&Object`，写成`fn gimme_an_object(i: Object)`不行吗？
答案是不行。有人可能很奇怪，为什么我在go里面直接写interface就没问起，rust里面却必须要加个引用呢？
原因有两个：

1. 
因为按照rust的设计用途，它可以做底层开发，也可以做上层开发。因此内存布局要尽可能的”raw“。所有的数据都是赤裸裸的躺在堆上或栈上。因此一个Object的大小是不确定的。比如你可以为一个i8实现Object，再为一个u64实现Object。它们都能被当错参数传进`gimme_an_object`，但是显然他们的大小是不一样的（不考虑内存对齐）。对于动态长度的类型，显然没法在栈上分配空间，因为他们是编译时位置长度的。所以要用一个指针指向某个实现了trait的对象。因为指针是编译时大小已知的。
同理，像go、java也不可能绕过这个限制，毕竟他们不是黑魔法。之所以他们能直接写`func(i 
interface{})`的原因，是因为它们的interface自己就是一个指针。他们没有写嵌入式的负担，又有GC的照顾，自然可以肆无忌惮的用指针来指向一个类型并且把一切都隐藏起来就好像interface里的数据真真切切就在那儿一样。其实只是个indirection而已。
2. rust有三种原生指针，&、Box和*。无论哪一种都可以作为trait 
object的indirection，因此要是用interface一统江湖，不再写&，必然导致灵活性下降。无论用哪一种作为trait  
object的默认指针都有失偏颇。

* trait object的编译器魔法。

在rust里，所有的指针都是一个字长。比如64位机器上，&1i的大小就是64个bit。
但是在trait object中，rust编译器会隐式的把指针转换为一个胖指针。

```rust
    // in core::raw::TraitObject
    struct TraitObject {
        data: *mut (),
        vtable: *mut (),
    }
```

也就是说，所有的TraitObject大小其实都是两个字长。第一个指向数据，第二个指向虚函数表。这点和go的interface其实是一模一样的。

* trait safety

对于trait object，rust还有一个限制：只有safe的trait才能被用作trait object。
什么叫safe的trait呢？
因为有些trait会返回一个self类型，比如：

```rust
    trait RetSelf {
        fn ret_self(&self) -> Self;
    }
```

如果impl给了int，那么ret_self方法的返回值就是一个int，要是impl给了f64，那么返回值就是一个f64.这就意味着代码诸如：

```rust
    fn unsafe_object(i: &RetSelf) {
        let c = i.ret_self();
    }
```

是无法编译的，因为无从知道c的大小。因此在rust里面，只有不带有fn() -> 
Self类型的方法的trait才叫safe的trait，只有safe的trait才能被用作trait object。这也是为什么rust有很多trait xxxx， 
trait XXXXEXT。因为XXXX是safe的object，而trait 
XXXXEXT里面包含了带有返回Self的方法。如果把两者合并为同一个trait，意味着trait XXXX将不能再用于trait 
object。因此必须用两个trait来吧unsafe的方法隔离开。比如常用的Iterator 
trait就是如此。它从以前的一个trait变成了如今的interator和iteratorExt.

