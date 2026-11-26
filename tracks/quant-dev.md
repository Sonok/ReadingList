# Quant dev

C and C++ for building trading systems, read from the memory model up.

- [~] **The C Programming Language, 2nd edition** by Brian Kernighan and Dennis Ritchie (Tier 1)
  The memory model underneath C++: pointers, arrays, and how data is laid out. Read first because layout decides real
  performance in ways big-O hides. For a few hundred elements, an array's O(n) insert is a memmove over contiguous memory
  and often beats a skip list's pointer chasing and allocations.
  Status: page 116 of 238 (48%), section 6.2 Structures and Functions. Chapters 1 to 5 done.
- [~] **A Tour of C++** by Bjarne Stroustrup (Tier 1)
  Fast, authoritative overview of modern C++. Next after K&R.
  Plan: one pass. Chapters 1 to 8 (core language) at one chapter per sitting with a small program each. Chapters 9 onward
  (standard library) at two per sitting, with one Codeforces problem solved using that chapter's library feature.
  Status: page 5 of 226, section 1.4.
- [ ] **Introduction to C++ for Financial Engineers: An Object-Oriented Approach** by Daniel J. Duffy (Tier 3)
  C++ applied to pricing and numerical methods. Read after A Tour of C++.

Dated entries are in the [reading log](../log.md).
