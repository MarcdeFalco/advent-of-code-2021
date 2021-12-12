let ic = open_in "input.txt"

let rec assoc () =
    try
        match input_line ic |> String.split_on_char '-' with
        | [v1;v2] -> (v1,v2) :: assoc ()
        | _ -> assoc ()
    with End_of_file -> []

let assocs = assoc()
let fcpl f (x,y) = f x y
let vertices = Array.of_list (List.sort_uniq Stdlib.compare
    (fcpl (@) (List.split assocs)))

exception Found of int
let array_index v x =
    try
        for i = 0 to Array.length v - 1 do
            if v.(i) = x then raise (Found i)
        done; raise Not_found
    with Found i -> i

module IntSet = Set.Make(struct type t = int let compare = Stdlib.compare end)

let graph =
    Array.init (Array.length vertices)
        (fun i -> List.map (array_index vertices)
            (List.map fst (List.filter (fun c -> snd c = vertices.(i)) assocs)
            @ List.map snd (List.filter (fun c -> fst c = vertices.(i)) assocs)))

let is_small v = String.lowercase_ascii v = v
let rec visit x smalls double =
    List.fold_left (+) 0
        (List.map
            (fun i -> let v = vertices.(i) in
                match v with
                | "start" -> 0
                | "end" -> 1
                | _ when is_small v ->
                        if IntSet.mem i smalls
                        then (if double then 0 else visit i smalls true)
                        else visit i 
                               (IntSet.union smalls (IntSet.singleton i)) double
                | _ -> visit i smalls double)
            graph.(x))

let main =
    let start = array_index vertices "start" in
    Printf.printf "Part 1 : %d\n" (visit start IntSet.empty true);
    Printf.printf "Part 2 : %d\n" (visit start IntSet.empty false)
