let ic = open_in "input.txt"
let s = input_line ic

type bitstream = {
    mutable pos : int;
    mutable sub_pos : int
}

let get_bit b =
    let c = match s.[b.pos] with
        | '0'..'9' as c -> int_of_char c - int_of_char '0'
        | 'A'..'F' as c -> 10 + int_of_char c - int_of_char 'A'
        | _ -> failwith "Invalid character"
    in
    let bit = (c lsr (3 - b.sub_pos)) mod 2 in
    if b.sub_pos = 3
    then begin
        b.pos <- b.pos + 1;
        b.sub_pos <- 0
    end else
        b.sub_pos <- b.sub_pos + 1;
    bit

let get_number b n =
    let rec aux n acc =
        if n = 0 then acc
        else aux (n-1) (2 * acc + get_bit b)
    in aux n 0

type operator = Plus | Mult | Max | Min | Gt | Lt | Eq
type packet = Litteral of int * int
    | Operator of operator * packet list * int
let operator_of_pid pid = [| Plus; Mult; Min; Max; Plus; Gt; Lt; Eq |].(pid)

let get_litteral_value b =
    let rec aux acc count =
        let header = get_bit b in
        let value = get_number b 4 in
        let nacc = 16 * acc + value in
        if header = 0 
        then nacc, count*5 
        else aux nacc (count+1)
    in aux 0 1

let rec get_packet b =
    let version = get_number b 3 in
    let pid = get_number b 3 in
    if pid = 4
    then begin
        let lit, lit_size = get_litteral_value b in
        Litteral (lit, version), lit_size+6
    end else begin
        let lid = get_bit b in
        let sub, size =
            if lid = 0
            then let length = get_number b 15 in
                let sl = get_sub_packets_length b length in
                (sl, length + 15 + 7)
            else let count = get_number b 11 in
                let sl, size = get_sub_packets_count b count in
                (sl, size + 11 + 7)
        in Operator(operator_of_pid pid, sub, version), size
    end
and get_sub_packets_length b l =
    if l = 0
    then []
    else let p, size = get_packet b in
        p :: get_sub_packets_length b (l - size)
and get_sub_packets_count b n =
    if n = 0
    then [], 0
    else let p, size = get_packet b in
        let pl, sizel = get_sub_packets_count b (n-1) in
        p::pl, size+sizel

let rec version packet =
    match packet with
    | Litteral (_, v) -> v
    | Operator(_, sub, v) -> v + List.fold_left (+) 0 (List.map version sub)

let rec fold op l =
    match l with
    | [] -> failwith "No arguments"
    | [x] -> x
    | hd::tl -> op hd (fold op tl)

let cmp_gt x y = if x > y then 1 else 0
let cmp_lt x y = if x < y then 1 else 0
let cmp_eq x y = if x = y then 1 else 0

let rec value packet =
    match packet with
    | Litteral(lit, _) -> lit
    | Operator(op, sub, _) ->
        let sub_values = List.map value sub in
        fold (match op with
            | Plus -> (+)
            | Mult -> ( * )
            | Max -> max
            | Min -> min
            | Gt -> cmp_gt
            | Lt -> cmp_lt
            | Eq -> cmp_eq) sub_values

let string_of_operator operator = match operator with
    | Plus -> "+"
    | Mult -> "*"
    | Max -> "max"
    | Min -> "min"
    | Gt -> ">"
    | Lt -> "<"
    | Eq -> "="

let rec string_of_packet p =
    match p with
    | Litteral(value, _) ->  string_of_int value
    | Operator(op, sub, _) -> 
            "(" ^ string_of_operator op ^ " " 
            ^ (String.concat " " (List.map string_of_packet sub))
            ^ ")"


let main =
    let b = { pos = 0; sub_pos = 0 } in
    let p, _ = get_packet b in
    Printf.printf "%s\n" (string_of_packet p);
    Printf.printf "Part 1: %d\n" (version p);
    Printf.printf "Part 2: %d\n" (value p)


