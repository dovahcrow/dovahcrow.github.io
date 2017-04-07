---
categories:
- post
- rust
tags:
- compiler
date: 2015-11-04T11:54:16+08:00
title: Rust Compiler Plugin
summary: >
  We can use compiler plugin in rust compiler pipeline in order to enhance the grammar.
---

rust 提供了一个很强大的编译时功能：自定义编译器插件。

通过向编译器register一个函数作为入口，它可以在lint时期把ast作为register的那个函数的一个参数来invoke。也就是说，通过编译器插件，我们可以做很多强（wei）大（suo）的事情。

<!--more-->

* 例子1：[rust-chamber](https://github.com/brson/rust-chamber)

chamber是一个语言级别的sandbox(其实是一个rustc的包装)，可以防止你的语言中出现不安全的code。目前它的功能很简单，一旦发现你的code里面有使用了unsafe，或者开启了编译器feature(#![feature()]), 
或者使用了不安全的crate（比如intrinsic）编译就会通不过。怎么实现的呢？其实很简单。下面贴上核心代码：
<!--more-->
```rust
fn check_expr(&mut self, ctx: &Context, e: &ast::Expr) {
	match e.node {
    // Don't warn about generated blocks, that'll just pollute the output.
        ast::ExprBlock(ref blk) if blk.rules == ast::UnsafeBlock(ast::UserProvided) => {
	        ctx.span_lint(CH_UNSAFE_BLOCK, e.span, "chamber: `unsafe` block");
        }
        _ => ()
    }
}
```
context是用来控制编译器行为的。e是传入的expression的ast表现形式。check_expr的作用就是对每个传入的expression进行判断，如果是unsafe 
block，就报错。

* 例子2：[spellck](https://github.com/huonw/spellck)

这是一个基于字典的拼写检查插件。通过字典，可以将代码中的单词拼写错误在编译器进行提示。麻麻再也不用担心我在代码里面打错别字啦！

* 例子3：[regex](http://static.rust-lang.org/doc/master/regex/index.html)

重量级插件：rust官方正则表达式库。什么？正则表达式和插件有什么关系？
这里说的是rust的regex！宏。众所周知，正则表达式需要进行编译。比如python的re.compile，go的regexp.Compile等等。正则表达式需要在运行时，将一个正则表达式字符串编译成正则表达式虚拟机上的指令。所以正则表达式其实是一个内嵌在语言内部的虚拟机语言。
既然正则表达式在运行时才能够进行编译，并且只是编译成虚拟机指令，那么它的效率必然会比原生代码低很多。那么我们能不能把这个过程提前到编译时呢？正则表达式规则是通过字符串的形式来书写的，在编译时无法确定它的内容（字符串是可变的）。所以在一般的语言中确实做不到编译时处理正则表达式。但是通过rust的编译器插件，我们可以实现对常量字符串表达式进行编译时的正则表达式编译。
regex插件在编译时会把相应的正则表达式编译成rust代码，所以在运行时完全没有用到正则的虚拟机和指令。因此执行速度非常快。但唯一的缺点就是如果生成太多的正则表达式，那么编译出来的二进制文件会变得非常大。（毕竟是吧正则表达式展开成了大量的rust代码。）


================================================================

介绍到此为止，下面是教程。
首先，你需要引入一个编译器特性， `plugin_registrar`
在代码开头加上
`#![feature(phase, plugin_registrar)]`
使用phase特性是因为我们需要一些在rustc里面的宏来帮忙。可以省去一些代码。

	#[phase(plugin, link)] // Load rustc as a plugin to get lint macros
	extern crate rustc;
	extern crate syntax;
	
	use rustc::lint::{Context, LintPass, LintArray};
	use rustc::plugin::Registry;
	use syntax::ast;

引入一些crate。
phase是一个编译器特性。其中plugin的意思是把crate当作插件插入到当前代码（为了引入其中的macro。因为macro不能像传统变量那样采用use来引入），link的意思是把该crate连接到此文件（crate默认其实有一个link的feature）。
接下来是建立一个lint的属性：

	pub static mylint: &'static rustc::lint::Lint = &lint_initializer!(mylint, Deny, "abrakadabra");

我们把它起名字叫做mylint。默认级别是Deny, 
并且把它绑定到了mylint这个static变量上（需要注意的是，Lint变量必须是static的）。描述随便写了点。
其中，lint的级别有四个，分别是Allow,Warn,Deny,Forbid.其中Forbid和Deny的区别在于，如果是Deny，那么在源代码里面，使用者可以通过#[allow(myliny)],#[warn(mylint)]进行lint级别更换。比如从禁止一个特性转变为只是警告（P.S. 
那就没用啦！程序员从来不看警告）。但是如果设置为Forbid级别，那么用户就无论如何也没办法改变你的lint级别了。比如上面的例子，chamber里面，作者就使用了Forbid级别。
然后我们新建一个LintPassObject;

	struct MyLintPass1;

要成为一个LintPassObject，还需要一个Trait的帮助。

	impl LintPass for MyLintPass1 {
	    fn get_lints(&self) -> LintArray {
	        lint_array!(mylint)
	    }
	}

我们需要为我们的LintPassObject实现LintPass这个Trait。
LintPass这个Trait有很多方法，但是我们只要实现get_lint这一个就可以了。`get_lint`这个方法的含义就是把我们前面建立的那个`mylint`这个`lint`和我们的`LintPassObject`关联起来。`lint_array`这个宏的作用就是生成一个`static`的`lint 
array`。
然后，最后一件事，就是把我们的`LintPassObject`注册进编译器。

	#[plugin_registrar]
	pub fn plugin_registrar(reg: &mut Registry) {
	    reg.register_lint_pass(box MyLintPass1);
	}

只要在一个函数上面打上	

	#[plugin_registrar]

就告诉了编译器，下面那个函数，是要cha进你身体里的！
然后我们就完成了一个最简单的编译器插件。把它编译成dylib（注意必须是动态链接库，不能编译成rlib）
在需要使用它的地方写上

	#![feature(phase)]
	#[phase(plugin)] extern crate plugin;

就ok啦！
于是我们完成了一个什么都不做的编译器插件。

接下来我们给我们的插件添加点小功能：阻止编译啊哈哈哈！
在这个地方，我们加一个函数实现

	impl LintPass for MyLintPass1 {
	    fn get_lints(&self) -> LintArray {
	        lint_array!(mylint)
	    }
	    fn check_crate(&mut self, ctx: &Context, crt: &ast::Crate) {
	      ctx.lint(mylint, "deliberate fail!")
	    }
	}

于是除非你在main函数打标记#[allow(mylint)]否则编译就是通不过啦啦啦

