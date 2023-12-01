In ← &fras "inputs/day01.txt"
L ← ⊕□⍜▽¯:\+.=,@\n In

# part 1
/+∵(+⊃(×10⊢)(⊢⇌)▽≠0.∵⍣parse(0;;)⊔) L

# part 2
W ← {"one" "two" "three" "four" "five" "six" "seven" "eight" "nine"}
Rw ← ∵⇌W
Re ← ⊐/⊂↘1♭≡⊂"|"
Fa ← ⍣parse(+1⊗:W□⊙;)⊔⊢regex⊂"\\d|"Re W
Fb ← ⍣parse(+1⊗:Rw□⊙;)⊔⊢regex⊂"\\d|"Re Rw⇌
/+∵(+×10⊃Fa Fb ⊔)L
