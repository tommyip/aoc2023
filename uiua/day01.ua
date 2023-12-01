L ← ⊕□⍜▽¯:\+.=,@\n &fras "inputs/day01.txt"

# part 1
/+∵(+×10⊃⊢(⊢⇌)▽≠0.∵⍣parse(0;;)⊔)L

# part 2
W ← {"one" "two" "three" "four" "five" "six" "seven" "eight" "nine"}
F! ← ⍣parse(+1⊗:^0□⊙;)⊔⊢regex⊂"\\d"⊐/⊂♭≡⊂@|
/+∵(+×10⊃(F!W W)(F!(∵⇌W)∵⇌W⇌)⊔)L
