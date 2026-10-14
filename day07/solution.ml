(* Advent of Code 2021, jour 7.
   Force brute : on essaie toutes les positions de 0 au maximum et on garde
   la plus petite somme des coûts ; le coût d'un déplacement de d vaut d
   (partie 1) ou d(d+1)/2 (partie 2). *)

let lire_positions nom =
  let ic = open_in nom in
  let s = input_line ic in
  close_in ic;
  Array.of_list (List.map int_of_string (String.split_on_char ',' (String.trim s)))

let cout_minimal positions cout =
  let m = Array.fold_left max min_int positions in
  let total cible =
    Array.fold_left (fun acc p -> acc + cout (abs (p - cible))) 0 positions
  in
  Array.fold_left min max_int (Array.init (m + 1) total)

let partie1 positions = cout_minimal positions (fun d -> d)
let partie2 positions = cout_minimal positions (fun d -> d * (d + 1) / 2)

let () =
  let positions = lire_positions "input.txt" in
  Printf.printf "Partie 1 : %d\n" (partie1 positions);
  Printf.printf "Partie 2 : %d\n" (partie2 positions)
