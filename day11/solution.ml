(* Advent of Code 2021, jour 11.
   Simulation pas à pas : on incrémente toutes les cases, puis un parcours
   récursif fait flasher les cases qui dépassent 9, chaque flash
   incrémentant les huit voisins ; la matrice visited assure qu'une case
   flashe au plus une fois par pas.
   Partie 1 : nombre de flashs pendant les 100 premiers pas.
   Partie 2 : premier pas où toutes les cases flashent (on suppose qu'il
   arrive après le pas 100). *)

let digit c =
  match c with
  | '0' .. '9' -> int_of_char c - int_of_char '0'
  | _ -> failwith "caractère invalide"

let lire_grille nom =
  let ic = open_in nom in
  let rec lire () =
    match input_line ic with
    | s -> (String.to_seq s |> Array.of_seq |> Array.map digit) :: lire ()
    | exception End_of_file -> close_in ic; []
  in
  Array.of_list (lire ())

let hmap = lire_grille "input.txt"
let w = Array.length hmap.(0)
let h = Array.length hmap

let valid_coord (x, y) = 0 <= x && x < w && 0 <= y && y < h

let product l1 l2 = List.concat_map (fun x -> List.map (fun y -> (x, y)) l2) l1
let all_coords = product (List.init w (fun i -> i)) (List.init h (fun i -> i))

let voisins (x, y) =
  List.filter
    (fun c -> valid_coord c && c <> (x, y))
    (product [ x - 1; x; x + 1 ] [ y - 1; y; y + 1 ])

let h_incr (x, y) = hmap.(y).(x) <- 1 + hmap.(y).(x)
let flash (x, y) = hmap.(y).(x) > 9
let reset (x, y) = if flash (x, y) then hmap.(y).(x) <- 0

(* Un pas de simulation ; renvoie le nombre de cases qui ont flashé. *)
let step () =
  let visited = Array.make_matrix h w false in
  List.iter h_incr all_coords;
  let rec visit (x, y) =
    if not visited.(y).(x) then begin
      visited.(y).(x) <- true;
      List.iter h_incr (voisins (x, y));
      List.iter visit (List.filter flash (voisins (x, y)))
    end
  in
  List.iter visit (List.filter flash all_coords);
  let count_flash = List.length (List.filter flash all_coords) in
  List.iter reset all_coords;
  count_flash

(* Renvoie (flashs des 100 premiers pas, numéro du pas synchronisé). *)
let rec steps n acc =
  let v = step () in
  if v = w * h then (acc, n)
  else steps (n + 1) (if n <= 100 then v + acc else acc)

let () =
  let partie1, partie2 = steps 1 0 in
  Printf.printf "Partie 1 : %d\n" partie1;
  Printf.printf "Partie 2 : %d\n" partie2
