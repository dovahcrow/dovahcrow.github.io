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
date: 2015-11-04T11:53:30+08:00
title: rust inline asm
---

rust和c/c++一样,可以内联汇编.语法和c/c++的内联汇编大致一样.只有几个细节稍有不同.

首先,需要开启一个特性 `#![feature(asm)]`

然后在`asm!`宏里面写汇编即可.

<!--more-->

格式是:

	asm!(assembly template
 	  : output operands
	   : input operands
	   : clobbers
	   : options
	   );

大致和c/c++相同.其中有几个不同点:

在最后一段用来声明已经使用过的寄存器的那一段(clobbers)下面还可以跟一段option段.备选项有:"intel"表示采用intel汇编而不像c那样用AT&T汇编."volatile",和c里面的`__asm__volatile__`一样."alignstack",让编译器自动插入对齐栈的代码(因为有些指令集需要对齐栈,比如SSE指令集).
在填充模版的时候,变量用$0,$1来表示,而不是c的%1,%2来表示.
立即数用`$$`表示,`$$1`就是1.
寄存器直接用%来表示,%eax表示eax寄存器
模版里面多条指令用分号(;)来分割,而不是c的"\r\n"
声明clobber的时候直接写`eax`,不用像C那样写`%eax`
记得`asm!`的时候要外面套`unsafe`块
intel语法我没有试过.所以无从比较语法区别:(

下面附上我的一个小例子,用汇编+偏移量来访问数组.

```rust
#![feature(asm)]
	
fn main() {asm();}

#[cfg(target_arch = "x86_64")]
fn asm() {
	use std::mem::transmute;
	use std::rand::random;
			
	let array: &[u64] = &[random(),random(),random(),random()];
	
	let address = unsafe { transmute::<_, (i64, i64)>(array).0 };
	
	for offset in 0u64..4 {
	 	let ret: u64;
	 	unsafe {
	 		asm!(
	 			r"
	 			mov ($1, $2, 8), %rax;
	 			mov %rax, $0;
	 			"
	 			: "=r"(ret)
	 			: "r"(address), "r"(offset)
	 			: "rax"
	 			:
	 			);
	 	}
	 	println!("在第{}号位上的元素是{}", offset, ret);
	 }
}
```

