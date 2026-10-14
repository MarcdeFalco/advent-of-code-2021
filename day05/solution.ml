(* Advent of Code 2021, jour 5.
   Chaque segment est tracé point par point dans un dictionnaire (Map)
   case -> nombre de segments ; on compte les cases couvertes au moins deux
   fois. La partie 1 ignore les diagonales, la partie 2 les trace (pente
   +1 ou -1). *)

module IntPairs = struct
  type t = int * int
  let compare = Stdlib.compare
end

module PairsMap = Map.Make (IntPairs)

let mark m (x, y) =
  let up v = match v with
    | None -> Some 1
    | Some v -> Some (v + 1)
  in
  PairsMap.update (x, y) up m

(* segment {x} × [y1, y2] *)
let rec line_vert m x y1 y2 =
  if y1 > y2 then m else line_vert (mark m (x, y1)) x (y1 + 1) y2

(* segment [x1, x2] × {y} *)
let rec line_horiz m y x1 x2 =
  if x1 > x2 then m else line_horiz (mark m (x1, y)) y (x1 + 1) x2

(* diagonale de pente c partant de (x1, y) jusqu'à l'abscisse x2 *)
let rec line_diag m c x1 y x2 =
  if x1 > x2 then m else line_diag (mark m (x1, y)) c (x1 + 1) (y + c) x2

let coeff x1 y1 x2 y2 =
  let dx = float_of_int (x2 - x1) in
  let dy = float_of_int (y2 - y1) in
  dx /. dy

let lire_segments nom =
  let ic = open_in nom in
  let rec lire () =
    match input_line ic with
    | s -> Scanf.sscanf s "%d,%d -> %d,%d" (fun a b c d -> (a, b, c, d)) :: lire ()
    | exception End_of_file -> close_in ic; []
  in
  lire ()

let trace diagonales m (x1, y1, x2, y2) =
  if x1 = x2 then
    (if y1 <= y2 then line_vert m x1 y1 y2 else line_vert m x1 y2 y1)
  else if y1 = y2 then
    (if x1 <= x2 then line_horiz m y1 x1 x2 else line_horiz m y1 x2 x1)
  else if diagonales then begin
    let c = coeff x1 y1 x2 y2 in
    if c = -1.0 || c = 1.0 then begin
      let ic = int_of_float c in
      if x1 <= x2 then line_diag m ic x1 y1 x2 else line_diag m ic x2 y2 x1
    end else m
  end else m

let recouvrements segments diagonales =
  let m = List.fold_left (trace diagonales) PairsMap.empty segments in
  PairsMap.fold (fun _ v s -> if v > 1 then s + 1 else s) m 0

let partie1 segments = recouvrements segments false
let partie2 segments = recouvrements segments true

let () =
  let segments = lire_segments "input.txt" in
  Printf.printf "Partie 1 : %d\n" (partie1 segments);
  Printf.printf "Partie 2 : %d\n" (partie2 segments)
