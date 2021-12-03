let get_values () =
    let ic = open_in "input.txt" in
    let rec read () = 
        try
            let l = input_line ic in
            l :: read()
        with End_of_file -> []
    in read ()

let values = get_values ()
let nvalues = List.length values

let compte l i x =
    let rec compte_aux l acc =
        match l with
        | [] -> acc
        | t::q -> compte_aux q (if t.[i] = x then 1+acc else acc)
    in compte_aux l 0

let rec most i =
    if i = 12
    then []
    else let n1 = compte values i '1' in
        (if n1 >= nvalues/2 then 1 else 0) :: most (i+1)

let bin2int l =
    let rec bin2int_aux l acc = 
        match l with
        | [] -> acc
        | t::q -> bin2int_aux q (2*acc+t)
    in bin2int_aux l 0

let part1 = 
    let m = bin2int (most 0) in
    let l = 1 lsl 12 - m - 1 in
    Printf.printf "Part 1: %d\n" (m * l)

let string_to_binlist s =
    List.init (String.length s)
        (fun i -> if s.[i] = '1' then 1 else 0)

let rec split l f =
    match l with
    | [] -> ([], [])
    | t::q -> let l1, l2 = split q f in
        if f t then t :: l1, l2 else l1, t :: l2

let rec search l i most =
    match l with
    | [x] -> bin2int (string_to_binlist x)
    | _ -> 
        let v1, v0 = split l (fun s -> s.[i] = '1') in
        let n1, n0 = List.length v1, List.length v0 in
        let v1, v0 = if most then v1, v0 else v0, v1 in
        if n1 >= n0
        then search v1 (i+1) most
        else search v0 (i+1) most
        
let part2 = 
    let oxygen = search values 0 true in
    let co2 = search values 0 false in
    Printf.printf "Part 2: %d\n" (oxygen * co2)

