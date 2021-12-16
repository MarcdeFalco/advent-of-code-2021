let ic = open_in "input.txt"
let s = input_line ic
let l = Array.of_list (List.map int_of_string (String.split_on_char ',' s))
let m = Array.fold_left max min_int l
let all_pos = Array.init (m+1) (fun i -> i)

let cout part v =
    let cout_elt part v o = let d = abs(v-o) in
        if part = 1 then d else (d*(d+1))/2
    in
    Array.fold_left (+) 0 (Array.map (cout_elt part v) l)

let main =
    for part = 1 to 2 do
        let res = Array.fold_left min max_int (Array.map (cout part) all_pos) in
        Printf.printf "Part %d: %d\n" part res
    done


