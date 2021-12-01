let rec read_depths () =
    try
        let depth = read_int () in
        depth :: read_depths ()
    with End_of_file -> []

let depths = read_depths ()

let rec count_inc_aux l prec acc = 
    match l with
    | [] -> acc
    | t::q -> count_inc_aux q t
        ((if t > prec then 1 else 0)+acc)

let count_inc l =
    match l with
    | [] -> failwith "Empty list"
    | t::q -> count_inc_aux q t 0

let part1 =
    Printf.printf "Part 1 : %d\n"
        (count_inc depths)

let rec count_winc_aux l w w1 w2 w3 acc = 
    match l with
    | [] -> acc
    | t::q ->
        let nw = w - w1 + t in
        count_winc_aux q nw w2 w3 t
        ((if nw > w then 1 else 0)+acc)

let count_winc l =
    match l with
    | w1::w2::w3::q -> 
        count_winc_aux q (w1+w2+w3)
            w1 w2 w3 0
    | _ -> failwith "Empty list"

let part2 =
    Printf.printf "Part 2 : %d\n"
        (count_winc depths)

(* Non recursive version *)
let a_depths = Array.of_list depths

let part2 =
    let increased = ref 0 in
    let w = ref (a_depths.(0) 
        + a_depths.(1) + a_depths.(2)) in
    for i = 3 to Array.length a_depths - 1 do
        let nw = !w - a_depths.(i-3) + a_depths.(i) in
        if nw > !w
        then incr increased
    done;
    Printf.printf "Part 2 : %d\n" !increased


