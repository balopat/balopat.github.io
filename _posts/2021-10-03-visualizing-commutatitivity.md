---
title: Visualizing commutative structure in groups
subtitle: Introducing the commutativity plot to explain basic concepts related to commutativity
layout: default
date: 2021-10-20
keywords: grouptheory
published: true
---

## Introduction

I built a simple visualization tool, the commutativity plot, that I used to better understand commutativity in finite groups as I was learning about group theory this semester. By the end of this post, I aim to summarize a couple of concepts leading up to two theorems illustrated with this visualization. Namely, we'll touch on group action, orbits and stabilizers of an element, the permutation representation of groups, conjugation, conjugacy classes, centralizers, and we'll derive the formula for the number of conjugacy classes. We will also look at why the probability that two randomly picked elements commute in a finite group is a maximum of 5/8 in non-abelian groups, which I find fascinating.

Disclaimer: the function implementation and Mathematica syntax used is very naive, and blows up with larger groups. I am open to PRs, contributions, suggestions for improvements!



## Groups acting on sets

One of the most important things you can do with a group is to have it act on a set. The group action has to be valid operations on the set. For example, if the set is the group itself, the action can be left/right multiplication or conjugation (defined later) as well. When we're talking about an action of an element $g$ of the group $G$ on a set element $a$ in abstract, i.e. without specifying exactly what we mean, we denote it by $g \centerdot a$. 

