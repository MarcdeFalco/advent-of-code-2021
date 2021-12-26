let ic = open_in "input.txt"

type tree = Leaf of int | Node of tree * tree

let is_digit c = match c with
    | '0'..'9' -> true
    | _ -> false

let read_number s i =
    let j = ref i in
    let n = ref 0 in
    while !j < String.length s && is_digit s.[!j] do
        n := 10 * !n + (int_of_char s.[!j] - 48);
        incr j
    done;
    Leaf !n, !j

let rec parse_tree s i =
    if is_digit s.[i]
    then read_number s i
    else let left, i1 = parse_tree s (i+1) in
        let right, i2 = parse_tree s (i1+1) in
        Node(left, right), i2+1

let rec read_snails () =
    try
        let l = input_line ic in
        fst (parse_tree l 0) :: read_snails ()
    with End_of_file -> []

let snails = read_snails ()

type path = Left of tree | Right of tree

let rec add_rightmost t v =
    match t with
    | Leaf n -> Leaf (n+v)
    | Node(a,b) -> Node(a, add_rightmost b v)

let rec add_leftmost t v =
    match t with
    | Leaf n -> Leaf (n+v)
    | Node(a,b) -> Node(add_leftmost a v, b)

let rec rebuild path t left_add right_add =
    match path, left_add, right_add with
    | [], _, _ -> t
    | Right tl :: q, Some v, _ -> rebuild q (Node(add_rightmost tl v, t)) None right_add
    | Right tl :: q, None, _ -> rebuild q (Node(tl, t)) None right_add
    | Left tl :: q, _, Some v -> rebuild q (Node(t, add_leftmost tl v)) left_add None
    | Left tl :: q, _, None -> rebuild q (Node(t, tl)) left_add None

let rec explode_aux t path depth =
    match t with
    | Leaf n -> None
    | Node(Leaf a, Leaf b) when depth >= 4 ->
            Some (rebuild path (Leaf 0) (Some a) (Some b))
    | Node(a,b) ->
        match explode_aux a (Left b::path) (depth+1) with
        | None -> explode_aux b (Right a::path) (depth+1)
        | Some t -> Some t

let explode t = explode_aux t [] 0

let rec split t =
    match t with
    | Leaf n when n > 9 -> Some (Node (Leaf (n/2), Leaf ((n+1)/2)))
    | Leaf _ -> None
    | Node(a,b) -> match split a with
        | None -> begin
              match split b with
              | None -> None
              | Some b' -> Some (Node(a, b'))
            end
        | Some a' -> Some (Node(a', b))

let rec reduce t =
    match explode t with
    | Some t' -> reduce t'
    | None -> match split t with
        | Some t' -> reduce t'
        | None -> t
    
let rec magnitude t = 
    match t with
    | Leaf n -> n
    | Node(a, b) -> 3 * magnitude a + 2 * magnitude b
    
let main =
    let addition = List.fold_left 
        (fun t1 t2 -> reduce (Node(t1, t2)))
        (List.hd snails) (List.tl snails) in
    Printf.printf "Part 1 : %d\n" (magnitude addition);
    let max_magnitude = List.fold_left
        max 0
        (List.map (fun x -> 
            List.fold_left max 0
                (List.map (fun y -> magnitude @@ reduce (Node(x,y)))
                    (List.filter ((<>) x) snails))) snails)
    in Printf.printf "Part 2 : %d\n" max_magnitude

let tikz_of_tree t =
    let rec aux t = 
        match t with
        | Leaf n -> "node {" ^ string_of_int n ^ "}"
        | Node(a,b) -> "node {$\\bullet$} child {" ^ aux a ^ "} "
            ^ "child {" ^ aux b ^ "}"
    in "\\" ^ aux t ^ ";"

let pretty =
    let t, _ = parse_tree "[[[[0,7],4],[15,[0,13]]],[1,1]]" 0 in
    Printf.printf "%s\n" (tikz_of_tree t)

let rec string_of_tree t =
    match t with
    | Leaf n -> string_of_int n
    | Node(a,b) -> "[" ^ string_of_tree a ^ "," ^ string_of_tree b ^ "]"


