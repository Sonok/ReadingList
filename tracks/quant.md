# Quant dev / quant research

## Reading

- [~] **The C Programming Language, 2nd edition** by Brian Kernighan and Dennis Ritchie (Tier 1)
  Added 2026-09-29 after losing an Optiver interview on a question about this. Moved to Tier 1 and to the front of the
  queue on 2026-09-29 on my dad's advice: read K&R before A Tour of C++. The lesson: an array's O(n) insertion is a
  memmove over contiguous memory that runs at many GB/s. For a few hundred elements it is often faster than a skip list's
  pointer chasing, allocations, and random-level logic. Big-O hides constant factors and cache behavior. Read K&R for the
  memory model, pointers, and arrays; the cache-locality half of the lesson belongs to the low-latency book in the career track.
  Log: 2026-09-29 started, read to page 13. Currently on page 13, chapter 1.
- [~] **A Tour of C++** by Bjarne Stroustrup (Tier 1)
  Fast, authoritative overview of modern C++. Second priority overall, after K&R. Also pays off directly in competitive programming.
  Plan (started 2026-09-28): one pass, no re-reading. Chapters 1 to 8 (core language) at one chapter per sitting with a
  small program each. Chapters 9 onward (standard library) at two chapters per sitting, skim, and solve one Codeforces
  problem using that chapter's library feature. Done means every chapter read once, not mastered. Keep as a reference after.
  Log: 2026-09-28 pages 1 to 3. 2026-09-29 page 4. Currently on page 5, section 1.4.
- [~] **A Practical Guide to Quantitative Finance Interviews** by Xinfeng Zhou (Tier 1)
  Status (2026-09-28): ch 2 brainteasers mostly done, ch 4 probability a lot done. Not started: ch 3 calculus and linear
  algebra, ch 5 stochastic processes, ch 6 finance, ch 7 algorithms and numerical methods.
  Plan: one problem a day from the unread chapters, alongside the C++ book. Order: finish ch 4, then 3, 7, 5, 6.
  Brainteasers, probability, stochastic calculus basics, and finance questions in the form they show up in quant interviews.
- [ ] **An Introduction to Statistical Learning with Applications in Python** by Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, and Jonathan Taylor (Tier 2)
  Applied stats and ML foundations for quant research: regression, classification, resampling, tree methods, unsupervised learning.

### Interview prep (Tier 3)

- [ ] **Quant Job Interview Questions and Answers** by Mark Joshi, Nick Denson, and Andrew Downes (Tier 3)
  Second interview book after Zhou. Heavier on option pricing and stochastic calculus.
- [ ] **Heard on the Street: Quantitative Questions from Wall Street Job Interviews** by Timothy Falcon Crack (Tier 3)
  Classic bank of quant interview questions. Overlaps with Zhou and Joshi, so skim for what's new.
- [ ] **An Interview Primer for Quantitative Finance** by Dirk Bester (Tier 3)
  Shorter primer on the interview process and question types.
- [ ] **The Theory of Poker** by David Sklansky (Tier 3)
  Expected value, pot odds, and decision-making under uncertainty. Common background for trading-firm interviews.

### Foundations (Tier 3)

- [ ] **Introduction to Mathematical Statistics, 7th edition (2012)** by Robert V. Hogg, Joseph McKean, and Allen T. Craig (Tier 3)
  Proof-level probability and statistics. The theory underneath ISL.
- [ ] **Python for Data Analysis, 3rd edition** by Wes McKinney (Tier 3)
  pandas and NumPy from the pandas author. Practical tooling for research work.

### Finance and markets (Tier 3)

- [ ] **Paul Wilmott on Quantitative Finance** by Paul Wilmott (Tier 3)
  Broad, readable treatment of derivatives pricing and quant modeling. Reference more than cover-to-cover.
- [ ] **Trading and Exchanges: Market Microstructure for Practitioners** by Larry Harris (Tier 3)
  How markets actually work: order types, market makers, liquidity, price formation. Essential context for trading-side roles.
- [ ] **Introduction to C++ for Financial Engineers: An Object-Oriented Approach** by Daniel J. Duffy (Tier 3)
  C++ applied to pricing and numerical methods. Read after A Tour of C++.

## Done

_(none yet)_
