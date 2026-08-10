# Context for Claude Code: Hybrid Merge–Insertion Sort (CS Extended Essay)

Give this whole file to Claude Code before asking it to build/extend the hybrid algorithm. It consolidates everything in the CS EE project folder — the written essay content, the source list, the plan/to-do docs, and the current code — so Claude Code doesn't need to guess at context.

## 1. Who this is for

Manuel Zampogna, 17, Year 12 IBDP, International School of The Hague. This is his Computer Science HL Extended Essay, first year doing CS. Supervisor: Mr. Hare. Code should stay at a believable first-year-CS student level — plain, commented, not over-engineered or "too professional."

## 2. Research question

"To what extent does the cutoff threshold affect the performance and cost efficiency of a hybrid merge-insertion sort algorithm for cloud-based data processing?"

Proposal approved 12 Jan 2026. Essay limit: 4,000 words, MLA 9 citations. Final submission: early November 2026.

## 3. The essay's argument so far (from the written Introduction, latest draft v4, 28 Jul 2026)

This is the reasoning the code and experiments need to support — Claude Code should treat this as the "why" behind every task below.

- Sorting is fundamental to computing (search ranking, e-commerce listing, messaging order, etc.); even small speed gains compound at scale.
- Algorithm efficiency is usually judged with **Big O notation** — a machine-independent count of how the number of steps grows with input size `n`. Two simplification rules: constant multipliers are dropped (3n and 5n are both O(n)), and smaller terms are absorbed by larger ones (n² + n + 12 → O(n²)). Common classes, fastest to slowest: O(1), O(log n), O(n), O(n log n), O(n²).
- Merge sort is O(n log n) worst case; insertion sort is O(n²) worst case — so Big O favors merge sort on large inputs.
- **But Big O is asymptotic** — it ignores fixed/constant costs (function calls, memory allocation, copying). On small inputs those constant costs dominate, so insertion sort can beat merge sort in practice despite "worse" Big O. This mismatch between theoretical and measured performance is the whole reason hybrid sorts exist, and it's the central argument of the essay.
- A **hybrid sorting algorithm** combines two strategies and switches between them based on the size of the piece of data currently being sorted. The canonical example is **Timsort** (Python's and Java's default sort) — fundamentally merge sort, but it switches to insertion sort once a subarray drops below a fixed **cutoff threshold**.
- The gap in the literature this essay targets: textbooks say insertion sort should be used "on small arrays" but never define "small." Empirical studies tend to compare whole algorithms against each other rather than tune the threshold *inside* a hybrid. Cook and Kim (1980) show combining insertion sort with a merge step beats either alone, but never establish the switch-over size — that's specifically the gap this essay fills.
- **Practical/commercial motivation:** cloud platforms like AWS Lambda charge per GB-second of compute. A function that runs 15% faster costs 15% less. At the scale of e-commerce ranking, log analytics, or search backends, small per-run efficiency gains compound into real savings. This is why the research question has a "cost efficiency" half, not just a performance half.

### 3.1 Insertion sort (as described in the essay)

