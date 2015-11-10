---
draft: false
title: "说说Phantom Type"
description: "Lets talk about phantom typen"
date: "2015-11-02T10:36:23+08:00"
categories:
- "post"
tags:
- "rust"
- "phantom type"
#cardimagelg: "/images/default.jpg"
#cardimagesm: "/images/default.jpg"
cardbackground: '#3B4D7D'
author:
    name: "wooya"
    description: "The fortune teller"
    website: "http://wooya.me"
    email: "doomsplayer@gmail.com"
    github: "https://github.com/doomsplayer"
    image: "/images/avatar-64x64.png"
---

在具有高级类型系统的语言里面，有一种类型标记的用法叫phantom type,
比如[Haskell语言](http://www.haskell.org/haskellwiki/Phantom_type)。这种用法有个很有意思用途：用来做编译时的类型检查，并且对于编译后的代码来说，完全没有任何的副作用。

举个例子，在做几何运算的时候，我们会碰到运算时变量单位的问题。
<!--more-->
```rust
#[deriving(Show)]
struct Length<Num>(Num);

type Meter = f64;
type Inch = f64;

let a: Length<Meter> = Length(5.0 as Meter);
let b: Length<Inch>  = Length(7.0 as Inch);

impl<Num> Add<Length<Num>,Length<Num>> for Length<Num> where Num: Add<Num,Num> {
  fn add(self, rhs: Length<Num>) -> Length<Num> {
    Length(self.0 + rhs.0)
  }
}

println!("{}", a + b);
```

在上面的代码中，我们有一个很明显的bug,单位为米的a竟然和单位为英寸的b进行了相加。要是在业务逻辑中出现这么一茬，肯定很难debug，因为从语法上来讲，完全没有问题啊！

现在我们来引入一种类型系统的trick，叫做phantom type。 

```rust
mod unit {
  #[deriving(Show)]
  enum Meter {}
  #[deriving(Show)]
  enum Inch {}
}

#[deriving(Show)]
struct Length<Unit,Num>(Num);

let a: Length<unit::Meter,f64> = Length(5.0);
let b: Length<unit::Inch,f64> = Length(7.0);

impl<Unit,Num> Add<Length<Unit,Num>,Length<Unit,Num>> for Length<Unit,Num> where Num: Add<Num,Num> {
  fn add(self, rhs: Length<Unit,Num>) -> Length<Unit,Num> {
    Length(self.0 + rhs.0)
  }
}
println!("{}", a + b);
```

为了打印方便，加了一些`#[deriving(Show)]`。 我们给Length类型加上了一个`Unit	
`的类型标记。但是，Unit却没有出现在任何有值的地方，它仅仅是作为了一个类型标记存在着。所以，我想这也是为什么它叫`phantom 
type`的原因吧。

编译上面那段的代码，编译器会给你报错：

```rust
error: mismatched types: expected `main::Length<main::unit::Meter, f64>`, found `main::Length<main::unit::Inch, 
f64>` (expected enum main::unit::Meter,found enum main::unit::Inch)
```

编译器说： a是`Length<Meter,f64>`, b是`<Inch，f64>`,它们类型不相容。

仅仅通过增加一个额外的类型标记，我们就实现了让编译器自动给我们检查单位的方法，而且这种`phantom 
type`的小trick，不会带来任何的运行时负担。在编译完毕后，它们就被一并的擦除了。

其实这是一种对现实中单位制的模拟。平时我们写的时候一般写 
1m，2mm之类。其实当我们写下了1m这个数字的时候，其实着我们写下了两个东西，作为数字的1和作为单位的m。单独拿出来，对于数字1来讲，他没有任何的意义。可以随便对他加上其它的数字；对于m来说，它仅仅是个单位，同样也没有意义。但是1m结合起来，m就为1赋予了class信息，改变了它的运算规则。`phantom 
type`在此，就起到了这个量纲作用。

除了用来作为数字的单位以外，还有一个比较好用的地方是作为用户输入安全性的标记（这和rust着重安全是遥相呼应啊）。
众所周知，web安全有很大一部分问题，是因为没有对用户输入做检查。一个安全的系统应该对于所有的用户输入采取不信任的态度，应该由代码对其进行检查。
但是在开发的时候，可能由于程序员水平问题，或者一时疏忽等原因，往往会忘记检查。这就为系统埋下了很大的隐患。
利用`phantom type`我们可以为所有的string打上tag，让编译器来替我们进行检查。

```rust
enum Trusted {}
enum UnTrusted {}
struct UserInput<T>(String);

let a: UserInput<Trusted>("safe".to_string());
let b: UserInput<UnTrusted>("SQL Injectiong is here!!!".to_string());

insert_into_database(a);
insert_into_database(b); // 编译通不过
```

假定我们的`insert_into_database`接受一个`UserInput<Trusted>`作为输入。那么那个b，我们是无论如何也无法存入数据库的，必须要我们进行显式的检查，将其转换为UserInput<Trusted>,否则编译必定报错。这样系统的安全性就大大的加强了。
