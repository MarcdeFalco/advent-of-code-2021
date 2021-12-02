
type direction = Forward | Up | Down
type move = direction * int

let direction_of_string s = 
    match s with
    | "forward" -> Forward
    | "up" -> Up
    | "down" -> Down
    | _ -> failwith "Unreachable"

let apply1 (dir, amount) pos depth =
    match dir with
    | Forward -> pos + amount, depth
    | Up -> pos, depth - amount
    | Down -> pos, depth + amount

let rec part1 pos depth = 
    try
        let move = Scanf.scanf "%s %d\n"
            (fun d a -> (direction_of_string d, a)) in
        let npos, ndepth = apply1 move pos depth in
        part1 npos ndepth
    with End_of_file -> Printf.printf "Part1 : %d\n" (pos * depth)

let apply2 (dir, amount) pos depth aim =
    match dir with
    | Forward -> pos + amount, depth + aim*amount, aim
    | Up -> pos, depth, aim - amount
    | Down -> pos, depth, aim + amount

let rec part2 pos depth aim = 
    try
        let move = Scanf.scanf "%s %d\n"
            (fun d a -> (direction_of_string d, a)) in
        let npos, ndepth, naim = apply2 move pos depth aim in
        part2 npos ndepth naim
    with End_of_file -> Printf.printf "Part2 : %d\n" (pos * depth)


let main =
    part2 0 0 0
