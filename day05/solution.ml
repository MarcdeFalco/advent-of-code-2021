
module IntPairs =
    struct
         type t = int * int
         let compare (x0,y0) (x1,y1) =
           match Stdlib.compare x0 x1 with
               0 -> Stdlib.compare y0 y1
             | c -> c
    end

module PairsMap = Map.Make(IntPairs)

let mark m (x,y) =
    let up v = match PairsMap.find_opt (x, y) m with
         | None -> Some 1
         | Some v -> Some (v + 1) in
    PairsMap.update (x, y) up m

let rec line_horiz m x y1 y2 =
    if y1 > y2
    then m
    else line_horiz (mark m (x, y1)) x (y1+1) y2

let rec line_vert m y x1 x2 =
    if x1 > x2
    then m
    else line_vert (mark m (x1, y)) y (x1+1) x2

let rec line_diag m c x1 y x2 =
    if x1 > x2
    then m
    else line_diag (mark m (x1, y)) c (x1+1) (y+c) x2

let coeff x1 y1 x2 y2 =
    let dx = float_of_int (x2 - x1) in
    let dy = float_of_int (y2 - y1) in
    dx /. dy

let ic = open_in "input.txt"
let pack4 a b c d = (a, b, c, d)

let rec apply m =
    try
        let s = input_line ic in
        let x1, y1, x2, y2 = Scanf.sscanf s 
             "%d,%d -> %d,%d" pack4 in
        let nm = if x1 = x2
                 then begin
                     if y1 <= y2
                     then line_horiz m x1 y1 y2
                     else line_horiz m x1 y2 y1
                 end else if y1 = y2 
                 then begin
                     if x1 <= x2
                     then line_vert m y1 x1 x2
                     else line_vert m y1 x2 x1
                 end else
                     let c = coeff x1 y1 x2 y2 in
                     let ic = int_of_float c in
                     if c = -1.0 || c = 1.0
                     then begin
                         if x1 <= x2
                         then line_diag m ic x1 y1 x2
                         else line_diag m ic x2 y2 x1
                     end
                else m in
        apply nm
    with End_of_file -> m

let m = apply PairsMap.empty

let count = PairsMap.fold (fun c v s -> if v > 1 then 1+s else s) m 0

let main =
    Printf.printf "%d\n" count

let show_map m n =
    for j = 0 to n-1 do
        for i = 0 to n-1 do
            let v = match PairsMap.find_opt (i, j) m with
                    | Some n -> string_of_int n
                    | None -> "." in
            print_string v
        done;
        print_newline ()
    done