If we apply a group action defined by all elements of $G$ on an element $a$, we get a set: $ O_a = \\{ g \centerdot a \lvert g \in G \\} $, the [orbit](https://proofwiki.org/wiki/Definition:Orbit_(Group_Theory)) of $a$. The elements in $G$ that keep $a$ the same are called the _stabilizer_ of $a$ in $G$, denoted $G_S(a)=\\{g \in G \lvert g \centerdot a = a\\}$. The stabilizer of any element is a subgroup of $G$. In fact the orbit of $a$ is an equivalence class for $a$, and the group action divides $G$ into disjoint equivalence classes. It is also provable that the order of (the number of elements in) the orbit equals to the [index](https://en.wikipedia.org/wiki/Index_of_a_subgroup) of the stabilizer $\lvert G : G_a\lvert$.


## Permutation representation 

By [Cayley's theorem](https://en.wikipedia.org/wiki/Cayley%27s_theorem), every group of order $n$ is isomorphic to some subgroup of $S_n$, the symmetric group of order $n$. We are going to assume that for the group in question you can generate the permutation representation, specifically the [permutation cycle notation](https://mathworld.wolfram.com/PermutationCycle.html) of the elements. For example, for the quaternion group $Q_8$, we can list the elements of the group itself using the [`Quaternions` package](https://reference.wolfram.com/language/Quaternions/tutorial/Quaternions.html): 

```mathematica
<<Quaternions`
(* Code to generate a group based on its generators and composition 
rule, this is brute force, can easily blow up if your generators are 
not closed under multiplication, or are too big *)

GenerateGroupElements[generators_, compose_] := 
  FixedPoint[Union[#, compose @@@ Tuples[#, 2]] &, generators];

(* Q8 group = <i,j,k>, composition: quaternion product *)

quaternionGroupElements = GenerateGroupElements[
   
   {Quaternion[0, 1, 0, 0],  (* i *)
   Quaternion[0, 0, 1, 0],   (* j *)
    Quaternion[0, 0, 0, 1]}, (* k *)
   (#1 ** #2) & (* quaternion product *)
   ];


(* A nice example of Cayley's theorem, where we are acting on G by itself with 
left multiplication *)

quaternionGroupPermutations = (el = #;
     FindPermutation[
      quaternionGroupElements, (el ** #) & /@ 
       quaternionGroupElements]
     ) &  /@ quaternionGroupElements;

(* storing the result in a PermutationGroup object *)
QuaternionGroup = PermutationGroup[quaternionGroupPermutations ]

```

The above results in:

{% raw %}
```mathematica
PermutationGroup[{Cycles[{}], 
  Cycles[{{1, 2}, {3, 4}, {5, 6}, {7, 8}}], 
  Cycles[{{1, 4, 2, 3}, {5, 8, 6, 7}}], 
  Cycles[{{1, 3, 2, 4}, {5, 7, 6, 8}}], 
  Cycles[{{1, 6, 2, 5}, {3, 7, 4, 8}}], 
  Cycles[{{1, 5, 2, 6}, {3, 8, 4, 7}}], 
  Cycles[{{1, 8, 2, 7}, {3, 6, 4, 5}}], 
  Cycles[{{1, 7, 2, 8}, {3, 5, 4, 6}}]}]
```
{% endraw %}

The permutation representation for groups is akin to the matrix representation of operators on a vector space in a given basis. We can see in this chosen labeling that $1$ keeps the elements in place, $-1$ is a quadruple of transpositions (swaps), and $i$ permutes $12345678$ into $43128756$.

One thing we get with this representation is stable, deterministic ordering between permutations, which will allow for seeing subgroup structure clearly in larger groups.


## Conjugacy classes 


Fun things happen when a group $G$ acts on itself!
Two elements, $g, h \in G$ commute when $hg = gh$. This is the same as saying $g=h^{-1}gh$, i.e. that $g$ is fixed by conjugation by $h$. 


If we have $G$ act on itself by conjugation, the orbit of an element $g$, a.k.a the disjoint equivalence class, is called the [conjugacy class](https://en.wikipedia.org/wiki/Conjugacy_class) of $g$. The stabilizer subgroup under conjugation for $g$ is the subgroup that fixes $g$ by conjugation. What does that mean? It means that it's all the elements $g$ commutes with. There is a special name for that: the [centralizer](https://mathworld.wolfram.com/Centralizer.html) of $g$ in $G$, denoted $C_G(g)$. The elements that commute with everything are called the [center](https://en.wikipedia.org/wiki/Center_(group_theory)) of $G$, $Z(G)$ - it is easy to see that the center is the intersection of all the centralizers and hence it is also a subgroup.

It is easy to prove (p 125 in {% cite dummit2003abstract %}) that conjugation preserves the length of the cycles of a permutation, i.e. all the conjugates within a conjugacy class have the same cycle lengths. In Mathematica, you could write a function called `CycleLengths` that does this calculation.

{% raw %}
```mathematica

In[1]:= CycleLengths[c_]:=Sort[Length/@c[[1]]];
CycleLengths[Cycles[{{1,2},{3,4},{5,6},{7,8}}]]
CycleLengths[Cycles[{{1,2},{3,4,5}}]]
Out[2]= {2,2,2,2}
Out[3]= {2,3}
```
{% endraw %}

However, even though elements in the same conjugacy class have the same cycle lengths, it doesn't necessarily work the other direction. To see this there are two examples in mind: abelian groups and the $Q_8$ quaternion group. 

As everything commutes with everything in abelian groups, the conjugacy class for each element is going to contain only that element. But in a cyclic group of prime order for example all non-trivial elements are of order $p$, their permutation representation looks like $(1234...p)$. How is that possible? Well, there are no other elements to conjugate them into each other...or to put it another way all elements fix each other by conjugation.

In the quaternion group $Q_8$, $i, j, k$ have the same cycle lengths but you can only get as far as an element and its inverse in the conjugacy classes. There are no elements in the group that can do the conjugation. 

To summarize - conjugacy classes split up $G$ into disjoint sets, and while cycle lengths are the same within a conjugacy class, the property of being in a conjugacy class is inherently connected to the group you are in. 

## The commutativity plot: commuting visibly

To visualize all the ideas above, I coded up a function called `CommutativityPlot` in [this gist](https://gist.github.com/balopat/3e363e7ca4492fd77703ff80a14830bf). If we order the elements of the group by their conjugacy class and then their natural sorting order (defined by Mathematica), and we plot whether they commute or not, we'll get a graph plot like this for our quaternion group, $Q_8$: 


<center>
<img src="/assets/images/q8-commute.png" width="60%"/>
</center>

Let's dissect this! 

Each row and column contains the elements that are either commute (blue) or don't commute (red) with the given element corresponding to that row. The blue squares in a row (or column) are the centralizer $C_G(g)$ for each $g$. If the full row (column) is blue, that means that the $g$ element is in the center, $Z(G)$.

We know that every element commutes with: 
- itself $\rightarrow$ the diagonal is always going to be blue
- the identity $\rightarrow$ the first row and column will always be blue

In the case of $Q_8$, some of the elements are not self-inverse, e.g. $i^{-1} = -i$, and we know that the elements commute with their inverse. In the current labeling, the inverses are next to each other, that's why we see the 2x2 blue squares on the diagonal.

Also, notice the yellow grid. As we organized the elements by conjugacy class, a conjugacy class will be a contiguous interval of rows and columns. The intersection of these regions is where the inter-class commutation relations are visible. We can see intra-class commutativity relations outside of the block diagonal squares. 

As I mentioned in the previous part, cyclic groups are abelian, every element commutes with each other, thus in the commutativity plot we will have
- a fully blue plot
- conjugacy classes of size 1.

As an example see below the (pretty boring) commutativity plot for the $C_4$ group.
<center>
<img src="/assets/images/c4-commute.png" width="60%"/>
</center>

## Number of conjugacy classes

Within a conjugacy class (i.e. between two yellow lines), the number of blue squares is going to be the number of elements in the group! Why? 

To see this, let's line up our concepts next to each other in the different "languages" we talk about them: 


| Conjugation                                                | Group acting on _itself_ by conjugation  | commutativity plot                                                            |
| ---------------------------------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------- |
| element $a \in G$                                          | the target $a \in G$ of the group action | a row / a column                                                              |
| centralizer of $a$, $C_G(a)$, things that commute with $a$ | stabilizer of $a$, $S_G(a)$              | the elements corresponding to the blue squares in a row / column              |
| conjugacy class of $a$                                     | orbit of $a$, $O_a$                      | the rows/cols within the same yellow grid interval as $a$'s row/col           |
| number of conjugates / size of conjugacy class             | size of orbit                            | the number of rows/cols within the same yellow grid interval as $a$'s row/col |
| number of conjugacy classes                                | number of orbits                         | number of yellow grid intervals                                               |


Now, the centralizer for each element is a subgroup, in fact, the stabilizer for the element when we consider the group acting on itself by conjugation. As we noted, the size of the orbit is exactly the index of the stabilizer, which means exactly that the blue squares will add up to $\lvert G \lvert$ within the yellow lines. In the case of $Q_8$ above, if we add up all the blue squares and divide it by $G$, then we get the number of conjugacy classes, which is 5!

Hopefully, now it is more clear why the equation holds for the number of conjugacy classes: 

{% katexmm %}
$$
k = \frac{\sum_{g \in G} |C_G(g)|}{|G|}
$$
{% endkatexmm %}

Another example is the Pauli group (or Heisenberg-Weyl group), which is of fundamental importance in quantum mechanics and quantum computing. It is generated by the Pauli matrices $X, Y, Z$: 

{% katexmm %}
$$
X = \begin{pmatrix} 0 & 1 \\
1 & 0
\end{pmatrix}
Y = \begin{pmatrix} 0 & -i \\
i & 0
\end{pmatrix}
Z = \begin{pmatrix} 1 & 0 \\
0 & -1
\end{pmatrix}
$$
{% endkatexmm %}

These 3 matrices generate 16 elements, so our permutation representation will be the result of permuting 16 symbols, they get pretty lengthy. 

<center>
<img src="/assets/images/pauli-commute.png" width="90%">
</center>

We can see that the center of the Pauli group is $\\{\pm I, \pm i I\\}$, each element there has its own conjugacy class, and then, interestingly each element has only one conjugate, which is -1 times the element itself.

## The probability that two elements commute

The commutativity plot almost intuitively leads to this question: how dense can the blue squares be? In probabilistic terms, the proportion of the blue vs the full area is equivalent to the probability that two random elements commute from $G$. Of course, we are interested in non-abelian groups, as abelian groups have a boring full-blue plot. In the case of $S_6$, the plot becomes very large (6! x 6!), but we can see that it is very sparse (also has some cool structure in there): 

<center>
<a href="/assets/images/s6-commute.png" target="blank"><img src="/assets/images/s6-commute.png" width="60%"/></a>
</center>

The Pauli group above and the quaternion group have much more blue in them. Let's quantify this probability exactly. 


```mathematica
CommutationProbability[group_] := 
 Count[Tuples[GroupElements[group], 2], 
   x_ /; 
    PermutationProduct[x[[1]], x[[2]]] == 
     PermutationProduct[x[[2]], x[[1]]]]/GroupOrder[group]^2
```

With the function above (again, very slow, brute force implementation, careful), we can see that our groups have the following probabilities of two of their elements to commute:

- abelian groups of course 100% 
- Symmetric group of order 6: 11/720 - pretty low!
- Quaternion group, Dihedral group of order 4, and the Pauli group: 5/8 

Can we go higher? It turns out that two random elements in a non-abelian group can't have more than a 5/8 chance to commute! 

The proof is relatively simple: given that the centralizer $C_G(g)$ for any element $g \in G$ in a non-abelian group is a proper subgroup, it can only be of order $\lvert G \lvert/2$ at most (due to [Lagrange](https://en.wikipedia.org/wiki/Lagrange%27s_theorem_(group_theory)) the subgroup's order has to divide the group's order). But, the same is true for the center of the group itself, $Z(G)$ is a subgroup of all the centralizers, and as such, it must be up to half the size of the centralizers, and as such, it must be that $\lvert Z(G) \lvert  \leq \lvert G \lvert /4$. We can see in the Pauli group that the center has 4 elements, out of the 16, we are hitting this limit. 

Now, let's use these bounds. We'll simply add all the blue squares - that's going to be all the orders of the centralizers of all the elements, and divide by all the squares, which is simply $\lvert G \lvert^2$.

{% katexmm %}
$$
p(g,h \in G \text{ commute}) = \frac{\sum_{g \in G} |C_G(g)|}{|G|^2}
$$
{% endkatexmm %}

For elements in the center, the centralizer is the group itself (they commute with every element), so we can separate those out from the sum: 

{% katexmm %}
$$
p(g,h \in G \text{ commute}) = \frac{\sum_{g \in Z(G)} |G|}{|G|^2} + \frac{\sum_{g \notin Z(G)} |C_G(g)|}{|G|^2}
$$
{% endkatexmm %}

Let's divide in with the order of $G$: 

{% katexmm %}
$$
p(g,h \in G \text{ commute}) = \frac{\sum_{g \in Z(G)} |G|/|G|}{|G|} + \frac{\sum_{g \notin Z(G)} |C_G(g)|/|G|}{|G|}
$$
{% endkatexmm %}

And let's use our bounds: $\lvert Z(G) \lvert / \lvert G \lvert \leq 1/4$ and $\lvert C_G(g) \lvert / \lvert G \lvert \leq 1/2$ for all $g \in G$: 

{% katexmm %}
$$
p(g,h \in G \text{ commute}) \leq \frac{\sum_{g \in Z(G)} 1 }{|G|} + \frac{\sum_{g \notin Z(G)} 1/2}{|G|} = \\
=\frac{|Z(G)|}{|G|}  + \frac{|G|-|Z(G)|}{|G|}1/2 = 1/2 + \frac{|Z(G)|}{2|G|} \leq 1/2 + 1/8 = 5/8
$$
{% endkatexmm %}

When I first saw this, my mind was blown - group theory seems like this area of infinite possibilities, but it seems like it contains a lot more structure than we'd think at first.

## Conclusion

We demonstrated a simple tool to visualize commutation relationships within finite groups. It leverages the permutation representation of groups, which allows for a natural ordering that simplifies grouping conjugation classes together. We demonstrated proofs aided by this visual language for two theorems. I hope you enjoyed it, learned something from it! 


### Further things to explore and improve

This is probably just the tip of the iceberg. If I had an infinite amount of time I would explore a couple of ideas:
- Are these "game-of-life" type structures/patterns that show up in the plot of any interest? Can we derive anything from patterns formed on the plot from this particular ordering? Can other orderings result in different insights?
- What else can we visualize in this plot: 
   - Can we represent normalizers? 
   - Can we represent subgroup structure in the commutation plot? 
- Improve the tool: 
   - Make the tool interactive
   - create a Python/Javascript version of it, so it doesn't depend on non-opensource software

If you find issues with the post, please open an issue or PR to fix it!

## Acknowledgment 

Big thank you to Prof. Nathan Carter for [his comments](https://github.com/nathancarter/group-explorer/issues/19) on this blogpost and finding a bug in the original proof. 

## Comments

Comments are provided by giscus and Github Discussions. You will have to login with your Github account to comment.



<script src="https://giscus.app/client.js"
        data-repo="balopat/balopat.github.io"
        data-repo-id="MDEwOlJlcG9zaXRvcnkxODEyMzUxOA=="
        data-mapping="number"
        data-term="1"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="light"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>