Works like sorting a hand of playing cards — take each new item and slide it into place among the already-sorted items to its left, shifting larger items right to make room. Worst case O(n²) (Cormen et al. 18) — impractical on large inputs, but simple, low memory overhead, very little setup cost, and **adaptive** (fast on data that's already mostly sorted). These properties are exactly why it's used for the small pieces inside a hybrid.

### 3.2 Merge sort (as described in the essay)

Divide-and-conquer: repeatedly split the array in half until each piece is a single item (trivially sorted), then merge pairs of sorted pieces back together by repeatedly taking the smaller front item. Worst case O(n log n) (Cormen et al. 30) — on 1,000,000 items, roughly 50,000× fewer operations than insertion sort's worst case. Overhead: relies on recursion and uses extra memory for temporary arrays during merging — overhead that can outweigh its algorithmic advantage when the input is small. That's the opening the hybrid exploits.

## 4. Key sources (annotated bibliography, MLA 9 — from `EE_Key_Sources.docx`)

Claude Code should keep code/comments consistent with how these sources are used, and should not introduce claims that contradict them:

1. **Cormen, Thomas H., et al. *Introduction to Algorithms*. 3rd ed., MIT Press, 2009.** — Source for Big O definitions and complexity of merge/insertion sort. Also the source of the textbook claim "use insertion sort on small arrays" that the essay tests.
2. **Khairullah, Md. "Enhancing Worst Sorting Algorithms." *International Journal of Advanced Science and Technology*, vol. 56, 2013, pp. 13–26.** — Shows insertion sort can be sped up by cutting comparisons/shifts; evidence that insertion sort's real speed depends on small operations Big O ignores. Doesn't cover merge sort.
3. **Cook, Curtis R., and Do Jin Kim. "Best Sorting Algorithm for Nearly Sorted Lists." *Communications of the ACM*, vol. 23, no. 11, 1980, pp. 620–624.** — Shows combining insertion sort with a merge step beats either alone on nearly sorted lists — close to the hybrid idea — but never pins down the switch-over size. That's the specific gap this essay fills.
4. **Peters, Tim. "listsort.txt." *CPython Source Documentation*, Python Software Foundation, 2002.** — Design notes for Timsort. Proves real systems already use a fixed threshold, which is why choosing that threshold is a real, non-trivial decision.
5. **Astrachan, Owen. "Bubble Sort: An Archaeological Algorithmic Analysis." *ACM SIGCSE Bulletin*, vol. 35, no. 1, 2003, pp. 1–5.** — Shows real running time can diverge from Big O class due to constant factors; also the citation used to justify excluding bubble sort from the essay's algorithm comparison (bubble sort "has no apparent redeeming features"). Justifies finding the threshold empirically rather than theoretically.
6. **"AWS Lambda Pricing." Amazon Web Services, aws.amazon.com/lambda/pricing/. Accessed 5 June 2026.** — Source for the cost model: $0.0000166667 per GB-second. Turns measured time + memory into a dollar cost, answering the "cost efficiency" half of the research question.

Also referenced in the Introduction but not yet in the Key Sources doc: **Jadoon et al. 2011** (empirical algorithm analysis — cited re: empirical studies comparing whole algorithms rather than tuning thresholds). Insertion/merge sort *code* implementations are adapted from GeeksforGeeks (per the docstring in `sort_algorithms.py`) — this still needs a proper citation before submission, separate from the six sources above.

## 5. Current code state

Folder: `CS EE Actual` (the project folder). Files that exist right now:

**`sort_algorithms.py`** — contains, in full:
- `insertionSort(arr)` — standard in-place insertion sort on the whole array.
- `merge(arr, left, mid, right)` — merges two sorted sub-arrays `arr[left..mid]` and `arr[mid+1..right]`.
- `mergeSort(arr, left, right)` — standard recursive merge sort.
- `insertionSortRange(arr, left, right)` — insertion sort restricted to a sub-range (needed because the hybrid must sort *parts* of the array, not just the whole thing).
- `hybridSort(arr, left, right, threshold)` — the hybrid: if the sub-array size (`right - left + 1`) is `<= threshold`, calls `insertionSortRange`; otherwise splits in half, recurses on both halves, then calls `merge`. Call as `hybridSort(arr, 0, len(arr)-1, threshold)`.
- `printArray(arr)` — debug helper.
- A `__main__` block that sorts a small hardcoded 10-item array with all three functions and checks each against Python's built-in `sorted()`.

Insertion sort and merge sort implementations are adapted from GeeksforGeeks (cited in the file's docstring; needs a real MLA citation before submission, see §4).

**`experiment.py`** — currently a minimal first-pass timing script. It:
- Generates ONE random array of 1,000 integers (`random.randint(0, 10000)`).
- Times `insertionSort` and `mergeSort` (not yet the hybrid) with `time.perf_counter()`.
- Measures peak memory for each with `tracemalloc`.
- Prints CSV-style lines: `algorithm,input_size,time_seconds,peak_memory_bytes`.
- Does NOT yet: test `hybridSort`, vary threshold/size/ordering, run multiple trials, write to `results.csv`, or calculate AWS cost.

**`results.csv`** — exists but is empty except for the header row `algorithm,input_size,time_seconds,peak_memory_bytes`. No data collected yet.

## 6. Full experiment design (the target to build toward)

- **Algorithms compared:** pure insertion sort, pure merge sort (baselines), hybrid merge-insertion sort.
- **Thresholds to test (hybrid only):** 5, 10, 20, 30, 40, 50, 100.
- **Input sizes:** 100, 500, 1,000, 5,000, 10,000, 50,000.
- **Data orderings:** random, 75% sorted, reverse sorted. (Need generator functions for each — only the random generator exists so far, in `experiment.py`.)
- **Data type:** arrays of random integers only (decided deliberately — the algorithm itself is data-type agnostic, integers were chosen for simplicity/reproducibility/precedent in the literature). Don't need to generalize to other data types.
- **Trials:** 10 trials per configuration (currently only 1 run per config — the trials loop was deliberately left out for a first, simpler review by Mr. Hare, and needs to be added back now).
- **Total runs:** 126 configs × 10 trials = 1,260 runs.
- **Metrics per run:** execution time (`time.perf_counter`), peak memory (`tracemalloc`), then convert memory+time into an estimated AWS Lambda cost using $0.0000166667 per GB-second.
- **Output:** `results.csv` should end up with columns: `algorithm, threshold, size, ordering, trial, time, memory, cost` (threshold only applies to the hybrid; leave blank/NA for the two baselines).

## 7. Full to-do list (from `EE_To-Do_List.docx`, updated 30 Jul 2026)

**1. Coding & Testing — June–July**
- Finish merge sort (baseline)
- Finish insertion sort (baseline)
- Finish the hybrid algorithm (merge + insertion, with a threshold that can be changed)
- Add a timer (`time.perf_counter`)
- Add memory tracking (`tracemalloc`)
- Add the 10-trial loop back in + a trial column in `results.csv`
- Build the test framework that runs all 126 configs — July
  - Thresholds: 5, 10, 20, 30, 40, 50, 100
  - Sizes: 100, 500, 1K, 5K, 10K, 50K
  - Orderings: random, 75% sorted, reverse sorted
  - Write functions to generate the random / 75%-sorted / reverse arrays
- Add the AWS cost calculator ($0.0000166667 per GB-second)
- Run it on a few configs first to make sure it actually works

**2. Experiments — July–Sep**
- Run everything — 126 configs × 10 trials = 1,260 runs (July/Aug)
- Save it all to `results.csv` (algorithm, threshold, size, ordering, trial, time, memory, cost)
- Check for weird outliers in the data
- Back up `results.csv` somewhere safe
- Work out the averages for each config (Aug)
- Figure out the best threshold for each size/ordering
- Make the graphs (Aug/Sep): time vs. threshold (per size, per ordering), memory vs. threshold, cost vs. threshold
- Write up what the results actually show

**3. Write the Rest of the Essay — Sep–Oct** *(essay-writing tasks, not code — included for context only)*
- Chapter 2 – Research: Big O notation section (done in Draft v4, see §3), algorithm comparison table (bubble, selection, insertion, merge, quicksort, heapsort, Timsort), justify why only 3 algorithms are studied (cite Astrachan for excluding bubble sort), justify merge+insertion specifically, full citations.
- Chapter 3 – Experiment: methodology (setup, hardware, language, config matrix), 3 hypotheses, results tables/graphs, analysis.
- Chapter 4 – Conclusions: compare research vs. findings, answer the research question, limitations + further research.
- Whole-essay checks: word count under 4,000, MLA 9 citations fixed.

**4. Final Steps — Oct–Nov**
- Meet Mr. Hare before end of term
- First full draft → send for feedback → revise (Sep/Oct)
- Proofread + formatting (cover page, contents, word-count declaration)
- Check against IB criteria A–E
- Submit (Nov)

## 8. Where things stand (from `EE_Plan_and_Timeline.docx`, updated 5 Jun 2026, cross-checked against the 30 Jul to-do list)

- Plan and timeline made — done
- Key sources found and read — done
- Introduction written — done (now in its 5th revision, v4, incorporating Mr. Hare's feedback to add the Big O section)
- Coding the algorithms — in progress (baselines + hybrid function exist; test framework does not)
- Testing framework and experiments — not started (no data in `results.csv` yet)
- Meet supervisor before end of term — to do

## 9. What Claude Code should actually do next

In rough order:

1. Confirm/finish `hybridSort` in `sort_algorithms.py` (it appears functionally complete already — verify correctness and that threshold is easy to change).
2. Extend `experiment.py` (or split into a proper test-runner module) to:
   - Test `hybridSort` in addition to the two baselines.
   - Add functions to generate 75%-sorted and reverse-sorted arrays (only random exists now).
   - Add the 10-trial loop back in.
   - Loop over all 126 configs (7 thresholds × 6 sizes × 3 orderings, plus the 2 non-threshold baselines × 6 sizes × 3 orderings).
   - Write every run's results as a row to `results.csv` with columns `algorithm, threshold, size, ordering, trial, time, memory, cost`.
   - Add the AWS Lambda cost calculation ($0.0000166667/GB-second, using peak memory and time per run).
3. Run on a handful of configs first to sanity-check before doing the full 1,260-run sweep.

## 10. Constraints / style notes for Claude Code

- Keep code simple and heavily commented, matching the existing style in `sort_algorithms.py` (plain variable names, explanatory comments, no advanced Python idioms). This is student work that will be read by an IB examiner and a supervisor, not production code.
- In-place sorting (modifying the array passed in) is the established pattern — keep it consistent.
- Don't silently change the experiment design (thresholds, sizes, orderings, trial count) — it's already locked in from the approved proposal. Flag it to Manuel if a change seems necessary rather than just doing it.
- The essay's Introduction deliberately keeps the general framing free of implementation details like "integers" — that's methodology-only detail — so nothing in the code should need to change that framing.
- Terminology consistency matters: the essay uses "cutoff threshold," "subarray"/"piece," and the Big O vocabulary from §3.1 — keep code comments and any generated documentation consistent with that language since it all feeds the same essay.

## 11. Timeline context

It's currently August 2026. Per the original plan, June–July was for finishing the algorithms and test framework, July–September for running experiments and analysis, September–October for writing the rest of the essay, and November for final submission. As of the 30 July to-do list, coding/testing is still the active phase — no experiment data has been collected yet.
