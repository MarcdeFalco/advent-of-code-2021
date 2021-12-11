let ic = open_in "input.txt"

let digit c = match c with
    | '0'..'9' -> int_of_char c - int_of_char '0'
    | _ -> failwith "Invalid character"

let rec hmap_l () =
    try
        let s = input_line ic |> String.to_seq |> Array.of_seq |> Array.map digit in
        s :: hmap_l ()
    with End_of_file -> []
let hmap = Array.of_list (hmap_l ())
let w = Array.length hmap.(0)
let h = Array.length hmap
let valid_coord (x,y) = 0 <= x && x < w && 0 <= y && y < h

let voisins (x,y) =
    List.filter
        valid_coord
        [ (x-1,y); (x+1,y); (x,y-1); (x,y+1) ]

let low_point (x,y) =
    let min_voisins = List.fold_left min 9 (List.map (fun (x,y) ->
        hmap.(y).(x)) (voisins (x,y))) in
    min_voisins > hmap.(y).(x)

let all_coords = List.fold_left (@) [] (List.init w (fun x -> List.init h (fun y -> (x,y))))
let low_points = List.filter low_point all_coords

let basin (x,y) =
    let visited = Array.make_matrix h w false in
    let rec visit (x,y) =
        if not visited.(y).(x)
        then begin
            visited.(y).(x) <- true;
            List.fold_left (+) 1
                (List.map (fun (vx, vy) -> if not visited.(vy).(vx) && hmap.(vy).(vx) <> 9
                                           then visit (vx, vy)
                                           else 0) (voisins (x,y)))
        end else 0
    in visit (x,y)

let main =
    Printf.printf "Part 1 : %d\n"
        (List.fold_left (+) 0 (List.map (fun (x,y) -> 1+hmap.(y).(x)) low_points));
    let basins = List.map basin low_points in
    match List.rev (List.sort (Stdlib.compare) basins) with
    | a::b::c::_ -> Printf.printf "Part 2 : %d\n" (a*b*c)
    | _ -> failwith "Unreachable"

